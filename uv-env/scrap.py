from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pandas as pd
from tqdm import tqdm
import logging
from datetime import datetime
from pathlib import Path
import os
import yaml
import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
import numpy as np
import datetime as dt
import json


#######################################################
##                      LOGS                         ##
#######################################################

# Chemnin relatif au dépot Git
ROOT = Path(os.getenv("GITHUB_WORKSPACE", Path(__file__).resolve().parents[1]))

# Désactivation des logs Selenium
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("webdriver").setLevel(logging.WARNING)

# Enregistrement des logs
log_path = ROOT / "uv-env" / "app" / "logs" / "scrap.log"
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Date du scrap
logging.critical(f'Date du scrapping: {datetime.today().strftime("%d/%m/%Y")}')

# Configuration du driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Mode headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

if os.getenv("GITHUB_ACTIONS") == "true":
    # sur Ubuntu runner, Chrome est généralement ici après setup-chrome
    options.binary_location = os.getenv(
        "CHROME_PATH"
    )  # setup-chrome exporte souvent ça
else:
    # local Mac (optionnel) : laisse Selenium trouver Chrome automatiquement,
    options.binary_location = (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )
    pass


#######################################################
##                      ENV                          ##
#######################################################

CONFIG_PATH = Path(__file__).resolve().with_name("config.yaml")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def load_config(path: Path = CONFIG_PATH) -> dict:
    path = Path(path)
    print("CONFIG_PATH used:", path)
    print("CONFIG exists:", path.exists())
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


cfg = load_config()
env = cfg.get("env", "dev")  # "dev" ou "prod"
logging.warning(f"Scrapping des données en mode '{env}'")


@st.cache_resource
def _gspread_client():
    "Chargement des crédentials GCP"
    sa_json = os.environ["GCP"]  # ou "GCP"
    sa_info = json.loads(sa_json)  # <-- dict
    creds = Credentials.from_service_account_info(sa_info, scopes=SCOPES)
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


#######################################################
##                     SCRAP                         ##
#######################################################

# Base de données
if env == "dev":
    outpath = (ROOT / cfg[env]["data"]["TABLE"]).resolve()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    entire_df = load_table(env, "BDD")  # fichier CSV
else:  # "prod"
    entire_df = load_table(env, "BDD")  # Google Sheet

# Télécharger et utiliser le bon ChromeDriver
service = Service(ChromeDriverManager().install())

# Années à scrapper
if not entire_df.empty:
    years = list(range(datetime.now().year, datetime.now().year + 1))
else:
    years = list(range(2004, datetime.now().year + 1))


# Jeu de données final
df_all = pd.DataFrame([])

# Normaliser Date côté CSV (au jour)
entire_df["Date"] = pd.to_datetime(entire_df["Date"], errors="coerce").dt.normalize()

# Set des dates existantes (rapide + fiable)
existing_dates = set(entire_df["Date"].dropna())

# Dataframe
for year in tqdm(years, desc=f"Récupération des données..."):
    print(f"Capture des données de l'année {year}")

    # Accès à la page web
    url = f"https://www.tirage-euromillions.net/euromillions/annees/annee-{year}/"
    driver = webdriver.Chrome(options=options, service=service)
    driver.get(url)

    # Localiser la table par son XPath, ID, ou une autre méthode
    table = driver.find_element(By.XPATH, "//table")  # Modifier selon le cas

    # Récupérer toutes les lignes de la table
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Extraire les en-têtes (th) et les cellules (td)
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "th") + row.find_elements(
            By.TAG_NAME, "td"
        )
        data.append([cell.text for cell in cells])

    # Convertir en DataFrame Pandas
    df = pd.DataFrame(data)

    # Définir la première ligne comme en-tete
    df.columns = df.iloc[0]
    df = df[1:]  # Supprimer la première ligne des données
    df.reset_index(drop=True, inplace=True)  # Réindexer proprement

    # Supprimer les lignes sans valeurs
    df = df.dropna(subset=["Tirage"])

    # Reformater les dates
    df["Date"] = df["Date"].str.extract(r"(\d{2}/\d{2}/\d{4})")

    # Convertir en datetime + normaliser (au jour)
    df["Date"] = pd.to_datetime(
        df["Date"], format="%d/%m/%Y", errors="coerce"
    ).dt.normalize()

    try:
        # Si le site renvoie "Tirage Gagnant" au lieu de "Tirage"
        df = df.rename(columns={"Tirage Gagnant": "Tirage"})

        num_cols = ["n1", "n2", "n3", "n4", "n5", "e1", "e2"]

        # Extraire les nombres (robuste même si Tirage = "-" ou vide)
        nums = df["Tirage"].astype(str).str.findall(r"\d+")

        # Garder uniquement les lignes qui ont exactement 7 nombres (5 + 2 étoiles)
        mask_ok = nums.str.len().eq(7)

        # Logger les lignes invalides (ex: "-")
        if (~mask_ok).any():
            bad = df.loc[~mask_ok, ["Date", "Tirage"]].copy()
            for _, r in bad.iterrows():
                logging.warning(f"Tirage illisible le {r['Date']}: {r['Tirage']}")

        # Construire un df propre uniquement avec les tirages valides
        df_ok = df.loc[mask_ok].copy()

        # Si df_ok est vide, rien à ajouter
        if df_ok.empty:
            df_new = df_ok.copy()
        else:
            df_ok[num_cols] = pd.DataFrame(
                nums[mask_ok].tolist(), index=df_ok.index
            ).astype("Int64")

            # Garder uniquement les nouvelles dates
            df_new = df_ok[~df_ok["Date"].isin(existing_dates)].copy()

            # Mettre à jour le set pour éviter les doublons dans les itérations suivantes
            existing_dates.update(df_new["Date"].dropna())

            # Drop colonnes inutiles
            df_new = df_new.drop(columns=["Tirage"], errors="ignore")

    except Exception as e:
        date_safe = (
            df["Date"].iloc[0] if "Date" in df.columns and len(df) > 0 else "unknown"
        )
        logging.exception(
            f"Erreur récupération des données (date approx: {date_safe.strftime('%Y-%m-%d')})"
        )
        df_new = pd.DataFrame()  # pour éviter de planter le reste de la boucle

    if not df_new.empty:
        # Ajouter les nouvelles lignes
        df_all = pd.concat([df_all, df_new], ignore_index=True)
        logging.info(f"Nouvelles données: {df_new}")
        save = True
    else:
        save = False
        logging.warning("Pas de nouveaux tirages à ajouter")

    # Fermer la page web
    driver.quit()

# Enregistrer les nouvelles données s'il en existe
if save:
    # Trier de la plus ancienne à la plus récente
    df_all = df_all.sort_values(by="Date", ascending=True).reset_index(drop=True)

    if env == "dev":
        # Sauvegarder les données au format CSV
        df_all.to_csv(outpath, sep=";", index=False, mode="a", header=None)
    else:  # "prod"
        row_list = df_new.squeeze().tolist()  # nouvelle ligne
        cols = ["Date", "Gagnant", "Jackpot", "n1", "n2", "n3", "n4", "n5", "e1", "e2"]
        row_dict = dict(zip(cols, row_list))  # conversion en dictionnaire
        row_dict["Jackpot"] = str(row_dict["Jackpot"])
        row_dict["Date"] = row_dict["Date"].strftime(
            "%d/%m/%Y"
        )  # modifier la date au bon format
        append_rows_sheet([row_dict], "BDD")
