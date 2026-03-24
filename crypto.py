from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode

def derive_key(password: str, salt: bytes) -> bytes:
    """Dérive une clé de Fernet (32 bytes) à partir du master password et d'un salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )

    password_bytes = password.encode("utf-8")
    key = kdf.derive(password_bytes)
    #Fernet attend 32 bytes en base64 URL-safe
    return urlsafe_b64encode(key)


def encrypt(data: bytes, key: bytes) -> bytes:
    """Chiffre une data à partir de la clé de Fernet"""
    f = Fernet(key)
    return f.encrypt(data)


def decrypt(data: bytes, key: bytes) -> bytes:
    """Déchiffre une data à partir de la clé de Fernet"""
    f = Fernet(key)
    return f.decrypt(data)