import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import datetime as dt
import numpy as np
import yaml
from pathlib import Path
import os

# --- Accès aux google sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def load_config(path) -> dict:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# Définition de l'environnement
cfg = load_config("config.yaml")
env = cfg.get("env", "dev")  # "dev" ou "prod"


@st.cache_resource
def _gspread_client():
    "Chargement des crédentials GCP"
    creds = Credentials.from_service_account_info(os.environ["GCP"], scopes=SCOPES)
    return gspread.authorize(creds)


def _ws(sheet_id: str, worksheet: str):
    """Récupère une worksheet par nom, crée si absente."""
    gc = _gspread_client()
    sh = gc.open_by_key(sheet_id)
    try:
        return sh.worksheet(worksheet)
    except gspread.WorksheetNotFound:
        return sh.add_worksheet(title=worksheet, rows=1000, cols=26)


@st.cache_data
def load_table(env: str, table: str) -> pd.DataFrame:
    """Chargement des données dev/prod, mis en cache par Streamlit."""
    if env == "prod":
        # SHEET_ID vient de .streamlit/secrets.toml, section [prod]
        sheet_id = os.environ["SHEET_ID"]

        # à adapter : ici tu utilises _ws pour récupérer la worksheet
        ws = _ws(sheet_id, table)  # ou autre nom d’onglet
        rows = ws.get_all_records()  # suppose 1re ligne = en-têtes
        df = pd.DataFrame(rows)

    elif env == "dev":
        # BDD depuis un fichier CSV
        paths = os.environ["BDD"]
        df = pd.read_csv(paths[table], sep=";")

    else:
        raise ValueError(f"Environnement inconnu : {env}")

    return df


# -- Téléchargement des données
BDD = load_table(env, "BDD")


def to_native(v):
    # NaN/NaT -> ""
    if (
        v is None
        or (isinstance(v, float) and pd.isna(v))
        or (isinstance(v, str) and v == "nan")
    ):
        return ""
    if isinstance(v, (pd.Timestamp, dt.datetime, dt.date)):
        return v.isoformat()
    if isinstance(v, np.generic):  # numpy.int64, float64, bool_...
        return v.item()
    return v


def append_row_sheet(row: dict, worksheet="Feuille1"):
    append_rows_sheet([row], worksheet)


def append_rows_sheet(rows: list[dict], worksheet="Feuille1"):
    global BDD

    if not rows:
        return

    ws = _ws(os.environ["SHEET_ID"], worksheet)

    # Récupérer / créer les headers
    headers = ws.row_values(1)
    if not headers:
        # on prend les clés du premier dict comme référence
        headers = list(rows[0].keys())
        ws.update("A1", [headers])

    # Construire la matrice de valeurs dans l'ordre des headers
    values_matrix = []
    for row in rows:
        values_matrix.append([to_native(row.get(h, "")) for h in headers])

    # Append en une seule fois
    ws.append_rows(values_matrix, value_input_option="USER_ENTERED")

    # 🔁 on recharge les données après l’écriture
    BDD = load_table(env, "BDD")

    # 🧹 On invalide tous les caches de données Streamlit
    st.cache_data.clear()
