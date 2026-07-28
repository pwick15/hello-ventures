from pydantic import BaseModel, Field
from backend.pipeline.state import VentureState
from backend.pipeline.prompts import QUALITY_CHECK_PROMPT
from backend.pipeline.llm import get_llm
from backend.pipeline.prompts import QUALITY_CHECK_PROMPT

class QualityAssessment(BaseModel):
    sufficient: bool = Field(description="True if we have enough data to meaningfully evaluate this venture across all 5 ASME criteria")
    missing_topics: list[str] = Field(default_factory=list, description="Specific topics we lack data on, e.g. 'funding history', 'team background', 'IP portfolio'. Empty if sufficient.")
    confidence: str = Field(description="low, medium, or high — confidence in the data quality")

async def quality_check_node(state: VentureState) -> dict:
    llm = get_llm(QualityAssessment)
    
    assessment = await llm.ainvoke(QUALITY_CHECK_PROMPT.format(
        name=state["name"],
        data=state.get("raw_enrichment", ""),
        round_num=state.get("enrichment_round", 1),
    ))
    
    return {
        "data_sufficient": assessment.sufficient,
        "missing_topics": assessment.missing_topics,
        "follow_up_queries": [
            f"{state['name']} {topic}" for topic in assessment.missing_topics
        ] if not assessment.sufficient else [],
    }
