import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    
    # Base de Datos SQLite 3 (Ruta Absoluta para evitar discrepancias por directorio de trabajo)
    DATABASE_URL: str = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'jmshop.db').replace('\\', '/')}"
    
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
