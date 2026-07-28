from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY, GEMINI_MODEL, SCORING_WEIGHTS, SCORE_LABELS
from backend.pipeline.state import VentureState
from backend.pipeline.prompts import RATIONALE_PROMPT

class VentureRationale(BaseModel):
    rationale: str = Field(description="2-3 sentence explanation of overall fit with ASME Ventures")
    strengths: list[str] = Field(description="List of 3 key strengths")
    weaknesses: list[str] = Field(description="List of 2-3 concerns or gaps")

async def aggregate_node(state: VentureState) -> dict:
    scores = state["scores"]
    overall = sum(scores[k] * SCORING_WEIGHTS[k] for k in SCORING_WEIGHTS)
    overall = round(overall, 2)
    
    score_label = SCORE_LABELS.get(round(overall), "Average")
    
    scores_summary = "\n".join(
        f"  - {k.replace('_', ' ').title()}: {v}/5" for k, v in scores.items()
    )
    
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GEMINI_API_KEY,
    ).with_structured_output(VentureRationale)
    
    result = await llm.ainvoke(RATIONALE_PROMPT.format(
        name=state["name"],
        scores_summary=scores_summary,
        overall=overall,
        score_label=score_label,
    ))
    
    return {
        "overall_score": overall,
        "rationale": result.rationale,
        "strengths": result.strengths,
        "weaknesses": result.weaknesses,
        "status": "scored",
    }
