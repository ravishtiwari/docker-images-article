from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    app_name: str = "IMDb API"
    debug: bool = False
    version: str = "1.0.0"

    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/imdb_db"

    # AWS S3
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    s3_bucket_name: Optional[str] = None

    # Google Cloud Storage
    gcp_project_id: Optional[str] = None
    gcs_bucket_name: Optional[str] = None
    google_application_credentials: Optional[str] = None

    # Vector Search
    vector_dimension: int = 384

    # Auth (placeholder for future implementation)
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
