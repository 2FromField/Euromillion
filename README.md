# Euromillion

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
`deactivate` # Désactiver l'environnement virtuel <br>
`pip freeze>requirements.txt` # Lister les dépendances nécessaires dans un fichier "requirements.txt" <br>
