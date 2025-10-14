"""Validation Result Entity

Brand compliance and legal checks (Decision 10: Nice-to-have).
"""
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ValidationStatus(Enum):
    """Validation check status."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


@dataclass
class ValidationIssue:
    """Individual validation issue."""
    check_name: str
    severity: str  # "error", "warning", "info"
    message: str
    fix_suggestion: Optional[str]


@dataclass
class ValidationResult:
    """
    Validation result for brand compliance and legal checks.

    Decision 10: Implement logging + legal checks (stubbed orchestrator methods).
    - Brand compliance: Logo presence, color usage (stubbed for PoC)
    - Legal checks: Prohibited words (implemented)
    """
    asset_id: str
    status: ValidationStatus
    checks_run: List[str]  # ["prohibited_words", "brand_colors", "logo_presence"]
    issues: List[ValidationIssue]
    passed_count: int
    failed_count: int

    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)."""
        return self.status == ValidationStatus.PASSED and self.failed_count == 0

    def summary(self) -> str:
        """Generate validation summary for logging."""
        return f"Validation: {self.passed_count} passed, {self.failed_count} failed"
