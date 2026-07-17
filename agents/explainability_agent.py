import json
from .base_agent import BaseAgent

SYSTEM_PROMPT = """You are Explainability Agent.

Your responsibility is to explain every recommendation in plain English.

For every conclusion explain:
1. Why this recommendation was generated.
2. Which evidence supported it.
3. Which news influenced it.
4. Which financial metrics influenced it.
5. Which risks were considered.
6. What assumptions were made.
7. What could change this recommendation.
8. What additional data would improve confidence.

Never hide uncertainty.

Return ONLY valid JSON, no markdown fences, no preamble, in this exact format:

{
 "summary": "",
 "reasoning": [],
 "evidence": [],
 "assumptions": [],
 "uncertainties": [],
 "alternative_scenarios": [],
 "confidence": 0
}"""


class ExplainabilityAgent(BaseAgent):
    name = "Explainability Agent"
    system_prompt = SYSTEM_PROMPT

    def explain(
        self,
        market_analysis: dict,
        news_analysis: dict,
        risk_assessment: dict,
        portfolio_recommendation: dict,
        verification: dict,
    ) -> dict:
        message = (
            "Explain the full recommendation chain below in plain English.\n\n"
            "Market Analysis JSON:\n"
            f"{json.dumps(market_analysis, indent=2)}\n\n"
            "News Analysis JSON:\n"
            f"{json.dumps(news_analysis, indent=2)}\n\n"
            "Risk Assessment JSON:\n"
            f"{json.dumps(risk_assessment, indent=2)}\n\n"
            "Portfolio Recommendation JSON:\n"
            f"{json.dumps(portfolio_recommendation, indent=2)}\n\n"
            "Verification JSON:\n"
            f"{json.dumps(verification, indent=2)}\n\n"
            "Produce the explainability JSON."
        )
        return self.run(message)
