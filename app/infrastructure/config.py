"""
Configuration Management

Loads settings from environment variables with sensible defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Weaviate (local default)
    WEAVIATE_HOST: str = os.getenv("WEAVIATE_HOST", "127.0.0.1")
    WEAVIATE_HTTP_PORT: int = int(os.getenv("WEAVIATE_HTTP_PORT", "8080"))
    WEAVIATE_GRPC_PORT: int = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))

    # MinIO (local S3-compatible storage)
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ROOT_USER", "minio")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_ROOT_PASSWORD", "minio123")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "assets")

    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    OUTPUT_DIR: Path = PROJECT_ROOT / "out"


settings = Settings()
