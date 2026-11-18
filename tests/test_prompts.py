from internship_extractor.prompts import build_prompt


def test_invoice_prompt_substitutes_parameters():
    prompt = build_prompt(
        "invoice",
        "Acme invoice",
        source_language="English",
        currency="EUR",
    )

    assert "English" in prompt
    assert "EUR" in prompt
    assert "Acme invoice" in prompt


def test_resume_prompt_substitutes_target_role():
    prompt = build_prompt(
        "resume",
        "Python developer",
        source_language="French",
        target_role="Backend Engineer",
    )

    assert "French" in prompt
    assert "Backend Engineer" in prompt

