from string import Template


INVOICE_TEMPLATE = Template(
    """You analyze invoice text and return exactly one JSON object.
Task parameters:
- requested_document_type: invoice
- source_language: $source_language
- output_currency: $currency

Rules:
- Use null for fields that are not present.
- Return ISO-style dates when identifiable (YYYY-MM-DD), otherwise preserve the text.
- Do not invent values.
- Return amounts as JSON numbers, not strings.
- Use a three-letter uppercase ISO currency code in "currency".
- The response must contain no markdown, explanation, or text outside the JSON object.

Invoice text:
---
$document_text
---
"""
)


RESUME_TEMPLATE = Template(
    """You analyze resume text and return exactly one JSON object.
Task parameters:
- requested_document_type: resume
- source_language: $source_language
- target_role: $target_role

Rules:
- Use null for fields that are not present.
- Keep candidate facts grounded in the source text.
- Skill levels may be beginner, intermediate, advanced, or null; infer only with clear evidence.
- The response must contain no markdown, explanation, or text outside the JSON object.

Resume text:
---
$document_text
---
"""
)


def build_prompt(document_type: str, document_text: str, **parameters: str) -> str:
    template = INVOICE_TEMPLATE if document_type == "invoice" else RESUME_TEMPLATE
    defaults = {
        "source_language": "auto",
        "currency": "USD",
        "target_role": "not specified",
    }
    defaults.update(parameters)
    return template.substitute(document_text=document_text, **defaults)
