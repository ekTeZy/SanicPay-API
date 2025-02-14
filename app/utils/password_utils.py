import re
import bcrypt

def validate_password(password: str, min_length=6, max_length=16) -> bool:
    if not (min_length <= len(password) <= max_length):
        raise Exception({"error": "Password length must be between 6 and 16 characters"})

    if not re.search(r"[A-Za-z]", password):
        raise Exception({"error": "Password must contain at least one letter"})

    if not re.search(r"\d", password):
        raise Exception({"error": "Password must contain at least one digit"})

    if " " in password:
        raise Exception({"error": "Password must not contain spaces"})

    return True

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
