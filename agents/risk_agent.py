import json
from .base_agent import BaseAgent

SYSTEM_PROMPT = """You are Risk Assessment Agent.

Input:
- Market Analysis
- News Analysis
- User Risk Profile

Tasks:

Evaluate:
- Market Risk
- Business Risk
- Sector Risk
- Political Risk
- Liquidity Risk
- Currency Risk
- Volatility Risk

Assign overall risk level.

Return ONLY valid JSON, no markdown fences, no preamble, in this exact format:

{
 "overall_risk": "Low/Medium/High",
 "risk_score": 0,
 "major_risks": [],
 "risk_reasoning": "",
 "confidence": 0
}"""


class RiskAgent(BaseAgent):
    name = "Risk Agent"
    system_prompt = SYSTEM_PROMPT

    def analyze(self, market_analysis: dict, news_analysis: dict, user_risk_profile: str) -> dict:
        message = (
            "Here is the Market Analysis JSON:\n"
            f"{json.dumps(market_analysis, indent=2)}\n\n"
            "Here is the News Analysis JSON:\n"
            f"{json.dumps(news_analysis, indent=2)}\n\n"
            f"User Risk Profile: {user_risk_profile}\n\n"
            "Produce the risk assessment JSON."
        )
        return self.run(message)
