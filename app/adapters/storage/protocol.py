"""
Storage Adapter Protocol

Defines contract for storage services:
- Local filesystem (default)
- MinIO/S3 (production)
"""
from typing import Protocol, List


class IStorageAdapter(Protocol):
    """Interface for storage adapters."""

    def save(self, path: str, content: bytes) -> str:
        """
        Save content to storage.

        Args:
            path: Relative path (e.g., "lavender-soap/en-US/1x1/asset-123.png")
            content: File content (bytes)

        Returns:
            Full storage path or URL
        """
        ...

    def load(self, path: str) -> bytes:
        """Load content from storage."""
        ...

    def exists(self, path: str) -> bool:
        """Check if file exists."""
        ...

    def list(self, prefix: str) -> List[str]:
        """List files with given prefix."""
        ...
