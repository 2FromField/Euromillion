# Pipeline Euromillion

Répertoire permettant d'estimer le prochain tirage de l'euromillion en se basant sur la fréquence de tirage des numéros et des étoiles.

## Data

- ./euromillions.csv : historique des tirages depuis 2004

## Scripts

- ./scrap.py : fichier permettant le scrapping des données sur la page : https://www.tirage-euromillions.net pour chaque année
- ./analysis.ipynb : notebook jupyter permettant d'analyser les probabilités du prochain tirage.

## Lancer le scrapping

`python ./Euromillion/scripts/scrap.py`

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

mon-app-vue/
├── node_modules/ # Contient les packages installés (jamais versionner dans Git) <br>
├── public/ # Fichiers statistiques (ex: images, favicon, manifest) <br>
├── src/ # Coeur de l'application<br>
│ ├── assets/ Dossier pour images, polices, SVG, etc<br>
│ ├── App.vue # Composant racine<br>
│ └── main.js # Point d'entrée de l'appliation<br>
├── .gitignore # Fichiers que doit ignorer Git<br>
├── index.html # Seul fichier HTML définissant app<br>
├── package.json # Contient le nom du projet / dépendances / scripts<br>
├── vite.config.js # Fichier de configuration de Vite<br>
└── README.md # Documentation du projet<br>
