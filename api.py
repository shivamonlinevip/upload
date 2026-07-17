#!/usr/bin/env python3
"""
Thin HTTP API layer on top of the existing Orchestrator.

This does NOT change orchestrator.py, agents/, or config.py at all — it
just gives the web frontend a way to call orchestrator.run() over HTTP
instead of via the CLI in main.py.

Run it with:
    uvicorn api:app --reload --port 8000

Then open static/index.html (or visit http://localhost:8000/ if you use
the StaticFiles mount below) in your browser.
"""
from __future__ import annotations

import traceback
from dataclasses import asdict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from orchestrator import Orchestrator, UserRequest

app = FastAPI(title="Multi-Agent Financial Advisor API")

# Allow the frontend (served from a file:// page, or a different port like
# 5500/3000 during development) to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten this to your real frontend origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# One shared Orchestrator instance (agents are stateless per-call, so this is fine)
orchestrator = Orchestrator()


class AnalyzeRequest(BaseModel):
    company: str = Field(..., min_length=1, example="Tata Motors")
    budget: float = Field(..., gt=0, example=100000)
    duration: str = Field(..., min_length=1, example="5 years")
    risk_profile: str = Field("moderate", example="moderate")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    if req.risk_profile not in ("conservative", "moderate", "aggressive"):
        raise HTTPException(
            status_code=400,
            detail="risk_profile must be 'conservative', 'moderate', or 'aggressive'",
        )

    user_request = UserRequest(
        company=req.company,
        budget=req.budget,
        duration=req.duration,
        risk_profile=req.risk_profile,
    )

    try:
        # verbose=False so the [1/6] ... progress prints don't spam the server logs
        result = orchestrator.run(user_request, verbose=False)
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {exc}")

    return {
        "request": asdict(user_request),
        "market_analysis": result.market_analysis,
        "news_analysis": result.news_analysis,
        "risk_assessment": result.risk_assessment,
        "portfolio_recommendation": result.portfolio_recommendation,
        "verification": result.verification,
        "explainability": result.explainability,
        "final_confidence": result.final_confidence,
    }


# Optional: serve the frontend from the same server at http://localhost:8000/
# so you don't need a separate static file server. Comment out if not wanted.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
