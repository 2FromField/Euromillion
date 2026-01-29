# Projet BeMillionnaire

![Pandas](https://img.shields.io/badge/Pandas%20v2.3.0-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium%20v4.34.0-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)
![Numpy](https://img.shields.io/badge/Numpy%20v2.2.6-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![Github Pages](https://img.shields.io/badge/GitHub%20Pages-222222?style=for-the-badge&logo=github%20Pages&logoColor=white)
![Excel](https://img.shields.io/badge/Microsoft_CSV-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)

## Présentation

Projet visant à récupérer les données depuis le site internet open-source https://www.tirage-euromillions.net/ et à les restructurer pour en tirer profit au sein d'une application.<br>
L'application "BeMillionnaire" vient quant à elle appeller ces mêmes données pour permettre aux différents utilisateurs de concevoir leurs prochains pronostics tout en ayant la transparence des résultats antérieurs.

## Architecutre

```
Euromillion/
├── 📁 .github
│   └── 📁 workflows
│       └── ⚙️ daily-update.yml             # Fichier d'automatisation via GithHub Pages
├── 📁 euromillion_app
│   ├── 📁 public
│   │   └── 🖼️ vite.svg
│   ├── 📁 src
│   │   ├── 📁 assets
│   │   │   └── 🖼️ vue.svg
│   │   ├── 📁 components
│   │   │   └── 📄 HelloWorld.vue
│   │   ├── 📁 data
│   │   │   └── 📄 euromillion.csv          # Base de données
│   │   ├── 📄 App.vue                      # Application VueJS
│   │   ├── 📄 main.ts
│   │   ├── 🎨 style.css                    # Style CSS de l'app
│   │   └── 📄 vite-env.d.ts
│   ├── ⚙️ .gitignore                       # Exclusion git de l'app
│   ├── 🌐 index.html
│   ├── ⚙️ package-lock.json
│   ├── ⚙️ package.json
│   ├── ⚙️ tsconfig.app.json
│   ├── ⚙️ tsconfig.json
│   ├── ⚙️ tsconfig.node.json
│   └── 📄 vite.config.ts
├── 📁 logs
│   └── 📄 scrap.log                        # Fichier de centralisation des logs
├── 📁 scripts
│   ├── 📄 analysis.ipynb                   # Analyses ponctuelles
│   └── 🐍 scrap.py                         # Script de scrapping des données
├── ⚙️ .gitignore                           # Exclusion git
├── 📝 README.md                            # Documentation du projet
├── ⚙️ package-lock.json
├── ⚙️ package.json
└── 📄 requirements.txt                     # Dépendances du projet
```

## Lancer le scrapping

`python ./Euromillion/scripts/scrap.py`

Exemple de sortie:

```
Récupération des données...:  43%|██████████████████████████████████████████████                                                            | 10/23 [01:01<01:38,  7.60s/it]Capture des données de l'année 2014
Récupération des données...:  48%|██████████████████████████████████████████████████▋                                                       | 11/23 [01:10<01:35,  7.98s/it]Capture des données de l'année 2015
```

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

## 📬 Contact

[![GitHub](https://img.shields.io/badge/2FromField-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/2FromField)
[![Linkedin](https://img.shields.io/badge/LinkedIn:_BRUNO_Joey-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](www.linkedin.com/in/joey-bruno-076390223)
