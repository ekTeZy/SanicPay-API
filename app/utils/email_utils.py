import re
def validate_email(email: str) -> bool:
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    else:
        raise Exception({"error": "Invalid email"})
