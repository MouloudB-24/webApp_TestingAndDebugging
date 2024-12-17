# Projet
## Améliorer une application Web python par des tests et du débugge

# Installation

1. Clone le dépôt : git@github.com:MouloudB-24/webApp_TestingAndDebugging.git

2. Installez les dépendances : pip install -r requirements.txt

3. Configurez les variables d'environnement : cp env.example .env


Ensuite ouvrez le fichier .env et mettez à jour les variables:
- Pour générer une nouvelle SECRET_KEY, utilisez cette commande: python -c "import secrets; print(secrets.token_hex(16))"
- Copiez la clé générée et collez la dans votre fichier .env


Exemple de contenu final de .env : FLASK_SECRET_KEY=1234567890abcdef1234567890abcdef







