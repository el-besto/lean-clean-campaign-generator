"""
Weaviate Brand Repository

Implements IBrandRepository protocol using Weaviate vector database.
Enables brand similarity search and vector-based retrieval.
"""
from typing import Optional, List
from datetime import datetime
import weaviate
from weaviate.classes.config import Property, DataType, Configure
from weaviate.classes.query import Filter

from app.entities.brand_summary import BrandSummary
from app.infrastructure.config import settings


COLLECTION_NAME = "Brand"


class WeaviateBrandRepository:
    """Brand repository using Weaviate vector database."""

    def __init__(self):
        self.client = weaviate.connect_to_local(
            host=settings.WEAVIATE_HOST,
            port=settings.WEAVIATE_HTTP_PORT,
            grpc_port=settings.WEAVIATE_GRPC_PORT,
        )
        self._ensure_schema()
        self.collection = self.client.collections.get(COLLECTION_NAME)

    def _ensure_schema(self) -> None:
        """Create Brand collection schema if it doesn't exist."""
        if COLLECTION_NAME in self.client.collections.list_all():
            return

        self.client.collections.create(
            name=COLLECTION_NAME,
            description="Brand identity and guidelines for campaign generation",
            vectorizer_config=Configure.Vectorizer.text2vec_transformers(),
            properties=[
                Property(name="brand_id", data_type=DataType.TEXT),
                Property(name="name", data_type=DataType.TEXT),
                Property(name="description", data_type=DataType.TEXT),
                Property(name="colors", data_type=DataType.TEXT_ARRAY),
                Property(name="typography", data_type=DataType.TEXT),
                Property(name="voice_tone", data_type=DataType.TEXT),
                Property(name="target_audiences", data_type=DataType.TEXT_ARRAY),
                Property(name="target_regions", data_type=DataType.TEXT_ARRAY),
                Property(name="products", data_type=DataType.TEXT_ARRAY),
                Property(name="campaign_slogans", data_type=DataType.TEXT_ARRAY),
                Property(name="logo_url", data_type=DataType.TEXT),
                Property(name="created_at", data_type=DataType.DATE),
                Property(name="updated_at", data_type=DataType.DATE),
            ],
        )

    def get_by_id(self, brand_id: str) -> Optional[BrandSummary]:
        """
        Load brand by ID from Weaviate.

        Args:
            brand_id: Unique brand identifier

        Returns:
            BrandSummary entity or None if not found
        """
        # Query by brand_id property
        where_filter = Filter.by_property("brand_id").equal(brand_id)
        result = self.collection.query.fetch_objects(filters=where_filter, limit=1)

        if not result.objects:
            return None

        # Convert Weaviate object to BrandSummary entity
        props = result.objects[0].properties
        return BrandSummary(
            brand_id=props["brand_id"],
            name=props["name"],
            description=props["description"],
            colors=props.get("colors", []),
            typography=props.get("typography", ""),
            voice_tone=props.get("voice_tone", ""),
            target_audiences=props.get("target_audiences", []),
            target_regions=props.get("target_regions", []),
            products=props.get("products", []),
            campaign_slogans=props.get("campaign_slogans", []),
            logo_url=props.get("logo_url"),
            created_at=datetime.fromisoformat(props["created_at"]),
            updated_at=datetime.fromisoformat(props["updated_at"]),
        )

    def search_similar(self, brand: BrandSummary, limit: int = 5) -> List[BrandSummary]:
        """
        Find similar brands using vector search.

        Args:
            brand: Reference brand for similarity search
            limit: Maximum number of results

        Returns:
            List of similar BrandSummary entities
        """
        # Build search query from brand attributes
        query_text = f"{brand.description} {brand.voice_tone} {' '.join(brand.target_audiences)}"

        result = self.collection.query.near_text(
            query=query_text,
            limit=limit,
        )

        # Convert results to BrandSummary entities
        brands = []
        for obj in result.objects:
            props = obj.properties
            brands.append(
                BrandSummary(
                    brand_id=props["brand_id"],
                    name=props["name"],
                    description=props["description"],
                    colors=props.get("colors", []),
                    typography=props.get("typography", ""),
                    voice_tone=props.get("voice_tone", ""),
                    target_audiences=props.get("target_audiences", []),
                    target_regions=props.get("target_regions", []),
                    products=props.get("products", []),
                    campaign_slogans=props.get("campaign_slogans", []),
                    logo_url=props.get("logo_url"),
                    created_at=datetime.fromisoformat(props["created_at"]),
                    updated_at=datetime.fromisoformat(props["updated_at"]),
                )
            )

        return brands

    def upsert(self, brand: BrandSummary) -> None:
        """
        Insert or update brand in Weaviate.

        Args:
            brand: BrandSummary entity to persist
        """
        data = {
            "brand_id": brand.brand_id,
            "name": brand.name,
            "description": brand.description,
            "colors": brand.colors,
            "typography": brand.typography,
            "voice_tone": brand.voice_tone,
            "target_audiences": brand.target_audiences,
            "target_regions": brand.target_regions,
            "products": brand.products,
            "campaign_slogans": brand.campaign_slogans,
            "logo_url": brand.logo_url or "",
            "created_at": brand.created_at.isoformat(),
            "updated_at": brand.updated_at.isoformat(),
        }
        self.collection.data.insert(data)

    def __del__(self):
        """Close Weaviate client connection."""
        if hasattr(self, "client"):
            self.client.close()
