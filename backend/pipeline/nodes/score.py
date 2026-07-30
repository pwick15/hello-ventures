from pydantic import BaseModel, Field
from config.settings import ASME_CONTEXT
from backend.pipeline.state import VentureState
from backend.pipeline.prompts import SCORING_PROMPT
from backend.pipeline.llm import get_llm
from backend.pipeline.prompts import SCORING_PROMPT

class VentureScores(BaseModel):
    focus_area_alignment: int = Field(description="1-5: Alignment with Digital Solutions, Intelligent Automation, Hardware, Energy, or Safety Tech")
    built_world_impact: int = Field(description="1-5: Potential to advance human progress in the built world and industrial transformation")
    engineering_innovation: int = Field(description="1-5: Intersection of engineering and innovation, deep operational intelligence")
    early_stage_fit: int = Field(description="1-5: Alignment with early-stage investment focus")
    asme_synergy: int = Field(description="1-5: Ability to leverage ASME's domain expertise and global network")

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
