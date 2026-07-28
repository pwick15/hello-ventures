from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from config.settings import LLM_PROVIDER, GEMINI_MODEL, GEMINI_API_KEY, OPENAI_MODEL, OPENAI_API_KEY

def get_llm(structured_schema=None):
    """Factory to get the configured LLM, optionally with a structured output schema."""
    if LLM_PROVIDER.lower() == "openai":
        llm = ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0
        )
    else:
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=0
        )
        
    if structured_schema:
        return llm.with_structured_output(structured_schema)
    return llm
