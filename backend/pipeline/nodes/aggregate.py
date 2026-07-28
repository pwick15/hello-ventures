from pydantic import BaseModel, Field
from config.settings import SCORING_WEIGHTS, SCORE_LABELS
from backend.pipeline.state import VentureState
from backend.pipeline.prompts import RATIONALE_PROMPT
from backend.pipeline.llm import get_llm
from backend.pipeline.prompts import RATIONALE_PROMPT

class VentureRationale(BaseModel):
    rationale: str = Field(description="2-3 sentence explanation of overall fit with ASME Ventures")
    strengths: list[str] = Field(description="List of 3 key strengths")
    weaknesses: list[str] = Field(description="List of 2-3 concerns or gaps")

async def aggregate_node(state: VentureState) -> dict:
    scores = state["scores"]
    overall = sum(scores[k] * SCORING_WEIGHTS[k] for k in SCORING_WEIGHTS)
    overall = round(overall, 2)
    
    if overall >= 4.5:
        score_label = "Exceptional"
    elif overall >= 4.0:
        score_label = "Strong"
    elif overall >= 3.5:
        score_label = "Promising"
    elif overall >= 2.5:
        score_label = "Average"
    elif overall >= 1.5:
        score_label = "Weak"
    else:
        score_label = "Poor"
    
    scores_summary = "\n".join(
        f"  - {k.replace('_', ' ').title()}: {v}/5" for k, v in scores.items()
    )
    
    llm = get_llm(VentureRationale)
    
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
