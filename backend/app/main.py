import os
import sys

# Asegurar que el directorio backend y sus submódulos estén siempre en sys.path
_current_file_dir = os.path.dirname(os.path.abspath(__file__))
_backend_dir = os.path.dirname(_current_file_dir)
_root_dir = os.path.dirname(_backend_dir)
for _d in [_backend_dir, _root_dir]:
    if _d not in sys.path:
        sys.path.insert(0, _d)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from app.core.config import settings
from app.db.database import init_db
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Inicializa la estructura de tablas en la base de datos SQLite 3 al arrancar la aplicación.
    """
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API RESTful para JMSHOP E-Commerce (FastAPI + SQLModel + SQLite 3)",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# =========================================================
# MIDDLEWARE UNIVERSAL DE CORS (Soporta file:// Origin:null, Localhost y Dev)
# =========================================================
@app.middleware("http")
async def universal_cors_middleware(request: Request, call_next):
    # Obtener origen de la petición (manejando el valor 'null' producido por file://)
    raw_origin = request.headers.get("origin")
    allowed_origin = raw_origin if raw_origin and raw_origin != "null" else "*"

    # Responder inmediatamente a preflight OPTIONS
    if request.method == "OPTIONS":
        response = Response(status_code=200)
        response.headers["Access-Control-Allow-Origin"] = allowed_origin
        if allowed_origin != "*":
            response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept"
        return response

    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = allowed_origin
    if allowed_origin != "*":
        response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept"
    return response


@app.get("/", tags=["Health Check"])
def root_status():
    """Endpoint de estado para verificación de salud de la API."""
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }


# Registrar Rutas de la API v1 (/api/v1)
app.include_router(api_router, prefix=settings.API_V1_STR)
