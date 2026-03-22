import bcrypt

def hash_master_password(password: str) -> bytes:
    """Hash le password maître avec bcrypt. Retourne le hash en bytes"""
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())

def verify_master_password(password: str, hashed: bytes) -> bool:
    """Verifie que le password maître et le hash corresponde. Retourne un bool"""
    password_bytes = password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed)