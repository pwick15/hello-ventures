from typing import TypedDict, Optional

class VentureState(TypedDict):
    name: str
    website: str
    description: Optional[str]
    enrichment_round: int
    max_enrichment_rounds: int
    raw_enrichment: Optional[str]
    follow_up_queries: Optional[list[str]]
    data_sufficient: bool
    missing_topics: Optional[list[str]]
    mission: Optional[str]
    technology_focus: Optional[str]
    sector: Optional[str]
    founding_year: Optional[int]
    team_size: Optional[str]
    funding_stage: Optional[str]
    location: Optional[str]
    key_products: Optional[list[str]]
    notable_achievements: Optional[list[str]]
    scores: Optional[dict]
    overall_score: Optional[float]
    rationale: Optional[str]
    strengths: Optional[list[str]]
    weaknesses: Optional[list[str]]
    status: str
    error: Optional[str]
