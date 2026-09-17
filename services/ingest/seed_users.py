"""
Cria os usuários iniciais do CRQ-V para fiscalização e atendimento à exigência
de múltiplos acessos simultâneos (TR itens 1.2.3.4 e 4.2.4).
"""

from sqlalchemy.orm import Session
from apps.api.models.user import User
from apps.api.core.security import get_password_hash

def seed_users(db: Session):
    default_users = [
        {
            "email": "fiscal1@crqv.org.br",
            "password": "crqv@fiscal2026",
            "full_name": "Agente Fiscal CRQ-V (Posto 01)",
            "role": "fiscal"
        },
        {
            "email": "fiscal2@crqv.org.br",
            "password": "crqv@fiscal2026",
            "full_name": "Agente Fiscal CRQ-V (Posto 02)",
            "role": "fiscal"
        },
        {
            "email": "gestor@crqv.org.br",
            "password": "crqv@gestor2026",
            "full_name": "Gestor de Fiscalização e Autuação",
            "role": "gestor"
        },
        {
            "email": "admin@crqv.org.br",
            "password": "admin@crqv2026",
            "full_name": "Administrador do Sistema CRQ-V",
            "role": "admin"
        }
    ]

    count = 0
    for u in default_users:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            user = User(
                email=u["email"],
                hashed_password=get_password_hash(u["password"]),
                full_name=u["full_name"],
                role=u["role"],
                is_active=True
            )
            db.add(user)
            count += 1

    db.commit()
    print(f"[Seed] {count} usuários do CRQ-V cadastrados.")
