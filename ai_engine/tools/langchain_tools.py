from langchain_core.tools import tool

from ai_engine.tools.news_tool import fetch_market_news
from ai_engine.tools.search_tool import perform_web_search, scrape_page_summary
from ai_engine.tools.trend_tool import fetch_google_trends_score


@tool
def startup_web_search(query: str) -> str:
    """Search the web for startup, market, and competitor context."""
    return str(perform_web_search(query, max_results=3))


@tool
def startup_trend_score(query: str) -> str:
    """Get a Google Trends or fallback trend score for a startup domain."""
    return str(fetch_google_trends_score(query))


@tool
def startup_market_news(query: str) -> str:
    """Fetch market news signals for a startup domain."""
    return str(fetch_market_news(query, max_results=3))


@tool
def startup_page_summary(url: str) -> str:
    """Extract a title and short summary from a web page."""
    return str(scrape_page_summary(url))


LANGCHAIN_STARTUP_TOOLS = [
    startup_web_search,
    startup_trend_score,
    startup_market_news,
    startup_page_summary,
]
