import os
import shutil
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_default_db_url() -> str:
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    default_db = os.path.join(backend_dir, "jmshop.db")
    
    # En entorno Vercel Serverless Function, copiar DB a /tmp para soporte de lectura/escritura
    if os.getenv("VERCEL") or os.getenv("LAMBDA_TASK_ROOT"):
        tmp_db = "/tmp/jmshop.db"
        if not os.path.exists(tmp_db) and os.path.exists(default_db):
            try:
                shutil.copyfile(default_db, tmp_db)
            except Exception:
                pass
        return f"sqlite:///{tmp_db}"
    
    return f"sqlite:///{default_db.replace('\\', '/')}"


class Settings(BaseSettings):
    """
    Configuración global de la aplicación utilizando Pydantic Settings.
    Permite cargar variables desde variables de entorno o valores por defecto.
    """
    PROJECT_NAME: str = "JMSHOP E-Commerce API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Seguridad JWT
    SECRET_KEY: str = "jmshop_super_secret_jwt_key_2026_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 Horas
    
    # Base de Datos SQLite 3
    DATABASE_URL: str = get_default_db_url()
    
    # Middleware CORS: Permitir Host Local (desarrollo frontend)
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


settings = Settings()
