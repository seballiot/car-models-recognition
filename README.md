# Projet de classification de voiture à l'aide du Deep Learning

L'objectif de ce projet est de réaliser un réseau de neuronnes capable de détecter des marques/modèles de véhicules à partir d'images, dans son ensemble jusqu’à sa mise en production.

Dataset : Stanford Cars Dataset

### Composition du groupe

- REGGIANI Eléa
- ALLIOT Sébastien
- AMROUCHE Belkacem
- BENKANIA Mustapha
- DANI Sofian

### Organisation du repository

- `deep_learning_scripts/` : Dossier contenant les scripts de nettoyage, analyse et modélisation + images croppés
- `flask_web_app` : application web Flask

### Preview

![](/screen_import.png)
![](/screen_analyse.png)

### Technologies utilisées

- Framework Python : **Flask**
- Base de données : **SQLite**
- Env : **Docker**
- Deep learning : **InceptionV3 model**

### Running de l'application Web en local

Prérequis : Docker est installé
- Build de l'image
```
docker build --tag car-classification .
```
- Run (ajuster le port si besoin)
```
docker run -p 5066:5000 car-classification
```
- Go to http://localhost:5066/