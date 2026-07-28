from tavily import AsyncTavilyClient
from config.settings import TAVILY_API_KEY
from backend.pipeline.state import VentureState

INITIAL_QUERY_TEMPLATES = [
    "{name} company overview technology products",
    "{name} funding stage investors team size",
    "{name} partnerships achievements milestones",
]

async def enrich_node(state: VentureState) -> dict:
    client = AsyncTavilyClient(api_key=TAVILY_API_KEY)
    round_num = state.get("enrichment_round", 0)
    
    if round_num == 0:
        queries = [q.format(name=state["name"]) for q in INITIAL_QUERY_TEMPLATES]
    else:
        queries = state.get("follow_up_queries", [])
    
    new_results = []
    for query in queries:
        try:
            response = await client.search(
                query=query,
                search_depth="advanced",
                max_results=5,
            )
            new_results.extend(response.get("results", []))
        except Exception as e:
            print(f"Search error for query '{query}': {e}")
    
    new_content = "\n\n".join(
        f"Source: {r.get('url', 'unknown')}\n{r.get('content', '')}" for r in new_results
    )
    existing = state.get("raw_enrichment", "") or ""
    combined = f"{existing}\n\n{new_content}".strip() if existing else new_content
    
    return {
        "raw_enrichment": combined,
        "enrichment_round": round_num + 1,
        "status": "enriched",
    }
