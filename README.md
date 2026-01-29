# Projet BeMillionnaire

![Pandas](https://img.shields.io/badge/Pandas%20v2.3.0-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium%20v4.34.0-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)
![Numpy](https://img.shields.io/badge/Numpy%20v2.2.6-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![Github Pages](https://img.shields.io/badge/GitHub%20Pages-222222?style=for-the-badge&logo=github%20Pages&logoColor=white)
![Excel](https://img.shields.io/badge/Microsoft_CSV-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

# 🖼️ Présentation

Projet visant à récupérer les données depuis le site internet open-source https://www.tirage-euromillions.net/ et à les restructurer pour en tirer profit au sein d'une application.<br>
L'application "BeMillionnaire" vient quant à elle appeller ces mêmes données pour permettre aux différents utilisateurs de concevoir leurs prochains pronostics tout en ayant la transparence des résultats antérieurs.

# ✨ Fonctionnalités

- Historique des tirages officiels de l'Euromillion
- Statistiques & Probabilités interactifs selon vos pronostics
- Déploiement GitHub -> Streamlit Community Cloud
- Secrets sécurisés (credentials GCP + SHEET ID) via Secrets Manager Streamlit
- Datavisualisation via Altair

# 🗂️ Arborescence

```
├── 📁 .github
│   └── 📁 workflows
│       └── ⚙️ daily-update.yml             # Fichier d'automatisation via GithHub Pages
├── 📁 logs
├── 📁 scripts
│   ├── 📄 analysis.ipynb                   # Datamining
│   └── 🐍 scrap.py                         # Script de scrapping des données
├── 📁 uv-env
│   ├── 📁 app
│   │   ├── 📁 assets                       # Elements annexés au projet (img,photo,etc)
│   │   ├── 📁 data
│   │   │   └── 📄 euromillion.csv          # Base de données
│   │   ├── 📁 pages
│   │   │   ├── 🐍 0_Pronostic.py           # Page interactif de simulation
│   │   │   └── 🐍 1_Historique.py          # Page "Historique" des tirages
│   │   ├── 🐍 app.py                       # Application Streamlit
│   │   └── 🐍 utils.py                     # Fichier de fonctions
│   ├── ⚙️ .gitignore                       # Exclusions git
│   ├── ⚙️ config.yaml                      # Fichier de configiration "prod"/"dev"
│   ├── 🐍 main.py
│   └── ⚙️ pyproject.toml                   # Dépendances UV-python
└── 📝 README.md                            # Documentation
```

# 📦 Aperçu technique

- Automation: Github Pages (daily-update.yml)
- Frontend : Streamlit
- Données : Scraping avec Selenium et stockage sur Google Sheets (via gspread, google-auth)
- Viz : Altair
- Pandas pour la logique data (split double “A/B”, mapping rangs, KPIs)
- Gestion d’état : st.session_state (confirmations, filtres, formulaires)
- Cache : @st.cache_data pour les lectures stables

# ✅ Prérequis

- Un compte Google et un Google Sheet (formaté avec vos onglets de données).
- Un projet Google Cloud avec un Service Account et une clé JSON.
- Un repo GitHub public/privé contenant cette app.

# 🧰 Installation & Lancement (local)

1. Cloner: `git clone https://github.com/2FromField/$REPO.git && cd env-uv`

2. Python 3.10+ recommandé: `python -m venv .venv && source .venv/bin/activate # Windows: .venv\Scripts\activate`

3. Dépendances: `pip install -r requirements.txt`

4. Secrets: créez .streamlit/secrets.toml comme ci-dessus

5. Lancer: `uv run streamlit run app/app.py`

# 🔐 Google Cloud & Google Sheets (accès service account)

1. Créer un Service Account (GCP → IAM & Admin → Service Accounts) et générer une clé JSON.
2. Dans Google Sheets, partager le document à l’e-mail du service account (le compte doit avoir au moins Éditeur sur le fichier).
3. Notez l’ID du Sheet, l’URL ressemble à `https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit#gid=0` et <SHEET_ID> est la valeur à copier.
4. Onglets requis dans votre fichier (exemples) :

- BDD: Date, Gagnant, Jackpot, n1, n2, n3, n4, n5, e1, e2

# 🔑 Secrets (local & cloud)

En local, créez `.streamlit/secrets.toml` pour y stocker vos données sensibles (comme ci-joint):

```
[prod]
SHEET_ID = "<votre_sheet_id>"
[dev]
BDD = "path/to/bdd.csv"
[gcp]
type = "service_account"
project_id = "<...>"
private_key_id = "<...>"
private_key = """-----BEGIN PRIVATE KEY-----
...votre clé...
-----END PRIVATE KEY-----"""
client_email = "<service-account>@<project>.iam.gserviceaccount.com"
client_id = "<...>"
token_uri = "https://oauth2.googleapis.com/token"
```

Sur Streamlit Community Cloud:

1. Dans Manage App → Settings → Secrets, collez le même contenu (YAML/TOML-like).
2. Ajoutez SHEET_ID et le bloc [gcp].

# ☁️ Déploiement — Streamlit Community Cloud

1. Poussez le code sur GitHub (branche main de préférence).
2. Allez sur streamlit.io → Community Cloud → Deploy an app.
3. Pointez vers votre repo/branche, et chemin du script (ex: app/app.py).
4. Dans Secrets, collez le contenu de votre secrets.toml.
5. Vérifiez que le `requirements.txt` contient au minimum :

- streamlit
- pandas
- gspread
- google-auth
- altair
  Ainsi qu'un `runtime.txt` avec python-3.10.

6. Déployez. L’URL aura la forme https://<app-name>-<user>.streamlit.app.

# 🐍 Scraping

Lancer le scraping manuellement: `python ./Euromillion/scripts/scrap.py`

Exemple de sortie:

```
Récupération des données...:  43%|██████████████████████████████████████████████                                                            | 10/23 [01:01<01:38,  7.60s/it]Capture des données de l'année 2014
Récupération des données...:  48%|██████████████████████████████████████████████████▋                                                       | 11/23 [01:10<01:35,  7.98s/it]Capture des données de l'année 2015
```

# 🧪 Données

_BDD_
| Colonne | Description | Type |
| ----------- | ------------------------------------------------------------ | ------ |
| `Date` | Date du tirage | pd.datetime |
| `Gagnant` | Nombre de gagnants lors du tirage | int |
| `Jackpot` | Montant de la cagnote | string |
| `n1, n2, etc` | Numéros du tirage | int |
| `e1, e2` | Etoiles du tirage | int |

# 🏙️ Environnement virtuel UV

1. Installer UV sur l'ensemble du système macOS ou Linux (vérifier via `uv self version`): `curl -LsSf https://astral.sh/uv/install.sh | sudo sh`
   Sortie: `uv 0.8.22 (ade2bdbd2 2025-09-23)`
2. Créer un nouveau projet: `uv init $PROJECT_NAME`
3. Commandes:
   Ajouter des dépendances: `uv add $PACKAGE`
   Retirer des dépendances: `uv remove $PACKAGE`
   Lancer un script: `uv run $SCRIPT.py`
   Exporter un fichier 'requirements.txt': `uv export -o requirements.txt`

# 🚀 Roadmap (idées)

...

## 📬 Contact

[![GitHub](https://img.shields.io/badge/2FromField-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/2FromField)
[![Linkedin](https://img.shields.io/badge/LinkedIn:_BRUNO_Joey-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](www.linkedin.com/in/joey-bruno-076390223)
