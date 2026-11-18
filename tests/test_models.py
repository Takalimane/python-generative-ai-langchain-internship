from decimal import Decimal

import pytest
from pydantic import ValidationError

from internship_extractor.models import InvoiceAnalysis, ResumeAnalysis


def test_invoice_accepts_strict_valid_payload():
    result = InvoiceAnalysis.model_validate(
        {
            "document_type": "invoice",
            "invoice_number": "INV-12",
            "currency": "usd",
            "total": "125.50",
            "line_items": [],
        }
    )

    assert result.currency == "USD"
    assert result.total == Decimal("125.50")


def test_invoice_rejects_extra_fields():
    with pytest.raises(ValidationError):
        InvoiceAnalysis.model_validate(
            {"document_type": "invoice", "unknown_field": "unexpected"}
        )


def test_resume_accepts_valid_payload():
    result = ResumeAnalysis.model_validate(
        {
            "document_type": "resume",
            "candidate_name": "Alex Student",
            "skills": [{"name": "Python", "level": "advanced"}],
        }
    )

    assert result.skills[0].name == "Python"

