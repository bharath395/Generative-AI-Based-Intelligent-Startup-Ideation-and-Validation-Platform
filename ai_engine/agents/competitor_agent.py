from ai_engine.llm.gemini_service import gemini_service
from ai_engine.tools.search_tool import perform_web_search

class CompetitorAgent:
    """
    Agent 3: Competitor Analysis Agent
    Finds existing companies, products, strengths, weaknesses, technology, and market gaps.
    """
    def execute(self, startup_name, domain):
        search_data = perform_web_search(f"Top competitors in {domain}")

        prompt = f"""
        ROLE: Competitive Intelligence Analyst.
        TASK: Identify 4 to 5 top competitors for a startup named '{startup_name}' in domain '{domain}'.
        SEARCH CONTEXT: {search_data}

        Return JSON object with key "competitors" containing list of 4-5 objects with:
        "company_name", "product_name", "website", "strength", "weakness", "technology", "pricing" (formatted in Indian Rupees e.g. ₹9,999/month).
        """

        response = gemini_service.generate_content(prompt, response_schema_json=True)
        if response and isinstance(response, dict) and 'competitors' in response:
            return response.get('competitors', [])

        # Heuristic fallback (5 competitors in INR)
        return [
            {
                "company_name": f"{domain} Enterprise Corp",
                "product_name": "Enterprise Suite Pro",
                "website": "https://example.com",
                "strength": "Established national distribution",
                "weakness": "Expensive licensing and slow setup",
                "technology": "Cloud Infrastructure",
                "pricing": "₹49,999/month"
            },
            {
                "company_name": "AgileTech Systems",
                "product_name": "FlexiApp Lite",
                "website": "https://example.com",
                "strength": "Low entry price point",
                "weakness": "Lacks real-time AI automation",
                "technology": "Web APIs",
                "pricing": "₹9,999/month"
            },
            {
                "company_name": "NextGen Innovations",
                "product_name": "SmartMatrix AI",
                "website": "https://example.com",
                "strength": "Modern user interface",
                "weakness": "Limited third-party integrations",
                "technology": "React & Python",
                "pricing": "₹19,999/month"
            },
            {
                "company_name": "OmniSolution Labs",
                "product_name": "OmniHub Platform",
                "website": "https://example.com",
                "strength": "Strong analytics reporting",
                "weakness": "Requires specialized IT staff",
                "technology": "Kubernetes & Microservices",
                "pricing": "₹34,999/month"
            },
            {
                "company_name": "VentureScale India",
                "product_name": "VentureStart MVP",
                "website": "https://example.com",
                "strength": "Tailored for Indian startups",
                "weakness": "No automated investor pitch deck builder",
                "technology": "Node.js & Postgres",
                "pricing": "₹3,999/month"
            }
        ]


competitor_agent = CompetitorAgent()
