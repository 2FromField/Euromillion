# Euromillion

Répertoire permettant d'estimer le prochain tirage de l'euromillion en se basant sur la fréquence de tirage des numéros et des étoiles.

## Data

- ./euromillions.csv : historique des tirages depuis 2004

## Scripts

- ./scrap.py : fichier permettant le scrapping des données sur la page : https://www.tirage-euromillions.net pour chaque année
- ./analysis.ipynb : notebook jupyter permettant d'analyser les probabilités du prochain tirage.

## Lancer le scrapping

`/Users/joeybruno/Desktop/GITHUB/Euromillion/venv/bin/python /Users/joeybruno/Desktop/GITHUB/Euromillion/scripts/Scrap.py`

## Environnement virtuel

`python -m venv venv` # Créer un environnement virtuel nommé "venv" <br>
`source venv/bin/activate` # Activer l'environnement virtuel <br>
`deactivate` # Désactiver l'environnement virtuel <br>
`pip freeze>requirements.txt` # Lister les dépendances nécessaires dans un fichier "requirements.txt" <br>
