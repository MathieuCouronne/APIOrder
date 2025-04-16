# Utilisation d'une image de base avec Python
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 5000 pour Flask
EXPOSE 5000

# Commande pour lancer l'application Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
