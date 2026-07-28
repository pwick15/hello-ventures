from pydantic import BaseModel, Field
from config.settings import ASME_CONTEXT
from backend.pipeline.state import VentureState
from backend.pipeline.prompts import SCORING_PROMPT
from backend.pipeline.llm import get_llm
from backend.pipeline.prompts import SCORING_PROMPT

class VentureScores(BaseModel):
    technology_focus: int = Field(description="1-5: Deep-tech/hardware alignment")
    reindustrialization: int = Field(description="1-5: Potential to modernize essential industries")
    engineering_ip: int = Field(description="1-5: Engineering IP strength and credibility")
    stage_fit: int = Field(description="1-5: Stage alignment with ASME target")
    geographic_reach: int = Field(description="1-5: Global/multi-market presence")

async def score_node(state: VentureState) -> dict:
    llm = get_llm(VentureScores)
    
    venture_data = f"""Name: {state['name']}
Website: {state.get('website', 'N/A')}
Mission: {state.get('mission', 'N/A')}
Technology Focus: {state.get('technology_focus', 'N/A')}
Sector: {state.get('sector', 'N/A')}
Founding Year: {state.get('founding_year', 'N/A')}
Team Size: {state.get('team_size', 'N/A')}
Funding Stage: {state.get('funding_stage', 'N/A')}
Location: {state.get('location', 'N/A')}
Key Products: {', '.join(state.get('key_products', []))}
Notable Achievements: {', '.join(state.get('notable_achievements', []))}"""
    
    scores = await llm.ainvoke(SCORING_PROMPT.format(
        context=ASME_CONTEXT,
        name=state["name"],
        venture_data=venture_data,
    ))
    
    scores_dict = scores.model_dump()
    # Clamp scores to 1-5 range
    for key in scores_dict:
        scores_dict[key] = max(1, min(5, scores_dict[key]))
    
    return {"scores": scores_dict}
