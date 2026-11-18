from __future__ import annotations

import os
from typing import Protocol


class ProviderError(RuntimeError):
    pass


class TextProvider(Protocol):
    def generate(self, prompt: str) -> str: ...


class GeminiProvider:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ProviderError("GEMINI_API_KEY is required for the Gemini provider")
        try:
            from google import genai
        except ImportError as exc:
            raise ProviderError("Gemini support requires 'google-genai'.") from exc
        self.client = genai.Client(api_key=key)
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(model=self.model, contents=prompt)
            if not response.text:
                raise ProviderError("Gemini returned an empty response")
            return response.text
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError(f"Gemini request failed: {exc}") from exc


class OpenAIProvider:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ProviderError("OPENAI_API_KEY is required for the OpenAI provider")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ProviderError("OpenAI support requires 'openai'.") from exc
        self.client = OpenAI(api_key=key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            if not content:
                raise ProviderError("OpenAI returned an empty response")
            return content
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError(f"OpenAI request failed: {exc}") from exc


def create_provider(name: str) -> TextProvider:
    if name == "gemini":
        return GeminiProvider()
    if name == "openai":
        return OpenAIProvider()
    raise ProviderError("AI_PROVIDER must be 'gemini' or 'openai'")
