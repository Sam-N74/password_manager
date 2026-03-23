import getpass
import argparse
import os
import vault
import auth
import crypto

#Constantes
VAULT_PATH = "vault.enc"
SALT_PATH = "salt.bin"
HASH_PATH = "master.hash"


def init_vault() -> None:
    """Initialise le CLI en créant et stockant le salt et le Master Password (uniquement si le vault n'existe pas deja)"""
    if os.path.exists(HASH_PATH):
        print("Attention le CLI a deja été initialisé !\n")
        return None
    password = getpass.getpass("Master Password: ")

    salt = os.urandom(16)
    with open(SALT_PATH, 'wb') as f:
        f.write(salt)

    hashed = auth.hash_master_password(password)
    with open(HASH_PATH, 'wb') as f:
        f.write(hashed)


def verify_vault() -> bytes | None:
    """Renvoie la clé de Fernet à partir du Master Password, si il est correct. Retourne None sinon (après 3 échecs)"""
    with open(SALT_PATH, 'rb') as f:
        salt = f.read()
    with open(HASH_PATH, 'rb') as f:
         hashed = f.read()

    for i in range (3):
        password = getpass.getpass("Master Password: ")
        print("\n")
        if (not auth.verify_master_password(password, hashed)):
            print(f"Master Password incorrect, {2 - i} tentative(s) restante(s).")
        else:
            print("Master Password correct \n")
            return crypto.derive_key(password, salt)
    return None


def cmd_add(site: str, login: str, password: str) -> None:
    """Commande add de vault.py"""
    key = verify_vault()
    if key is None:
        print("Clé incorrect.\n")
        return
    
    if vault.add_vault(VAULT_PATH, site, login, password, key):
        print("Enregistrement effectué.\n")
    else:
        print("Erreur, site deja présent.\n")
    return


def cmd_get(site: str) -> None:
    """Commande get de vault.py"""
    key = verify_vault()
    if key is None:
        print("Clé incorrect.\n")
        return
    
    entry = vault.get_vault(VAULT_PATH, site, key)

    if entry is None:
        print("Le site n'est pas enregistré.\n")
        adding = None

        while (adding != "o" and adding != "n"):
            adding = input("Voulez-vous l'enregistrer ? (o/n): ")

            if (adding == "o"):
                login = input("Login: ")
                password = input("Password: ")
                if vault.add_vault(VAULT_PATH, site, login, password, key):
                    print("Enregistrement effectué.\n")
                else:
                    print("Erreur, site deja présent.\n")
                    return
                return
            
            elif (adding == "n"):
                return
            
    print(f"Login: {entry['login']}\nPassword: {entry['password']}\n")
    

def cmd_list() -> None:
    """Commande list de vault.py"""
    key = verify_vault()
    if key is None:
        print("Clé incorrect.\n")
        return
    
    entry = vault.list_vault(VAULT_PATH, key)

    for site in entry:
        print(f"Site: {site}\nLogin: {entry[site]['login']}\nPassword: {entry[site]['password']}")
    

def cmd_delete(site: str) -> None:
    """Commande delete de vault.py"""
    key = verify_vault()
    if key is None:
        print("Clé incorrect.\n")
        return
    
    if vault.delete_vault(VAULT_PATH, site, key):
        print("Effacement effectué.\n")
    else:
        print("Le site n'est pas présent.\n")
    return
    

def main():
    parser = argparse.ArgumentParser(description="Gestionnaire de Mot de passe.")
    subparsers = parser.add_subparsers(dest="cmd")

    #Commande init
    parser_init = subparsers.add_parser("init", help="Initialise le Gestionnaire de Mot de passe")

    #Commande add
    parser_add = subparsers.add_parser("add", help="Ajouter un site")
    parser_add.add_argument("site")
    parser_add.add_argument("login")
    parser_add.add_argument("password")

    #Commande get
    parser_get = subparsers.add_parser("get", help="Afficher les informations d'un site")
    parser_get.add_argument("site")

    #Commande list
    parser_list = subparsers.add_parser("list", help="Liste tous sites avec login et mot de passe")
    
    #Commande delete
    parser_delete = subparsers.add_parser("delete", help="Supprime l'entrée pour le site voulu")
    parser_delete.add_argument("site")

    args = parser.parse_args()

    if args.cmd == "init":
        init_vault()
    elif args.cmd == "add":
        cmd_add(args.site, args.login, args.password)
    elif args.cmd == "get":
        cmd_get(args.site)
    elif args.cmd == "list":
        cmd_list()
    elif args.cmd == "delete":
        cmd_delete(args.site)
    else:
        print("Commande introuvable.\n")

    return


if __name__ == "__main__":
      main() 