"""
MinIO Storage Adapter

Implements IStorageAdapter protocol for S3-compatible blob storage.
"""
import boto3
from typing import List
from botocore.exceptions import ClientError

from app.infrastructure.config import settings


class MinIOStorageAdapter:
    """S3-compatible storage adapter using MinIO."""

    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.MINIO_ENDPOINT,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
        )
        self.bucket = settings.MINIO_BUCKET
        self._ensure_bucket()

    def _ensure_bucket(self) -> None:
        """Create bucket if it doesn't exist."""
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket)

    def save(self, path: str, content: bytes) -> str:
        """
        Save content to MinIO.

        Args:
            path: Relative path (e.g., "lavender-soap/en-US/1x1/asset-123.png")
            content: File content (bytes)

        Returns:
            S3 URI (s3://bucket/path)
        """
        self.client.put_object(
            Bucket=self.bucket,
            Key=path,
            Body=content,
            ContentType="image/png",
        )
        return f"s3://{self.bucket}/{path}"

    def load(self, path: str) -> bytes:
        """Load content from MinIO."""
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=path)
            return response["Body"].read()
        except ClientError as e:
            raise FileNotFoundError(f"File not found: {path}") from e

    def exists(self, path: str) -> bool:
        """Check if file exists in MinIO."""
        try:
            self.client.head_object(Bucket=self.bucket, Key=path)
            return True
        except ClientError:
            return False

    def list(self, prefix: str) -> List[str]:
        """List files with given prefix."""
        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix,
            )
            if "Contents" not in response:
                return []
            return [obj["Key"] for obj in response["Contents"]]
        except ClientError:
            return []
