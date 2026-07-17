import json
from .base_agent import BaseAgent

SYSTEM_PROMPT = """You are Verification Agent.

Your task is to verify every conclusion produced by previous agents.

Check:
- Unsupported claims
- Hallucinated facts
- Missing evidence
- Logical contradictions
- Overconfidence

If evidence is weak, reduce confidence.

Return ONLY valid JSON, no markdown fences, no preamble, in this exact format:

{
 "verified": true,
 "issues": [],
 "confidence_adjustment": 0,
 "verification_notes": ""
}"""


class VerifierAgent(BaseAgent):
    name = "Verifier Agent"
    system_prompt = SYSTEM_PROMPT

    def verify(
        self,
        market_analysis: dict,
        news_analysis: dict,
        risk_assessment: dict,
        portfolio_recommendation: dict,
    ) -> dict:
        message = (
            "Review the following agent outputs for unsupported claims, "
            "hallucinated facts, missing evidence, contradictions, or overconfidence.\n\n"
            "Market Analysis JSON:\n"
            f"{json.dumps(market_analysis, indent=2)}\n\n"
            "News Analysis JSON:\n"
            f"{json.dumps(news_analysis, indent=2)}\n\n"
            "Risk Assessment JSON:\n"
            f"{json.dumps(risk_assessment, indent=2)}\n\n"
            "Portfolio Recommendation JSON:\n"
            f"{json.dumps(portfolio_recommendation, indent=2)}\n\n"
            "Produce the verification JSON."
        )
        return self.run(message)
