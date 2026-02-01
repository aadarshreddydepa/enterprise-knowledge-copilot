import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import AsyncSessionLocal
from app.audit.service import create_audit_log


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()

        response = None
        outcome = "success"

        try:
            response = await call_next(request)
            if response.status_code >= 400:
                outcome = "error"
            return response

        except Exception:
            outcome = "exception"
            raise

        finally:
            latency_ms = int((time.time() - start) * 1000)

            user = getattr(request.state, "user", None)
            roles = getattr(request.state, "roles", [])

            # Skip unauthenticated requests (login, health, etc.)
            if not user:
                return

            async with AsyncSessionLocal() as db:
                await create_audit_log(
                    db=db,
                    user_id=user.id,
                    action=f"{request.method} {request.url.path}",
                    roles_applied=roles,
                    outcome=outcome,
                    latency_ms=latency_ms,
                )
