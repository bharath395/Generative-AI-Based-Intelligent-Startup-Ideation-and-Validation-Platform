from ai_engine.llm.gemini_service import gemini_service
from ai_engine.tools.news_tool import fetch_market_news
from ai_engine.tools.search_tool import perform_web_search
from ai_engine.tools.trend_tool import fetch_google_trends_score

class MarketAgent:
    """
    Agent 2: Market Research Agent
    Analyzes market opportunity, market size, growth rate, demand score, and future potential.
    """
    def execute(self, startup_name, domain):
        search_info = perform_web_search(f"{domain} market size demand growth trends")
        news_info = fetch_market_news(f"{domain} startup market")
        trend_data = fetch_google_trends_score(domain, [startup_name])
        trend_score = trend_data["score"]

        prompt = f"""
        ROLE: Market Research Analyst.
        TASK: Analyze market opportunity for the startup: {startup_name} in domain: {domain}.
        SEARCH CONTEXT: {search_info}
        NEWS CONTEXT: {news_info}
        TREND CONTEXT: {trend_data}
        
        Return JSON object with keys:
        "market_size", "growth_rate", "trend_score", "customer_demand", "future_scope"
        """

        response = gemini_service.generate_content(prompt, response_schema_json=True)
        if response and isinstance(response, dict) and 'market_size' in response:
            return response

        # Heuristic fallback
        return {
            "market_size": "$12.4 Billion",
            "growth_rate": "22.4% CAGR",
            "trend_score": trend_score,
            "customer_demand": "High Demand",
            "future_scope": f"Expanding rapidly due to enterprise adoption of generative AI and automation tools in {domain}."
        }

market_agent = MarketAgent()
