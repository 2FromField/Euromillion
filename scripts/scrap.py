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

# Désactivation des logs
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("webdriver").setLevel(logging.WARNING)

# Enregistrement des logs
logging.basicConfig(
    filename="logs/scrap.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Date du scrap
logging.critical(f'Date du scrapping: {datetime.today().strftime("%d/%m/%Y")}')

# Configuration du driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Mode headless
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# options.add_argument(
#     "--disable-gpu"
# )  # Désactiver l'accélération GPU (utile sur certains OS)
# options.add_argument(
#     "--no-sandbox"
# )  # Recommandé pour éviter des erreurs sur certains systèmes
# options.add_argument("--disable-dev-shm-usage")  # Pour éviter des crashs sur Linux

# Télécharger et utiliser le bon ChromeDriver
service = Service(ChromeDriverManager().install())

# Années à scrapper
years = list(range(2004, datetime.now().year + 1))

# Jeu de données final
df_all = pd.DataFrame([])

# Dataframe
for year in tqdm(years, desc="Récupération des données..."):

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

    # Ajouter au dataframe final
    df_all = pd.concat([df_all, df], ignore_index=True)

    # Fermer la page web
    driver.quit()

# Sauvegarder les données au forma CSV
df_all.to_csv("Data/euromillion.csv", sep=";")
print(df_all)
