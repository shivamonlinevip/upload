"""
Orchestrator (plain Python, not an LLM prompt).

Coordinates the flow:

User Input
  -> Market Agent
  -> News Agent
  -> Risk Agent
  -> Portfolio Agent
  -> Verifier Agent
  -> Explainability Agent
  -> Final Response
"""
from dataclasses import dataclass, field

from config import ENABLE_WEB_SEARCH
from agents import (
    MarketAgent,
    NewsAgent,
    RiskAgent,
    PortfolioAgent,
    VerifierAgent,
    ExplainabilityAgent,
)


@dataclass
class UserRequest:
    company: str
    budget: float
    duration: str
    risk_profile: str = "moderate"


@dataclass
class PipelineResult:
    request: UserRequest
    market_analysis: dict = field(default_factory=dict)
    news_analysis: dict = field(default_factory=dict)
    risk_assessment: dict = field(default_factory=dict)
    portfolio_recommendation: dict = field(default_factory=dict)
    verification: dict = field(default_factory=dict)
    explainability: dict = field(default_factory=dict)
    final_confidence: int = 0


class Orchestrator:
    def __init__(self):
        self.market_agent = MarketAgent()
        # News Agent benefits most from real-time web search
        self.news_agent = NewsAgent(use_web_search=ENABLE_WEB_SEARCH)
        self.risk_agent = RiskAgent()
        self.portfolio_agent = PortfolioAgent()
        self.verifier_agent = VerifierAgent()
        self.explainability_agent = ExplainabilityAgent()

    def run(self, request: UserRequest, verbose: bool = True) -> PipelineResult:
        result = PipelineResult(request=request)

        if verbose:
            print(f"\n[1/6] Market Agent analyzing {request.company}...")
        result.market_analysis = self.market_agent.analyze(request.company)

        if verbose:
            print("[2/6] News Agent gathering & analyzing news...")
        result.news_analysis = self.news_agent.analyze(request.company)

        if verbose:
            print("[3/6] Risk Agent assessing risk...")
        result.risk_assessment = self.risk_agent.analyze(
            result.market_analysis, result.news_analysis, request.risk_profile
        )

        if verbose:
            print("[4/6] Portfolio Agent building allocation...")
        result.portfolio_recommendation = self.portfolio_agent.recommend(
            request.budget,
            request.duration,
            request.risk_profile,
            result.market_analysis,
            result.news_analysis,
            result.risk_assessment,
        )

        if verbose:
            print("[5/6] Verifier Agent checking for issues...")
        result.verification = self.verifier_agent.verify(
            result.market_analysis,
            result.news_analysis,
            result.risk_assessment,
            result.portfolio_recommendation,
        )

        if verbose:
            print("[6/6] Explainability Agent writing plain-English explanation...\n")
        result.explainability = self.explainability_agent.explain(
            result.market_analysis,
            result.news_analysis,
            result.risk_assessment,
            result.portfolio_recommendation,
            result.verification,
        )

        result.final_confidence = self._compute_final_confidence(result)
        return result

    @staticmethod
    def _compute_final_confidence(result: PipelineResult) -> int:
        base_confidences = [
            result.market_analysis.get("confidence", 0),
            result.news_analysis.get("confidence", 0),
            result.risk_assessment.get("confidence", 0),
            result.portfolio_recommendation.get("confidence", 0),
        ]
        base_confidences = [c for c in base_confidences if isinstance(c, (int, float))]
        avg = sum(base_confidences) / len(base_confidences) if base_confidences else 0

        adjustment = result.verification.get("confidence_adjustment", 0)
        try:
            adjustment = float(adjustment)
        except (TypeError, ValueError):
            adjustment = 0

        final = avg + adjustment
        return max(0, min(100, round(final)))
