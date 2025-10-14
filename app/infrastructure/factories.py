"""
Adapter Factory

Dependency injection helper for creating adapters.
Enables toggling between fake and real implementations.
"""
from app.adapters.ai.protocol import IAIAdapter
from app.adapters.ai.fake import FakeAIAdapter
from app.adapters.ai.openai_image import OpenAIImageAdapter

from app.adapters.storage.protocol import IStorageAdapter
from app.adapters.storage.fake import FakeStorageAdapter
from app.adapters.storage.minio import MinIOStorageAdapter

from app.infrastructure.repositories.brand.protocol import IBrandRepository
from app.infrastructure.repositories.brand.in_memory import InMemoryBrandRepository
from app.infrastructure.repositories.brand.weaviate import WeaviateBrandRepository


def create_ai_adapter(use_real: bool = False) -> IAIAdapter:
    """
    Create AI adapter (fake or real OpenAI).

    Args:
        use_real: If True, use OpenAIImageAdapter; else use FakeAIAdapter

    Returns:
        IAIAdapter implementation
    """
    if use_real:
        return OpenAIImageAdapter()
    return FakeAIAdapter()


def create_storage_adapter(use_real: bool = False) -> IStorageAdapter:
    """
    Create storage adapter (fake or real MinIO).

    Args:
        use_real: If True, use MinIOStorageAdapter; else use FakeStorageAdapter

    Returns:
        IStorageAdapter implementation
    """
    if use_real:
        return MinIOStorageAdapter()
    return FakeStorageAdapter()


def create_brand_repository(use_real: bool = False) -> IBrandRepository:
    """
    Create brand repository (fake or real Weaviate).

    Args:
        use_real: If True, use WeaviateBrandRepository; else use InMemoryBrandRepository

    Returns:
        IBrandRepository implementation
    """
    if use_real:
        return WeaviateBrandRepository()
    return InMemoryBrandRepository()
