import json
from .base_agent import BaseAgent

SYSTEM_PROMPT = """You are Portfolio Recommendation Agent.

Inputs:
- User budget
- Investment duration
- Risk profile
- Market analysis
- News analysis
- Risk assessment

Your task is NOT to guarantee profits.

Construct a diversified investment suggestion.

Explain diversification.

Recommend percentage allocations (they must sum to 100).

Never promise returns.

Return ONLY valid JSON, no markdown fences, no preamble, in this exact format:

{
 "allocation": [
   {"asset": "", "percentage": 0}
 ],
 "expected_strategy": "",
 "investment_horizon": "",
 "warnings": [],
 "confidence": 0
}"""


class PortfolioAgent(BaseAgent):
    name = "Portfolio Agent"
    system_prompt = SYSTEM_PROMPT

    def recommend(
        self,
        budget: float,
        duration: str,
        risk_profile: str,
        market_analysis: dict,
        news_analysis: dict,
        risk_assessment: dict,
    ) -> dict:
        message = (
            f"User Budget: {budget}\n"
            f"Investment Duration: {duration}\n"
            f"Risk Profile: {risk_profile}\n\n"
            "Market Analysis JSON:\n"
            f"{json.dumps(market_analysis, indent=2)}\n\n"
            "News Analysis JSON:\n"
            f"{json.dumps(news_analysis, indent=2)}\n\n"
            "Risk Assessment JSON:\n"
            f"{json.dumps(risk_assessment, indent=2)}\n\n"
            "Produce the portfolio recommendation JSON."
        )
        return self.run(message)
