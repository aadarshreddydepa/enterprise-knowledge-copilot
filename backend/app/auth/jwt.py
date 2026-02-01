
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(subject: str, expires_minutes: int = 30) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {
        "sub": subject,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload.get("sub")
    except JWTError:
        return None
