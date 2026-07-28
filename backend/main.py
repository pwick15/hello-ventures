import json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from config.settings import SCORING_WEIGHTS, MAX_ENRICHMENT_ROUNDS
from backend.database import init_db, get_all_ventures, get_venture, create_venture, update_venture, delete_venture
from backend.pipeline.graph import pipeline
from backend.seed_data import SEED_VENTURES

app = FastAPI(title="ASME Ventures - AI Venture Screener")

@app.on_event("startup")
async def startup():
    await init_db()

# --- API Models ---
class AnalyzeRequest(BaseModel):
    name: str
    website: str
    description: Optional[str] = None

class WeightsUpdate(BaseModel):
    technology_focus: float
    reindustrialization: float
    engineering_ip: float
    stage_fit: float
    geographic_reach: float

# --- API Routes ---
@app.get("/api/ventures")
async def list_ventures():
    ventures = await get_all_ventures()
    return {"ventures": ventures}

@app.get("/api/ventures/{venture_id}")
async def get_venture_detail(venture_id: int):
    venture = await get_venture(venture_id)
    if not venture:
        raise HTTPException(status_code=404, detail="Venture not found")
    return venture

@app.post("/api/ventures/analyze")
async def analyze_venture(req: AnalyzeRequest):
    print(f"\n🚀 Starting analysis for: {req.name}")
    # Create venture in DB
    venture = await create_venture(req.name, req.website, req.description)
    
    # Run through LangGraph pipeline
    try:
        initial_state = {
            "name": req.name,
            "website": req.website,
            "description": req.description,
            "enrichment_round": 0,
            "max_enrichment_rounds": MAX_ENRICHMENT_ROUNDS,
            "raw_enrichment": None,
            "follow_up_queries": None,
            "data_sufficient": False,
            "missing_topics": None,
            "mission": None,
            "technology_focus": None,
            "sector": None,
            "founding_year": None,
            "team_size": None,
            "funding_stage": None,
            "location": None,
            "key_products": None,
            "notable_achievements": None,
            "scores": None,
            "overall_score": None,
            "rationale": None,
            "strengths": None,
            "weaknesses": None,
            "status": "pending",
            "error": None,
        }
        
        result = await pipeline.ainvoke(initial_state)
        
        # Update venture in DB with results
        await update_venture(
            venture["id"],
            location=result.get("location"),
            founding_year=result.get("founding_year"),
            team_size=result.get("team_size"),
            funding_stage=result.get("funding_stage"),
            sector=result.get("sector"),
            enrichment_data=json.dumps({
                "mission": result.get("mission"),
                "technology_focus": result.get("technology_focus"),
                "key_products": result.get("key_products"),
                "notable_achievements": result.get("notable_achievements"),
                "enrichment_rounds": result.get("enrichment_round", 1),
            }),
            scores=json.dumps(result.get("scores")),
            overall_score=result.get("overall_score"),
            rationale=result.get("rationale"),
            strengths=json.dumps(result.get("strengths")),
            weaknesses=json.dumps(result.get("weaknesses")),
            status=result.get("status", "scored"),
        )
        
        print(f"✅ Completed analysis for {req.name} | Score: {result.get('overall_score')}/5.0")
        return await get_venture(venture["id"])
    except Exception as e:
        await update_venture(venture["id"], status="error")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ventures/seed")
async def seed_ventures():
    """Seed pre-curated ventures and run pipeline on all."""
    print("\n🌱 Starting batch seed process...")
    results = []
    
    existing = await get_all_ventures()
    existing_map = {v["name"]: v for v in existing}
    
    for idx, v in enumerate(SEED_VENTURES, 1):
        if v["name"] in existing_map:
            ex_v = existing_map[v["name"]]
            if ex_v["status"] == "scored":
                print(f"⏭️  [{idx}/{len(SEED_VENTURES)}] Skipping {v['name']} (already fully processed)")
                continue
            else:
                print(f"🗑️  [{idx}/{len(SEED_VENTURES)}] Removing previous failed/incomplete run for {v['name']}...")
                await delete_venture(ex_v["id"])
                
        print(f"⏳ [{idx}/{len(SEED_VENTURES)}] Processing {v['name']}...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = await analyze_venture(AnalyzeRequest(**v))
                results.append({"name": v["name"], "status": "success"})
                break
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    wait_time = 22  # Wait 22 seconds to clear the rate limit window
                    print(f"⚠️  Rate limit hit for {v['name']}. Waiting {wait_time}s before retry (Attempt {attempt+1}/{max_retries})...")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"❌ Error processing {v['name']}: {err_str}")
                    results.append({"name": v["name"], "status": "error", "error": err_str})
                    break
            
    print("✨ Seeding complete!\n")
    return {"results": results}

@app.get("/api/config/weights")
async def get_weights():
    return {"weights": SCORING_WEIGHTS}

@app.put("/api/config/weights")
async def update_weights(weights: WeightsUpdate):
    total = weights.technology_focus + weights.reindustrialization + weights.engineering_ip + weights.stage_fit + weights.geographic_reach
    if abs(total - 1.0) > 0.01:
        raise HTTPException(status_code=400, detail=f"Weights must sum to 1.0, got {total}")
    SCORING_WEIGHTS["technology_focus"] = weights.technology_focus
    SCORING_WEIGHTS["reindustrialization"] = weights.reindustrialization
    SCORING_WEIGHTS["engineering_ip"] = weights.engineering_ip
    SCORING_WEIGHTS["stage_fit"] = weights.stage_fit
    SCORING_WEIGHTS["geographic_reach"] = weights.geographic_reach
    return {"weights": SCORING_WEIGHTS}

# --- Static Files ---
import os
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))
