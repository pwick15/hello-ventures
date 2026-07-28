from pydantic import BaseModel, Field
from typing import Optional
from typing import Optional
from backend.pipeline.state import VentureState
from backend.pipeline.prompts import EXTRACTION_PROMPT
from backend.pipeline.llm import get_llm
from backend.pipeline.prompts import EXTRACTION_PROMPT

class VentureSignals(BaseModel):
    mission: Optional[str] = Field(None, description="Core mission statement")
    technology_focus: Optional[str] = Field(None, description="What technology they develop")
    sector: Optional[str] = Field(None, description="Primary industry sector")
    founding_year: Optional[int] = Field(None, description="Year founded")
    team_size: Optional[str] = Field(None, description="Approximate team size")
    funding_stage: Optional[str] = Field(None, description="Current funding stage")
    location: Optional[str] = Field(None, description="Headquarters location")
    key_products: Optional[list[str]] = Field(default_factory=list, description="Main products or services")
    notable_achievements: Optional[list[str]] = Field(default_factory=list, description="Significant milestones")

async def extract_node(state: VentureState) -> dict:
    llm = get_llm(VentureSignals)
    
    signals = await llm.ainvoke(EXTRACTION_PROMPT.format(
        name=state["name"],
        data=state.get("raw_enrichment", ""),
    ))
    
    return {
        "mission": signals.mission,
        "technology_focus": signals.technology_focus,
        "sector": signals.sector,
        "founding_year": signals.founding_year,
        "team_size": signals.team_size,
        "funding_stage": signals.funding_stage,
        "location": signals.location,
        "key_products": signals.key_products or [],
        "notable_achievements": signals.notable_achievements or [],
    }
