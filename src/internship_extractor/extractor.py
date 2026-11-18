from __future__ import annotations

import json
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from .models import InvoiceAnalysis, ResumeAnalysis
from .prompts import build_prompt
from .providers import TextProvider


T = TypeVar("T", bound=BaseModel)


class ExtractionError(RuntimeError):
    pass


def extract(
    provider: TextProvider,
    document_type: str,
    document_text: str,
    **prompt_parameters: str,
) -> InvoiceAnalysis | ResumeAnalysis:
    if document_type not in {"invoice", "resume"}:
        raise ExtractionError("Document type must be 'invoice' or 'resume'")

    model: type[InvoiceAnalysis] | type[ResumeAnalysis]
    model = InvoiceAnalysis if document_type == "invoice" else ResumeAnalysis

    prompt = build_prompt(document_type, document_text, **prompt_parameters)
    raw = provider.generate(prompt)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ExtractionError("The model returned invalid JSON") from exc

    try:
        return model.model_validate(data)
    except ValidationError as exc:
        details = "; ".join(
            f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
            for error in exc.errors()
        )
        raise ExtractionError(f"Model JSON failed schema validation: {details}") from exc

