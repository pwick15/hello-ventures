# ASME Ventures - AI Venture Screening Tool

Scope: MVP

## Project Context
Built as a rapid prototype to demonstrate capability to ASME Ventures.
Goal: AI-driven pipeline to identify, screen, and rank potential venture partners.

## Session Notes
- Build window: ~1.5 hours
- Demo target: Next day interview
- Web app: Simple, minimal, clean (not fancy)
- Stack: Python (FastAPI) + SQLite + LangChain/LangGraph + Gemini + Tavily

## Architecture Decisions
- **AI Orchestration**: LangChain + LangGraph with conditional edges
- **Search**: Tavily Search API (primary) — no Gemini grounding, zero hallucination risk
- **Analysis**: Gemini 2.5 Flash (via LangChain) — analysis only, never for data sourcing
- **Scoring**: 1-5 scale (Poor/Weak/Average/Strong/Exceptional), weighted rubric
- **Pipeline**: Adaptive enrichment loop (enrich → quality check → loop or proceed)
- **Frontend**: Plain HTML/CSS/JS served by FastAPI
- **Database**: SQLite via aiosqlite
- **Auth/Security**: None (local demo only)

## Key Criteria (ASME Ventures Screening)
1. Technology Focus (25%) — Deep-tech / hardware alignment
2. Reindustrialization (25%) — Impact on essential industries
3. Engineering IP (20%) — IP strength + technical credibility
4. Stage Fit (15%) — Early→growth alignment
5. Geographic Reach (15%) — Global / multi-market presence
