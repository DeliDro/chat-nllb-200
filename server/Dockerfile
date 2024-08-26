# Création d'une image de base avec toutes les dépendances nécessaires pour lancer le projet
# On utilise une image légère de Python
FROM python:3.12-slim as base

# Copie du fichier décrivant les dépendances dans le conteneur
COPY ./requirements.txt /requirements.txt

# Installation des dépendances dans le conteneur
RUN pip install --no-cache-dir -r requirements.txt

# Utilisation de l'image avec les dépendances
FROM base

# Copie du code de l'application dans le conteneur
COPY ./app /app

RUN mkdir /sql /images

# Démarrage du conteneur
CMD ["fastapi", "run", "app/main.py", "--port", "5000"]