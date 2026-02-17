from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.audit.middleware import AuditMiddleware
from app.ingestion.router import router as ingestion_router

app = FastAPI()

app.include_router(auth_router)
app.add_middleware(AuditMiddleware)
app.include_router(ingestion_router)