"""
Fake Storage Adapter for Testing

In-memory storage for fast tests.
"""
from typing import Dict, List


class FakeStorageAdapter:
    """In-memory storage adapter implementing IStorageAdapter protocol."""

    def __init__(self):
        self.storage: Dict[str, bytes] = {}

    def save(self, path: str, content: bytes) -> str:
        """Save to in-memory dict."""
        self.storage[path] = content
        return path

    def load(self, path: str) -> bytes:
        """Load from in-memory dict."""
        if path not in self.storage:
            raise FileNotFoundError(f"File not found: {path}")
        return self.storage[path]

    def exists(self, path: str) -> bool:
        """Check existence in dict."""
        return path in self.storage

    def list(self, prefix: str) -> List[str]:
        """List files with prefix."""
        return [k for k in self.storage.keys() if k.startswith(prefix)]
