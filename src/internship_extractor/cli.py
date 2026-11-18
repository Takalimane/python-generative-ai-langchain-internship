from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

from .extractor import ExtractionError, extract
from .providers import ProviderError, create_provider


def read_input(text: str | None, file: str | None) -> str:
    if text is not None and file is not None:
        raise ValueExtractionError("Use either --text or --file, not both")
    if text is not None:
        value = text
    elif file is not None:
        path = Path(file)
        try:
            value = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueExtractionError(f"Could not read input file: {exc}") from exc
    else:
        if sys.stdin.isatty():
            raise ValueExtractionError("Provide --text, --file, or pipe text through stdin")
        value = sys.stdin.read()

    if not value.strip():
        raise ValueExtractionError("Input document cannot be empty")
    if len(value) > 100_000:
        raise ValueExtractionError("Input document exceeds the 100,000 character limit")
    return value


class ValueExtractionError(ValueError):
    pass


def model_json(model: BaseModel) -> str:
    return json.dumps(model.model_dump(mode="json"), ensure_ascii=False, indent=2)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="document-extractor",
        description="Extract invoice or resume data into validated JSON.",
    )
    parser.add_argument("document_type", choices=("invoice", "resume"))
    parser.add_argument("--text", help="Document text")
    parser.add_argument("--file", help="UTF-8 text file")
    parser.add_argument("--provider", choices=("gemini", "openai"), help="Override AI_PROVIDER")
    parser.add_argument("--language", default="auto", help="Source language hint")
    parser.add_argument("--currency", default="USD", help="Invoice currency hint")
    parser.add_argument("--role", default="not specified", help="Resume target role")
    return parser


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    args = build_parser().parse_args(argv)

    try:
        document_text = read_input(args.text, args.file)
        provider_name = args.provider or os.getenv("AI_PROVIDER", "gemini").lower()
        provider = create_provider(provider_name)
        parameters = {
            "source_language": args.language,
            "currency": args.currency,
            "target_role": args.role,
        }
        result = extract(provider, args.document_type, document_text, **parameters)
        print(model_json(result))
        return 0
    except (ValueExtractionError, ProviderError, ExtractionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Error: operation cancelled", file=sys.stderr)
        return 130

