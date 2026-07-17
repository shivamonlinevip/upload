"""
Central configuration for the multi-agent financial advisor system.
Loads settings from environment variables / .env file.

Supports two LLM providers, selected via LLM_PROVIDER:
  - "anthropic" (default) - uses the Claude API
  - "gemini"               - uses the Google Gemini API (google-genai SDK)
"""
import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic").lower().strip()

# --- Anthropic (Claude) settings ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5")

# --- Google Gemini settings ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true"
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

if LLM_PROVIDER not in ("anthropic", "gemini"):
    raise EnvironmentError(
        f"Invalid LLM_PROVIDER '{LLM_PROVIDER}'. Must be 'anthropic' or 'gemini'."
    )

if LLM_PROVIDER == "anthropic" and not ANTHROPIC_API_KEY:
    raise EnvironmentError(
        "LLM_PROVIDER is 'anthropic' but ANTHROPIC_API_KEY is not set. "
        "Copy .env.example to .env and add your key, or export it in your shell."
    )

if LLM_PROVIDER == "gemini" and not GEMINI_API_KEY:
    raise EnvironmentError(
        "LLM_PROVIDER is 'gemini' but GEMINI_API_KEY is not set. "
        "Copy .env.example to .env and add your key, or export it in your shell. "
        "Get a key at https://aistudio.google.com/apikey"
    )
