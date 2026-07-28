import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- Model ---
GEMINI_MODEL = "gemini-2.5-flash"

# --- Database ---
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "ventures.db")

# --- Scoring Scale: 1-5 ---
# 1 = Poor alignment | 2 = Weak | 3 = Average | 4 = Strong | 5 = Exceptional
SCORE_MIN = 1
SCORE_MAX = 5

# Scoring weights (must sum to 1.0) — adjustable via API
SCORING_WEIGHTS = {
    "technology_focus": 0.25,       # Deep-tech / hardware alignment
    "reindustrialization": 0.25,    # Impact on essential industries
    "engineering_ip": 0.20,         # IP strength + technical credibility
    "stage_fit": 0.15,              # Early→growth stage alignment
    "geographic_reach": 0.15,       # Global / multi-market presence
}

SCORE_LABELS = {
    1: "Poor",
    2: "Weak",
    3: "Average",
    4: "Strong",
    5: "Exceptional",
}

# --- Enrichment ---
MAX_ENRICHMENT_ROUNDS = 3

# --- ASME Context ---
ASME_CONTEXT = """
ASME Ventures is the strategic venture arm of the American Society of Mechanical Engineers (ASME).
They support founders building breakthrough engineering and deep-tech solutions, specifically
focused on reindustrializing essential industries. Target sectors include: hardware, energy,
robotics, advanced manufacturing, materials, and physical-world engineering technologies.
Beyond capital, ASME provides domain expertise, standards alignment, and engineering validation.
Stage focus: early-stage to growth deep-tech startups transitioning from R&D to commercial deployment.
"""
