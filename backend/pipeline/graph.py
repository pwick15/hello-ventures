from langgraph.graph import StateGraph, END
from backend.pipeline.state import VentureState
from backend.pipeline.nodes import enrich, quality_check, extract, score, aggregate

def should_continue_enrichment(state: VentureState) -> str:
    if state.get("data_sufficient", False):
        return "extract"
    if state.get("enrichment_round", 0) >= state.get("max_enrichment_rounds", 3):
        return "extract"
    return "enrich"

def build_pipeline():
    graph = StateGraph(VentureState)
    
    graph.add_node("enrich", enrich.enrich_node)
    graph.add_node("quality_check", quality_check.quality_check_node)
    graph.add_node("extract", extract.extract_node)
    graph.add_node("score", score.score_node)
    graph.add_node("aggregate", aggregate.aggregate_node)
    
    graph.set_entry_point("enrich")
    graph.add_edge("enrich", "quality_check")
    graph.add_conditional_edges(
        "quality_check",
        should_continue_enrichment,
        {"enrich": "enrich", "extract": "extract"}
    )
    graph.add_edge("extract", "score")
    graph.add_edge("score", "aggregate")
    graph.add_edge("aggregate", END)
    
    return graph.compile()

pipeline = build_pipeline()
