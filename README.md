# Internship Document Extractor

A Python CLI that analyzes invoice or resume text with Google Gemini or OpenAI and returns strictly validated JSON.

## Features

- Gemini or OpenAI selected through environment configuration
- Invoice and resume parameterized prompt templates
- Pydantic v2 strict schemas with extra fields rejected
- Input from argument, UTF-8 file, or standard input
- Clear non-zero error exits and 100,000-character input limit
- Focused unit tests

## Setup

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
Copy-Item .env.example .env
```

Set one provider in `.env`:

```dotenv
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.0-flash
```

Or:

```dotenv
AI_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
```

Do not commit `.env` or API keys.

## Usage

Analyze an example invoice:

```powershell
document-extractor invoice --file examples/invoice.txt --currency USD
```

Analyze resume text:

```powershell
document-extractor resume --file examples/resume.txt --role "Backend Engineer"
```

Pipe text from standard input:

```powershell
Get-Content examples/resume.txt -Raw | document-extractor resume --role "Backend Engineer"
```

Override the provider:

```powershell
document-extractor resume --file examples/resume.txt --provider openai
```

## JSON output

Invalid provider configuration, empty input, malformed model JSON, and Pydantic schema failures exit with status `2` and write a safe error to stderr. API credentials are never included in errors or output.

## Tests

```powershell
python -m pytest
```
