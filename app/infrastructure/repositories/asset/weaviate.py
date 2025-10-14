"""
Weaviate Asset Repository

Stores and searches brand assets (seed images, generated creatives) using Weaviate vector database.
Uses multi2vec-clip for image vectorization and similarity search.
"""
import base64
from typing import Optional, List
from datetime import datetime
import weaviate
from weaviate.classes.config import Property, DataType, Configure
from weaviate.classes.query import Filter

from app.entities.creative_asset import CreativeAsset
from app.infrastructure.config import settings


COLLECTION_NAME = "BrandAsset"


class WeaviateAssetRepository:
    """Asset repository using Weaviate with multi2vec-clip for image search."""

    def __init__(self):
        self.client = weaviate.connect_to_local(
            host=settings.WEAVIATE_HOST,
            port=settings.WEAVIATE_HTTP_PORT,
            grpc_port=settings.WEAVIATE_GRPC_PORT,
        )
        self._ensure_schema()
        self.collection = self.client.collections.get(COLLECTION_NAME)

    def _ensure_schema(self) -> None:
        """Create BrandAsset collection schema if it doesn't exist."""
        if COLLECTION_NAME in self.client.collections.list_all():
            return

        self.client.collections.create(
            name=COLLECTION_NAME,
            description="Seed assets and generated campaign creatives",
            vectorizer_config=Configure.Vectorizer.multi2vec_clip(
                image_fields=["image"],
                text_fields=[
                    "message",
                    "tags",
                    "product_name",
                    "locale",
                    "aspect_ratio",
                ],
            ),
            properties=[
                Property(name="asset_id", data_type=DataType.TEXT),
                Property(name="brand_id", data_type=DataType.TEXT),
                Property(name="product_name", data_type=DataType.TEXT),
                Property(name="locale", data_type=DataType.TEXT),
                Property(name="aspect_ratio", data_type=DataType.TEXT),
                Property(name="message", data_type=DataType.TEXT),
                Property(name="tags", data_type=DataType.TEXT_ARRAY),
                Property(name="image_url", data_type=DataType.TEXT),
                Property(name="palette", data_type=DataType.TEXT_ARRAY),  # Hex colors
                Property(name="image", data_type=DataType.BLOB),  # For vectorization
            ],
        )

    def upsert(
        self,
        asset: CreativeAsset,
        image_bytes: Optional[bytes] = None,
        tags: Optional[List[str]] = None,
        palette: Optional[List[str]] = None,
    ) -> None:
        """
        Insert or update asset in Weaviate.

        Args:
            asset: CreativeAsset entity
            image_bytes: Image data for vectorization
            tags: Tags for filtering (e.g., ["seed", "uploaded"] or ["generated"])
            palette: Hex color palette (e.g., ["#FF5733", "#C70039"])
        """
        data = {
            "asset_id": asset.asset_id,
            "brand_id": asset.brand_id,
            "product_name": asset.product_name,
            "locale": asset.locale,
            "aspect_ratio": asset.aspect_ratio,
            "message": asset.message,
            "tags": tags or ["generated"],
            "image_url": asset.image_url,
            "palette": palette or [],
        }

        # Add image blob for vectorization (base64-encoded)
        if image_bytes:
            data["image"] = base64.b64encode(image_bytes).decode("ascii")

        self.collection.data.insert(data)

    def find_existing(
        self,
        product_name: str,
        aspect_ratio: str,
        locale: str = "en-US",
        limit: int = 3,
    ) -> List[CreativeAsset]:
        """
        Search for existing similar assets using hybrid search (vector + text).

        Args:
            product_name: Product to search for
            aspect_ratio: Aspect ratio filter
            locale: Locale filter
            limit: Max results

        Returns:
            List of matching CreativeAsset entities
        """
        # Filter by product, aspect, locale
        where_filter = (
            Filter.by_property("product_name").equal(product_name)
            & Filter.by_property("aspect_ratio").equal(aspect_ratio)
            & Filter.by_property("locale").equal(locale)
        )

        # Hybrid search (combines vector similarity + keyword matching)
        result = self.collection.query.hybrid(
            query=f"{product_name} hero {aspect_ratio}",
            filters=where_filter,
            limit=limit,
        )

        # Convert to CreativeAsset entities
        assets = []
        for obj in result.objects:
            props = obj.properties
            assets.append(
                CreativeAsset(
                    asset_id=props.get("asset_id", ""),
                    brand_id=props.get("brand_id", ""),
                    brief_id="",
                    product_name=props.get("product_name", ""),
                    audience="",  # Not stored for seeds
                    locale=props.get("locale", "en-US"),
                    aspect_ratio=props.get("aspect_ratio", "1:1"),
                    message=props.get("message", ""),
                    image_url=props.get("image_url", ""),
                    reused=True,  # These are existing assets
                    generated_at=datetime.now(),  # Placeholder
                    meta={},
                )
            )

        return assets

    def find_seeds(
        self, brand_id: str, product_name: Optional[str] = None, limit: int = 5
    ) -> List[dict]:
        """
        Find seed assets (uploaded by user) for a brand.

        Args:
            brand_id: Brand identifier
            product_name: Optional product filter
            limit: Max results

        Returns:
            List of Weaviate objects with seed asset data
        """
        where_filter = (
            Filter.by_property("brand_id").equal(brand_id)
            & Filter.by_property("tags").contains_any(["seed", "uploaded"])
        )

        if product_name:
            where_filter &= Filter.by_property("product_name").equal(product_name)

        result = self.collection.query.hybrid(
            query=f"{brand_id} seed",
            filters=where_filter,
            limit=limit,
        )

        return result.objects

    def __del__(self):
        """Close Weaviate client connection."""
        if hasattr(self, "client"):
            self.client.close()
