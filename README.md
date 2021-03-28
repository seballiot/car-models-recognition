# Projet de classification de voiture à l'aide du Deep Learning

L'objectif de ce projet est de réaliser un réseau de neuronnes capable de détecter des marques/modèles de véhicules à partir d'images, dans son ensemble jusqu’à sa mise en production.

### Groupe 1

- REGGIANI Eléa
- AMROUCHE Belkacem
- ALLIOT Sébastien
- BENKANIA Mustapha
- DANI Sofian

### Jeu de données

- Stanford Cars Dataset : https://ai.stanford.edu/~jkrause/cars/car_dataset.html

### Accès à l'application déployée

- Heroku : TODO

### Composition du repository

- `deep_learning_scripts/` : Dossier contenant les scripts de nettoyage, analyse et modélisation + images croppés
- Les autres dossiers/fichiers composent l'application web Flask

### Technologies utilisées

- Framework Python : **Flask**
- Base de données : **SQLite**
- Déploiement : **Heroku**

### Running de l'application Web en local

- Télécharger le projet en local, puis se placer à la racine du projet
- Création d'un "virtual environment"
```
python3 -m venv venv-cars
# Si python3 non reconnu, essayer avec 'python'
```
- On rentre dans l'environnement virtuel
```
#  Sur Unix et MacOS
source venv-cars/bin/activate

# Sur Windows
venv-cars\Scripts\activate.bat
```
- Mise à jour pip
```
pip install --upgrade pip
```
- Installation des dépendances (dans le virtual env)
```
pip install -r requirements.txt
```
- Variables globales
```
#  Sur Unix et MacOS
export FLASK_APP=projectapp.py
export FLASK_ENV=development

# Sur Windows
set FLASK_APP=projectapp.py
set FLASK_ENV=development
```
- Running du projet
```
flask run
```
NB : kill le serveur + sortir de l'environnement virtuel 
```
$ 'CTRL C'

$ deactivate
```