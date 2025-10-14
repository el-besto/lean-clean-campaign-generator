"""Approval Entity

HITL approval tracking (Task 3: Agentic system).
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum


class ApprovalStatus(Enum):
    """Approval workflow states."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_REVIEW = "in_review"


@dataclass
class Approval:
    """
    HITL approval checkpoint (Decision 9: Simulated with logging).

    Tracks approval workflow for:
    - Brand choice (understand_brand → search_similar_brands → accept_brand_choice)
    - Campaign images (generate_campaign → accept_campaign_images)
    """
    approval_id: str
    brief_id: str
    checkpoint_name: str  # e.g., "brand_choice", "campaign_images"
    status: ApprovalStatus
    product_name: Optional[str]
    aspect_ratio: Optional[str]
    approved_by: Optional[str]  # Stakeholder name (for Task 3)
    comment: str
    started_at: datetime
    finished_at: Optional[datetime]

    @property
    def duration_seconds(self) -> Optional[int]:
        """Calculate approval duration (for Task 3 metrics)."""
        if self.finished_at:
            return int((self.finished_at - self.started_at).total_seconds())
        return None

    def is_blocking(self) -> bool:
        """Check if approval is blocking campaign generation."""
        return self.status in [ApprovalStatus.PENDING, ApprovalStatus.IN_REVIEW]
