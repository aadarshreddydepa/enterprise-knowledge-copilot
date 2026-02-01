from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.audit_log import AuditLog


async def create_audit_log(
    db: AsyncSession,
    *,
    user_id,
    action: str,
    roles_applied: list[str],
    outcome: str,
    latency_ms: int,
    retrieved_doc_ids: list[str] | None = None,
):
    log = AuditLog(
        user_id=user_id,
        action=action,
        roles_applied=roles_applied,
        retrieved_doc_ids=retrieved_doc_ids,
        outcome=outcome,
        latency_ms=latency_ms,
    )

    db.add(log)
    await db.commit()
