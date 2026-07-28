QUALITY_CHECK_PROMPT = """You are assessing data completeness for venture evaluation.
We are evaluating "{name}" for ASME Ventures (round {round_num} of data collection).

To meaningfully score this venture, we need data covering:
1. Technology/product details (what they build)
2. Company basics (founding year, location, team size)
3. Funding/stage information
4. Industry partnerships or achievements
5. Market presence and geographic reach

Review the data collected so far and determine if we have sufficient information to meaningfully evaluate this venture across all 5 ASME screening criteria. If not, identify the specific topics we still need data on (be concise — just the topic keywords).

Data collected so far:
{data}"""

EXTRACTION_PROMPT = """Extract structured information about the company "{name}" from the following web research data.
This is real web search data, not generated content. Extract ONLY what is explicitly stated or can be directly inferred. If information is not available, use null.

Research data:
{data}"""

SCORING_PROMPT = """You are an expert venture analyst for ASME Ventures.

{context}

Evaluate the following venture against ASME Ventures' screening criteria.
Score each dimension on a 1-5 scale:
  5 = Exceptional alignment — outstanding match, top-tier
  4 = Strong alignment — clear fit with minor gaps
  3 = Average — neither strong nor weak, neutral fit
  2 = Weak alignment — limited fit, notable concerns
  1 = Poor alignment — fundamental misalignment

Be rigorous and evidence-based. Only score based on the data provided. If data is insufficient for a dimension, score it 3 (average) and note the uncertainty.

Venture: {name}
Venture Data:
{venture_data}"""

RATIONALE_PROMPT = """You are an expert venture analyst for ASME Ventures.
Given these scores for "{name}":

{scores_summary}

Overall weighted score: {overall}/5.0 — {score_label}

Generate:
1. A concise 2-3 sentence rationale explaining the overall fit with ASME Ventures
2. A list of 3 key strengths
3. A list of 2-3 concerns or gaps

Be specific and evidence-based. Reference actual characteristics of the venture."""
