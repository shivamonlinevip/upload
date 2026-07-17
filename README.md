# Multi-Agent AI Financial Advisor

A 6-agent pipeline (Market → News → Risk → Portfolio → Verifier → Explainability),
coordinated by a plain-Python orchestrator, built on the Claude API.

```
User Input
   │
   ▼
Market Agent          – fundamentals, valuation, strengths/weaknesses
   │
   ▼
News Agent            – sentiment, events (optionally uses live web_search)
   │
   ▼
Risk Agent            – market/business/sector/political/liquidity/currency risk
   │
   ▼
Portfolio Agent        – diversified % allocation suggestion
   │
   ▼
Verifier Agent          – checks prior agents for hallucination/overconfidence
   │
   ▼
Explainability Agent  – plain-English "why" behind everything
   │
   ▼
Final Response
```

Each LLM agent is a strict system-prompt + JSON-schema contract (see `agents/`).
The orchestrator (`orchestrator.py`) calls them in sequence, feeding each
agent's output into the next, and folds the Verifier's `confidence_adjustment`
into a single final confidence score.

## 1. Requirements

- Python 3.9+
- An Anthropic API key: https://console.anthropic.com/settings/keys

## 2. Setup

```bash
# 1. Unzip / cd into the project
cd financial_advisor_multiagent

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
cp .env.example .env
# then open .env and paste your key into ANTHROPIC_API_KEY=
```

## 3. Run it

```bash
python main.py --company "Tata Motors" --budget 100000 --duration "5 years" --risk moderate
```

Arguments:

| Flag | Required | Example | Notes |
|---|---|---|---|
| `--company` | yes | `"Tata Motors"` | Company name to analyze |
| `--budget` | yes | `100000` | Numeric amount |
| `--duration` | yes | `"5 years"` | Investment horizon, free text |
| `--risk` | no | `moderate` | `conservative` \| `moderate` \| `aggressive` (default `moderate`) |
| `--save-json` | no | `report.json` | Also dumps the full structured pipeline output to a JSON file |

Example with a saved JSON report:

```bash
python main.py --company "Tata Motors" --budget 100000 --duration "5 years" --risk moderate --save-json report.json
```

### Expected console output shape

```
[1/6] Market Agent analyzing Tata Motors...
[2/6] News Agent gathering & analyzing news...
[3/6] Risk Agent assessing risk...
[4/6] Portfolio Agent building allocation...
[5/6] Verifier Agent checking for issues...
[6/6] Explainability Agent writing plain-English explanation...

======================================================================
  INVESTMENT ANALYSIS: Tata Motors
======================================================================
Budget: 100,000 | Duration: 5 years | Risk Profile: moderate

--- Market Analysis --------------------------------------------
...
--- News Analysis -----------------------------------------------
...
--- Risk Analysis ------------------------------------------------
Overall Risk: Medium
Risk Score: 62
...
--- Portfolio Suggestion ------------------------------------
  Tata Motors                 35%
  Nifty ETF                   40%
  Gold ETF                    15%
  Liquid Fund                 10%
...
--- Verification --------------------------------------------------
No unsupported claims detected.
Confidence adjustment: -3
--- Explainability ---------------------------------------------
...
======================================================================
  FINAL CONFIDENCE: 87%
======================================================================
```

## 4. Configuration options (`.env`)

| Variable | Default | Purpose |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` | `anthropic` or `gemini` — picks which API every agent uses |
| `ANTHROPIC_API_KEY` | — | Required when `LLM_PROVIDER=anthropic` |
| `CLAUDE_MODEL` | `claude-sonnet-5` | Model used by every agent (Anthropic) |
| `GEMINI_API_KEY` | — | Required when `LLM_PROVIDER=gemini`. Get one at https://aistudio.google.com/apikey |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Model used by every agent (Gemini) |
| `ENABLE_WEB_SEARCH` | `true` | If `true`, the News Agent uses live web search — Claude's `web_search` tool, or Gemini's Google Search grounding — instead of relying on model knowledge alone |
| `MAX_TOKENS` | `2000` | Max output tokens per agent call |

## 4b. Switching to Google Gemini

The whole system was built so that swapping providers is just a config
change — no agent logic, prompts, or orchestration changes needed.

1. Get a Gemini API key: https://aistudio.google.com/apikey
2. Install the extra dependency (already in `requirements.txt`):
   ```bash
   pip install google-genai
   ```
3. In your `.env`, set:
   ```
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```
4. Run exactly the same command as before:
   ```bash
   python main.py --company "Tata Motors" --budget 100000 --duration "5 years" --risk moderate
   ```

Under the hood, `agents/base_agent.py` checks `LLM_PROVIDER` and routes each
call to either the Anthropic SDK (`system` param + `web_search` tool) or the
Gemini SDK (`system_instruction` in `GenerateContentConfig` + Google Search
grounding tool). Every other file — `market_agent.py`, `news_agent.py`,
`orchestrator.py`, `main.py` — is provider-agnostic and untouched.

**Note on models:** Google updates Gemini model names periodically. If
`gemini-2.5-flash` returns a "model not found" error, check the current list
at https://ai.google.dev/gemini-api/docs/models and update `GEMINI_MODEL` in
`.env`. For higher-quality output at higher cost, try a `-pro` variant.

## 5. Project structure

```
financial_advisor_multiagent/
├── main.py                     # CLI entry point
├── orchestrator.py             # Python orchestrator — chains all agents
├── config.py                   # Loads env vars / API key
├── requirements.txt
├── .env.example
├── README.md
└── agents/
    ├── __init__.py
    ├── base_agent.py           # Shared Claude-calling + JSON-parsing logic
    ├── market_agent.py
    ├── news_agent.py
    ├── risk_agent.py
    ├── portfolio_agent.py
    ├── verifier_agent.py
    └── explainability_agent.py
```

## 6. Using it as a library (no CLI)

```python
from orchestrator import Orchestrator, UserRequest

orchestrator = Orchestrator()
request = UserRequest(company="Infosys", budget=250000, duration="3 years", risk_profile="aggressive")
result = orchestrator.run(request, verbose=False)

print(result.portfolio_recommendation)
print(result.final_confidence)
```

## 7. Notes & disclaimers

- This tool never issues BUY/SELL calls or guarantees returns — the Portfolio
  Agent is explicitly prompted to avoid that. All agents are prompted to
  return honest confidence scores and flag uncertainty.
- This is a decision-support / educational demo, **not** licensed financial
  advice. Validate outputs independently before acting on them.
- If a company name is ambiguous or very obscure, results depend on what the
  model already knows plus whatever `web_search` (News Agent only) can find —
  consider adding a real market-data API (e.g. a stock quotes provider) for
  production-grade numeric accuracy.
