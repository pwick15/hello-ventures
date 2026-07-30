import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- LLM Provider Selection ---
# Options: "gemini" or "openai"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# --- Models ---
GEMINI_MODEL = "gemini-3.6-flash"
OPENAI_MODEL = "gpt-5.4-mini"

# --- Database ---
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "ventures.db")

# --- Scoring Scale: 1-5 ---
# 1 = Poor alignment | 2 = Weak | 3 = Average | 4 = Strong | 5 = Exceptional
SCORE_MIN = 1
SCORE_MAX = 5

# Scoring weights (must sum to 1.0) — adjustable via API
SCORING_WEIGHTS = {
    "focus_area_alignment": 0.25,        # Fits the 5 specific tech areas
    "built_world_impact": 0.25,     # Advance human progress in the built world
    "engineering_innovation": 0.20, # Intersection of engineering and innovation
    "early_stage_fit": 0.15,        # Early-stage focus
    "asme_synergy": 0.15,           # Can leverage ASME's domain expertise & network
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
ASME Ventures is a wholly owned, for-profit subsidiary of the American Society of Mechanical Engineers (ASME).
We invest in visionary founders and breakthrough technologies that advance human progress in the built world.
Backed by over a century of leadership in mechanical engineering, we bring deep domain expertise and a global network.

Areas of Focus: Early-stage startups at the intersection of engineering and innovation.
- Digital Solutions: Advanced tools that amplify technical expertise and improve outcomes.
- Intelligent Automation: Next generation robotics, autonomous systems, and process optimization.
- Hardware Design & Operations: Smarter engineering tools and deep operational intelligence.
- Advanced Energy & Storage: Sustainable technologies that power the next wave of industrial transformation.
- Next-Gen Safety Tech: Enhancing human-AI collaboration, inspection and safety.
"""
