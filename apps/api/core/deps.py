from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from apps.api.core.config import settings
from apps.api.core.database import get_db
from apps.api.models.user import User
from apps.api.models.audit_log import AuditLog
from apps.api.core.security import register_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")

def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou sessão expirada",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None or not user.is_active:
        raise credentials_exception

    # Registra atividade da sessão simultânea
    client_ip = request.client.host if request.client else "127.0.0.1"
    register_session(user.id, user.email, client_ip)

    return user

from apps.api.engine.audit_sink import audit_sink, AuditEvent

def record_audit(
    db: Session,
    action: str,
    user: User = None,
    target_type: str = None,
    target_id: str = None,
    details: dict = None,
    ip_address: str = "127.0.0.1"
):
    """Registra evento de auditoria conforme governança, LGPD e SPEC-0022 (HeraclitusDB)."""
    event = AuditEvent(
        event_type=action,
        actor_id=str(user.id) if user else "anonymous",
        actor_role=user.role if user else "anonymous",
        entity_type=target_type or "system",
        entity_id=target_id or action,
        payload=details or {},
        ip_address=ip_address,
        tenant_id=settings.HERACLITUS_TENANT,
        software_release="1.0.0"
    )
    audit_sink.append(event, db=db)

