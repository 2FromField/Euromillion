# Pipeline Euromillion

Répertoire permettant d'estimer le prochain tirage de l'euromillion en se basant sur la fréquence de tirage des numéros et des étoiles.

## Data

- ./euromillions.csv : historique des tirages depuis 2004

## Scripts

- ./scrap.py : fichier permettant le scrapping des données sur la page : https://www.tirage-euromillions.net pour chaque année
- ./analysis.ipynb : notebook jupyter permettant d'analyser les probabilités du prochain tirage.

## Lancer le scrapping

`python ./Euromillion/scripts/scrap.py`

Exemple de sortie:

```
Récupération des données...:  43%|██████████████████████████████████████████████                                                            | 10/23 [01:01<01:38,  7.60s/it]Capture des données de l'année 2014
Récupération des données...:  48%|██████████████████████████████████████████████████▋                                                       | 11/23 [01:10<01:35,  7.98s/it]Capture des données de l'année 2015
```

## Dépendances

[![Pandas](https://img.shields.io/badge/Pandas%20v2.3.0-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)](https://pypi.org/project/pandas/)
[![Selenium](https://img.shields.io/badge/Selenium%20v4.34.0-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)](https://pypi.org/project/selenium/)
[![Numpy](https://img.shields.io/badge/Numpy%20v2.2.6-777BB4?style=for-the-badge&logo=numpy&logoColor=white)](https://pypi.org/project/numpy/)

## Environnement virtuel

`python -m venv venv` # Créer un environnement virtuel nommé "venv" <br>
`source venv/bin/activate` # Activer l'environnement virtuel <br>
`pip install -r requirements.txt` # Installer les dépendances dans le venv
`deactivate` # Désactiver l'environnement virtuel <br>
`pip freeze > requirements.txt` # Dépendances <br>

# Application VueJS

## Création et configuration de l'application VueJS

1. Installer Node : `brew install node`
2. Créer un projet : `npm create vite@latest` en séléctionnant "Vue" & "TypeScript"
3. Accéder au dossier courant de l'app : `cd euromillion_app`
4. Installer les dépendances : `npm install`
5. Lancer le serveur de dev : `npm run dev`
6. Accéder au localhost : `http://localhost:5173/`

## Architecutre

```
Euromillion/
├── 📁 euromillion_app
│   ├── 📁 public
│   │   └── 🖼️ vite.svg
│   ├── 📁 src
│   │   ├── 📁 assets
│   │   │   └── 🖼️ vue.svg
│   │   ├── 📁 components
│   │   │   └── 📄 HelloWorld.vue
│   │   ├── 📁 data
│   │   │   └── 📄 euromillion.csv
│   │   ├── 📄 App.vue
│   │   ├── 📄 main.ts
│   │   ├── 🎨 style.css
│   │   └── 📄 vite-env.d.ts
│   ├── ⚙️ .gitignore
│   ├── 📝 README.md
│   ├── 🌐 index.html
│   ├── ⚙️ package-lock.json
│   ├── ⚙️ package.json
│   ├── ⚙️ tsconfig.app.json
│   ├── ⚙️ tsconfig.json
│   ├── ⚙️ tsconfig.node.json
│   └── 📄 vite.config.ts
├── 📁 logs
├── 📁 scripts
│   ├── 📄 analysis.ipynb
│   ├── 📄 new.csv
│   └── 🐍 scrap.py
├── ⚙️ .gitignore
├── 📝 README.md
├── ⚙️ package-lock.json
├── ⚙️ package.json
└── 📄 requirements.txt
```
