import storage


def add_vault(filepath: str, site: str, login: str, password: str, key: bytes) -> bool:
    """Créer une entrée dans le filepath avec le site, login et password. Retourne faux si le site est deja dans le filepath"""
    data = storage.load_vault(filepath, key)

    if site not in data:
        data[site] = {"login": login, "password": password}
        storage.save_vault(filepath, key, data)
        return True
    
    return False


def get_vault(filepath: str, site: str, key: bytes) -> dict | None:
    """Renvoie le login et password du site voulue, retourne None si il n'est pas dans le filepath"""
    data = storage.load_vault(filepath, key)
    if site in data:
        return data[site]

    return None


def list_vault(filepath: str, key: bytes) -> dict:
    """Renvoie le filepath complet sous forme de dictionnaire"""
    return storage.load_vault(filepath, key)


def delete_vault(filepath: str, site: str, key: bytes) -> bool:
    """Supprime un site voulu dans le filepath. Retourne faux si le site n'est pas dans le filepath"""
    data = storage.load_vault(filepath, key)
    if site in data:
        del data[site]
        storage.save_vault(filepath, key, data)
        return True
    
    return False