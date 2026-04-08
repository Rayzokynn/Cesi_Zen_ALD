 CESIZen - Guide d'Installation
 Description
CESIZen est une application mobile et web de gestion de la santé mentale développée pour le Ministère de la Santé et de la Prévention. L'écosystème repose sur une architecture découplée avec un backend sous Django et un frontend mobile sous Ionic.

 Prérequis
Avant de procéder à l'installation, assurez-vous de disposer des outils suivants :

Python 3.12+

Node.js (LTS) & NPM

Ionic CLI (npm install -g @ionic/cli)

Git

 Installation du Projet
1. Récupération des sources
Clonez le dépôt officiel du projet :

Bash
git clone [LIEN_VERS_VOTRE_REPO_ICI]
cd cesizen
2. Configuration du Backend (Django)
Le backend gère la logique métier et fournit une API REST sécurisée via Django REST Framework.

Accédez au répertoire : cd backend

Créez un environnement virtuel : python -m venv venv

Activez l'environnement :

Linux/Mac : source venv/bin/activate

Windows : venv\Scripts\activate

Installez les dépendances : pip install -r requirements.txt

Initialisez la base de données (SQLite par défaut en dev) : python manage.py migrate

Lancez le serveur : python manage.py runserver 0.0.0.0:8000

3. Configuration du Frontend (Ionic)
L'interface est développée avec Ionic/Angular selon une approche Mobile First.

Accédez au répertoire : cd frontend

Installez les modules : npm install

Configurez l'API : Modifiez src/environments/environment.ts pour renseigner l'adresse IP de votre serveur.

Lancez l'application : ionic serve

 Déploiement Mobile
Pour tester l'application sur un appareil mobile ou un émulateur via Capacitor :

Ajoutez la plateforme Android : ionic cap add android

Copiez les ressources : ionic cap copy

Ouvrez dans Android Studio : ionic cap open android

 Base de données
Le projet utilise SQLite pour faciliter le développement rapide, mais est configuré pour supporter MySQL 8.0 en production.

Pour passer sur MySQL, créez une base de données cesizen et modifiez le dictionnaire DATABASES dans settings.py.

 Sécurité et Conformité
RGPD : Le projet respecte le principe de Privacy by Design.

Authentification : Utilisation de jetons JWT et hachage Argon2id (ou PBKDF2) pour les identifiants.

Accessibilité : Conformité au niveau AA du RGAA 4.1.
