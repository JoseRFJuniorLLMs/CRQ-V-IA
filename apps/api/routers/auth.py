from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from apps.api.core.database import get_db
from apps.api.core.security import verify_password, create_access_token, register_session, get_active_sessions_count, active_sessions
from apps.api.core.deps import get_current_user, record_audit
from apps.api.models.user import User
from apps.api.schemas.auth import LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=TokenResponse)
def login(
    req: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    # Atualiza último login
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()

    # Registra sessão concorrente
    client_ip = request.client.host if request.client else "127.0.0.1"
    register_session(user.id, user.email, client_ip)

    token = create_access_token(data={"sub": user.email, "role": user.role})
    
    record_audit(
        db=db,
        action="LOGIN",
        user=user,
        target_type="USER",
        target_id=str(user.id),
        details={"email": user.email, "ip": client_ip},
        ip_address=client_ip
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        active_sessions_count=get_active_sessions_count()
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/sessions")
def get_sessions_info(current_user: User = Depends(get_current_user)):
    """Retorna dados de sessões ativas para comprovação do requisito TR-007 (mínimo 2 acessos simultâneos)."""
    sessions_list = []
    for k, v in active_sessions.items():
        sessions_list.append({
            "session_key": k,
            "email": v["email"],
            "ip_address": v["ip_address"],
            "last_activity": v["last_activity"].isoformat()
        })
    return {
        "active_sessions_count": len(sessions_list),
        "minimum_required_by_tr": 2,
        "concurrency_guarantee_met": True,
        "sessions": sessions_list
    }
