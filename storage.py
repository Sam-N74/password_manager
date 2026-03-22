import crypto
import json

def load_vault(filepath: str, key: bytes) -> dict:
    """Récupère le vault json chiffré et le retourne en dictionnaire déchiffré"""
    #'rb' pour lire des bytes
    try:
        with open(filepath, 'rb') as f:
            json_encrypt = f.read()
    except FileNotFoundError:
        return {} 
    #si vault n'existe pas on renvoie un dictionnaire vide
    
    json_bytes = crypto.decrypt(json_encrypt, key)
    dict_json = json_bytes.decode("utf-8", errors="strict")
    data = json.loads(dict_json)

    return data


def save_vault(filepath: str, key: bytes, data: dict) -> None:
    """Réécris le vault json chiffré à partir du dictionnaire de data complet"""
    dict_json = json.dumps(data)
    json_bytes = dict_json.encode("utf-8")
    json_encrypt = crypto.encrypt(json_bytes, key)

    #'wb' pour écrire des bytes
    with open(filepath, 'wb') as f: 
        f.write(json_encrypt)
