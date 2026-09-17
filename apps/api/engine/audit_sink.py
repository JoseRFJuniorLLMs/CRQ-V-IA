"""
Módulo de Auditoria e Event Store Imutável (SPEC-0022).
Implementa o padrão AuditSink com suporte a gravação dupla (dual-write/shadow)
entre a base relacional operacional e o HeraclitusDB como event store append-only.
"""

import json
import hashlib
import uuid
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import httpx
from sqlalchemy.orm import Session

from apps.api.core.config import settings
from apps.api.models.audit_log import AuditLog

logger = logging.getLogger("audit_sink")

class AuditEvent:
    """Envelope canônico do evento de auditoria e evidência (SPEC-0022 §6)."""
    def __init__(
        self,
        event_type: str,
        actor_id: Optional[str] = None,
        actor_role: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
        ip_address: str = "127.0.0.1",
        tenant_id: str = "crq-v",
        software_release: str = "1.0.0",
        correlation_id: Optional[str] = None,
        event_id: Optional[str] = None,
        occurred_at: Optional[str] = None
    ):
        self.event_id = event_id or str(uuid.uuid4())
        self.tenant_id = tenant_id
        self.event_type = event_type
        self.actor_id = actor_id
        self.actor_role = actor_role
        self.entity_type = entity_type or "system"
        self.entity_id = entity_id or self.event_id
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.software_release = software_release
        self.occurred_at = occurred_at or datetime.now(timezone.utc).isoformat()
        self.payload = payload or {}
        self.ip_address = ip_address

        # Hash canônico SHA-256 do payload para garantia criptográfica de integridade (SPEC-0022 §46)
        canonical_bytes = json.dumps(self.payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
        self.payload_hash = hashlib.sha256(canonical_bytes).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "tenant_id": self.tenant_id,
            "event_type": self.event_type,
            "actor_id": self.actor_id,
            "actor_role": self.actor_role,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "correlation_id": self.correlation_id,
            "software_release": self.software_release,
            "occurred_at": self.occurred_at,
            "ip_address": self.ip_address,
            "payload": self.payload,
            "payload_hash": self.payload_hash
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


class AuditSink:
    """Interface abstrata para armazenamento de auditoria (SPEC-0022 §12)."""
    def append(self, event: AuditEvent, db: Optional[Session] = None) -> bool:
        raise NotImplementedError


class RelationalAuditSink(AuditSink):
    """Gravação na tabela operacional relacional (PostgreSQL / SQLite)."""
    def append(self, event: AuditEvent, db: Optional[Session] = None) -> bool:
        if db is None:
            return False
        try:
            user_id = None
            if event.actor_id and event.actor_id.isdigit():
                user_id = int(event.actor_id)
            
            entry = AuditLog(
                user_id=user_id,
                user_email=event.actor_id or "system",
                action=event.event_type,
                target_type=event.entity_type,
                target_id=event.entity_id,
                details=event.payload,
                ip_address=event.ip_address,
                created_at=datetime.fromisoformat(event.occurred_at) if event.occurred_at else datetime.now(timezone.utc)
            )
            db.add(entry)
            db.commit()
            return True
        except Exception as e:
            logger.error(f"[RelationalAuditSink] Erro ao gravar log relacional: {e}")
            return False


class HeraclitusAuditSink(AuditSink):
    """
    Gravação append-only e verificável no HeraclitusDB (SPEC-0022 §13).
    Usa o sovereign ledger H-VM (/hvm/upsert) com autenticação e fallback resiliente.
    """
    def __init__(
        self,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        tenant_id: Optional[str] = None,
        required: bool = False
    ):
        self.base_url = (base_url or settings.HERACLITUS_REST_URL).rstrip("/")
        self.username = username or settings.HERACLITUS_USER
        self.password = password or settings.HERACLITUS_PASSWORD
        self.tenant_id = tenant_id or settings.HERACLITUS_TENANT
        self.required = required

    def append(self, event: AuditEvent, db: Optional[Session] = None) -> bool:
        if not settings.AUDIT_HERACLITUS:
            return True

        key = f"audit:{self.tenant_id}:{event.event_id}"
        val = event.to_json()

        try:
            with httpx.Client(timeout=3.0) as client:
                res = client.post(
                    f"{self.base_url}/hvm/upsert",
                    auth=(self.username, self.password),
                    json={"key": key, "val": val}
                )
                if res.status_code in (200, 201):
                    data = res.json()
                    lsn = data.get("lsn")
                    logger.info(f"[HeraclitusAuditSink] Evento {event.event_id} registrado com sucesso (LSN: {lsn}).")
                    return True
                else:
                    msg = f"Falha no HeraclitusDB ({res.status_code}): {res.text}"
                    if self.required:
                        raise RuntimeError(msg)
                    logger.warning(f"[HeraclitusAuditSink] {msg}")
                    return False
        except Exception as e:
            msg = f"HeraclitusDB indisponível: {e}"
            if self.required:
                raise RuntimeError(msg)
            logger.warning(f"[HeraclitusAuditSink] {msg}")
            return False

    def verify_integrity(self) -> Dict[str, Any]:
        """
        Consulta a integridade da árvore de Merkle e estatísticas do storage (SPEC-0022 §26 e §27).
        """
        try:
            with httpx.Client(timeout=4.0) as client:
                # 1. Health
                health_res = client.get(f"{self.base_url}/healthz", auth=(self.username, self.password))
                is_healthy = (health_res.status_code == 200 and "panta rhei" in health_res.text)

                # 2. Merkle Verify
                verify_res = client.get(f"{self.base_url}/verify", auth=(self.username, self.password))
                verify_data = verify_res.json() if verify_res.status_code == 200 else {}

                # 3. Stats & Metrics
                stats_res = client.get(f"{self.base_url}/stats", auth=(self.username, self.password))
                stats_data = stats_res.json() if stats_res.status_code == 200 else {}

                return {
                    "online": is_healthy,
                    "engine": "HeraclitusDB",
                    "storage_format": stats_data.get("storage_format", "v6"),
                    "merkle_ok": verify_data.get("merkle_ok", 0),
                    "merkle_status": "VALID" if verify_data.get("ok") else "UNVERIFIED",
                    "active_tail_crc_ok": verify_data.get("active_tail_crc_ok", False),
                    "head_records": stats_data.get("head", 0),
                    "total_records_verified": verify_data.get("records", 0),
                    "sealed_segments": verify_data.get("sealed", 0),
                    "shadow_mode": True,
                    "tenant_id": self.tenant_id,
                    "checked_at": datetime.now(timezone.utc).isoformat()
                }
        except Exception as e:
            return {
                "online": False,
                "engine": "HeraclitusDB",
                "error": str(e),
                "merkle_status": "UNAVAILABLE",
                "shadow_mode": True,
                "tenant_id": self.tenant_id,
                "checked_at": datetime.now(timezone.utc).isoformat()
            }


class CompositeAuditSink(AuditSink):
    """Sink composto (SPEC-0022 §13): dual-write para banco relacional e HeraclitusDB."""
    def __init__(self):
        self.relational = RelationalAuditSink()
        self.heraclitus = HeraclitusAuditSink(required=settings.HERACLITUS_REQUIRED)

    def append(self, event: AuditEvent, db: Optional[Session] = None) -> bool:
        r_ok = True
        h_ok = True

        if settings.AUDIT_POSTGRES:
            r_ok = self.relational.append(event, db)

        if settings.AUDIT_HERACLITUS:
            h_ok = self.heraclitus.append(event, db)

        return r_ok and (h_ok or not settings.HERACLITUS_REQUIRED)

    def verify_integrity(self) -> Dict[str, Any]:
        return self.heraclitus.verify_integrity()


# Instância global
audit_sink = CompositeAuditSink()
