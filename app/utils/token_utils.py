import secrets

def generate_api_token() -> str:
    return secrets.token_hex(32)