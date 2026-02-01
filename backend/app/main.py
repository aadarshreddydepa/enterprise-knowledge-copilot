from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.audit.middleware import AuditMiddleware

app = FastAPI()

app.include_router(auth_router)
app.add_middleware(AuditMiddleware)