import pytest

from internship_extractor.extractor import ExtractionError, extract


class StubProvider:
    def __init__(self, output: str):
        self.output = output

    def generate(self, prompt: str) -> str:
        assert "invoice" in prompt.lower()
        return self.output


def test_extract_invoice_json():
    result = extract(
        StubProvider(
            '{"document_type":"invoice","invoice_number":"A-1","currency":"EUR","total":42.5}'
        ),
        "invoice",
        "Invoice A-1 from Acme",
    )

    assert result.document_type == "invoice"
    assert str(result.total) == "42.5"


def test_extract_rejects_invalid_json():
    with pytest.raises(ExtractionError, match="invalid JSON"):
        extract(StubProvider("not json"), "invoice", "Invoice")


def test_extract_rejects_schema_violation():
    with pytest.raises(ExtractionError, match="schema validation"):
        extract(
            StubProvider('{"document_type":"invoice","currency":"US"}'),
            "invoice",
            "Invoice",
        )

