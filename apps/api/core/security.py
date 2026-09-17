from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from jose import JWTError, jwt
import bcrypt
from apps.api.core.config import settings

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Tracker de sessões simultâneas (Garantia do TR item 1.2.3.4 / TR-007)
active_sessions: Dict[str, dict] = {}

def register_session(user_id: int, user_email: str, ip_address: str = "127.0.0.1"):
    now = datetime.now(timezone.utc)
    # Limpa sessões com mais de 2 horas de inatividade
    expired = [k for k, v in active_sessions.items() if (now - v["last_activity"]).total_seconds() > 7200]
    for k in expired:
        active_sessions.pop(k, None)
    
    session_key = f"{user_id}_{ip_address}"
    active_sessions[session_key] = {
        "user_id": user_id,
        "email": user_email,
        "ip_address": ip_address,
        "last_activity": now
    }

def get_active_sessions_count() -> int:
    return len(active_sessions)
