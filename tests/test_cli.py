import io
import sys

import pytest

from internship_extractor.cli import read_input


def test_read_input_rejects_text_and_file():
    with pytest.raises(ValueError, match="either"):
        read_input("text", "document.txt")


def test_read_input_accepts_text():
    assert read_input("  invoice text  ", None) == "  invoice text  "


def test_read_input_accepts_stdin(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("resume from stdin"))
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    assert read_input(None, None) == "resume from stdin"
