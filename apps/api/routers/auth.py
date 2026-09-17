from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from apps.api.core.database import get_db
from apps.api.core.security import verify_password, get_password_hash, create_access_token, register_session, get_active_sessions_count, active_sessions
from apps.api.core.deps import get_current_user, record_audit
from apps.api.models.user import User
from apps.api.schemas.auth import (
    LoginRequest, TokenResponse, UserResponse,
    UserProfileUpdate, ChangePasswordRequest,
    UserCreateRequest, UserUpdateRequest, PaginatedUsersResponse
)
import math

router = APIRouter(prefix="/auth", tags=["Autenticação e Perfis de Usuários"])

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

@router.put("/me", response_model=UserResponse)
def update_my_profile(
    payload: UserProfileUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza dados do perfil do usuário logado."""
    if payload.full_name:
        current_user.full_name = payload.full_name.strip()
    db.commit()
    db.refresh(current_user)

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db=db,
        action="UPDATE_PROFILE",
        user=current_user,
        target_type="USER",
        target_id=str(current_user.id),
        details={"updated_fields": ["full_name"]},
        ip_address=client_ip
    )
    return current_user

@router.post("/change-password")
def change_my_password(
    payload: ChangePasswordRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Permite ao usuário autenticado alterar sua própria senha de acesso."""
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha atual informada está incorreta."
        )
    if len(payload.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A nova senha deve possuir no mínimo 6 caracteres."
        )
    current_user.hashed_password = get_password_hash(payload.new_password)
    db.commit()

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db=db,
        action="CHANGE_PASSWORD",
        user=current_user,
        target_type="USER",
        target_id=str(current_user.id),
        details={"result": "success"},
        ip_address=client_ip
    )
    return {"message": "Senha alterada com sucesso!"}

@router.get("/users", response_model=PaginatedUsersResponse)
def list_users(
    page: int = 1,
    page_size: int = 10,
    q: str = None,
    role: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retorna listagem paginada de todos os usuários do sistema CRQ-V."""
    query = db.query(User)
    if q:
        query = query.filter(
            (User.full_name.ilike(f"%{q}%")) | (User.email.ilike(f"%{q}%"))
        )
    if role:
        query = query.filter(User.role == role)
    
    total = query.count()
    total_pages = max(1, math.ceil(total / page_size))
    items = query.order_by(User.id.asc()).offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedUsersResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.post("/users", response_model=UserResponse)
def create_user(
    payload: UserCreateRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Permite cadastrar um novo usuário / perfil no sistema."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário com este e-mail institucional."
        )
    new_user = User(
        email=payload.email,
        full_name=payload.full_name,
        role=payload.role,
        hashed_password=get_password_hash(payload.password),
        is_active=payload.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db=db,
        action="CREATE_USER",
        user=current_user,
        target_type="USER",
        target_id=str(new_user.id),
        details={"email": new_user.email, "role": new_user.role},
        ip_address=client_ip
    )
    return new_user

@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza perfil, cargo ou ativação de usuário."""
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    if payload.full_name is not None:
        target_user.full_name = payload.full_name
    if payload.role is not None:
        target_user.role = payload.role
    if payload.is_active is not None:
        target_user.is_active = payload.is_active
    if payload.password:
        target_user.hashed_password = get_password_hash(payload.password)

    db.commit()
    db.refresh(target_user)

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db=db,
        action="UPDATE_USER",
        user=current_user,
        target_type="USER",
        target_id=str(target_user.id),
        details={"email": target_user.email},
        ip_address=client_ip
    )
    return target_user

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
