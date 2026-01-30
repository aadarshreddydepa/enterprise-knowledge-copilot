from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from datetime import datetime, timedelta
from pathlib import Path

_password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        _password_hasher.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False

PRIVATE_KEY = Path("keys/private.pem").read_text()
PUBLIC_KEY = Path("keys/public.pem").read_text()

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "exp": expire,
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])

