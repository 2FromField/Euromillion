from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)
from selenium.webdriver.safari.options import Options
from selenium import webdriver
import pandas as pd
import time
from tqdm import tqdm
import logging
from datetime import datetime
from pathlib import Path
import os
import scrap_utils
import yaml


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
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CONFIG_PATH = Path(__file__).resolve().with_name("config.yaml")


# Environnement ("dev" OU "prod")
def load_config(path: str | Path = CONFIG_PATH) -> dict:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


cfg = load_config()
env = cfg.get("env", "dev")  # "dev" ou "prod"
logging.warning(f"Scrapping des données en mode '{env}'")

# Base de données
if env == "dev":
    outpath = (ROOT / cfg[env]["data"]["TABLE"]).resolve()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    entire_df = scrap_utils.load_table(env, "BDD")  # fichier CSV
else:  # "prod"
    entire_df = scrap_utils.load_table(env, "BDD")  # Google Sheet

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
        scrap_utils.append_rows_sheet([row_dict], "BDD")
