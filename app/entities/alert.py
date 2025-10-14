"""Alert Entity

Agentic monitoring and alerting (Task 3).
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types of alerts for agentic monitoring."""
    MISSING_ASSETS = "missing_assets"
    INSUFFICIENT_VARIANTS = "insufficient_variants"  # < 3 variants (Task 3 requirement)
    GENERATION_FAILED = "generation_failed"
    VALIDATION_FAILED = "validation_failed"
    API_ERROR = "api_error"
    APPROVAL_TIMEOUT = "approval_timeout"


@dataclass
class Alert:
    """
    Alert for agentic monitoring system (Task 3).

    Tracks issues requiring:
    - Automated remediation
    - Human notification
    - Stakeholder communication
    """
    alert_id: str
    brief_id: str
    alert_type: AlertType
    severity: AlertSeverity
    message: str
    context: Dict[str, Any]  # Additional context for Model Context Protocol (Task 3)
    created_at: datetime
    resolved_at: Optional[datetime]
    resolution: Optional[str]

    def to_human_readable(self) -> str:
        """
        Format alert for stakeholder communication (Task 3).

        Uses Model Context Protocol to generate human-readable message
        via LLM (e.g., Claude).
        """
        return f"[{self.severity.value.upper()}] {self.alert_type.value}: {self.message}"

    @property
    def is_resolved(self) -> bool:
        """Check if alert has been resolved."""
        return self.resolved_at is not None
