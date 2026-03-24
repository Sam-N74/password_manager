# Gestionnaire de Mot de passe CLI

## Description :

Ce projet est un Gestionnaire de Mot de passe codé entièrement en Python.  
Il fonctionne au travers de la console (CLI) et permet de sauvegarder et d'accéder à ses logins/mots de passe pour les sites voulus, à l'aide de commandes (décrites plus bas).

## Stack Technique :

### Les bibliothèques utilisées sont :

**bcrypt**, qui permet de hasher un Master Password choisi par l'utilisateur et de vérifier sa correspondance.  

**cryptography**, qui permet de dériver une clé de Fernet à partir du Master password et d'un Salt, et de chiffrer/déchiffrer des données.

## Installation :

```bash
git clone https://github.com/Sam-N74/password_manager.git
cd password_manager
python -m venv .venv 
.venv\Scripts\activate #source .venv/bin/activate (Linux/MacOS)
pip install -r requirements.txt
```

## Usage :

### Commandes :
init : initialise le Gestionnaire (à faire avant toutes les autres)
```python
python main.py init
```

reset : réinitialise le Gestionnaire (suppression de toutes les données !)
```python
python main.py reset
```

change_password : permet de changer le Master Password
```python
python main.py change_password
```

add : permet d'ajouter une entrée dans le Gestionnaire avec le site, login et mot de passe
```python
python main.py add <Site> <Login> <Mot_de_Passe>
```

get : permet d'afficher les informations de connexion d'un site en particulier
```python
python main.py get <Site>
```

list : Affiche toutes les informations enregistrées dans le Gestionnaire
```python
python main.py list
```

delete : permet de supprimer une entrée dans le Gestionnaire pour un site voulu
```python
python main.py delete <Site>
```

## Security Design

Le Master Password est hashé grâce à bcrypt en utilisant un salt aléatoire et stocké dans master.hash.  
Pour chiffrer/déchiffrer les données, le Master Password est dérivé en une clé de Fernet de 32 bytes en utilisant la fonction de dérivation PBKDF2 avec 600 000 itérations et un salt fixe stocké dans salt.bin.  
Toutes les données de l'utilisateur seront stockées de manière chiffrée dans vault.enc en utilisant la clé de Fernet.

**bcrypt vs SHA256 :** bcrypt est intentionnellement lent grâce à son coût calculatoire configurable (12 par défaut pour bcrypt.gensalt()), ce qui rend le bruteforce complexe. SHA256 est trop rapide, un attaquant peut tester des milliards de combinaisons par seconde.  
**600 000 itérations :** recommandation OWASP 2023 pour PBKDF2-SHA256. Ralentit volontairement le calcul (comme bcrypt) pour éviter le bruteforce.  
**Fernet :** schéma de chiffrement authentifié, garantit la confidentialité (chiffrement) et l'intégrité : si quelqu'un falsifie vault.enc, le déchiffrement échoue au lieu de retourner des données corrompues sans message d'erreur.

