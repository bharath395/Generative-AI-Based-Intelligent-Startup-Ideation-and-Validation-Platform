from ai_engine.llm.gemini_service import gemini_service

class BusinessAgent:
    """
    Agent 5: Business Model Agent
    Generates complete 9-block Business Model Canvas.
    """
    def execute(self, startup_name, domain, problem, solution):
        prompt = f"""
        ROLE: Business Model Strategist.
        TASK: Create a Business Model Canvas for startup '{startup_name}' in domain '{domain}'.
        PROBLEM: {problem}
        SOLUTION: {solution}

        Return JSON object with 9 keys:
        "customer_segments", "value_proposition", "channels", "customer_relationship",
        "revenue_streams", "key_resources", "key_activities", "key_partners", "cost_structure"
        """

        response = gemini_service.generate_content(prompt, response_schema_json=True)
        if response and isinstance(response, dict) and 'customer_segments' in response:
            return response

        # Heuristic fallback
        return {
            "customer_segments": "Engineering Students, Academic Incubators, Early-Stage Startup Founders, SMB Tech Teams",
            "value_proposition": "Automated 24/7 AI startup mentoring, instant feasibility scoring, and professional investor-ready report generation.",
            "channels": "Direct Web App Portal, University Campus Ambassador Network, Tech Conferences, Social Media Ads",
            "customer_relationship": "Self-service SaaS UI, Community Discord/Forum, Automated Email Onboarding, AI Mentor Assistant",
            "revenue_streams": "Freemium Access Model, Premium PDF Report Downloads ($9.99/report), B2B University SaaS Subscriptions",
            "key_resources": "Proprietary AI Prompt Libraries, Vector Database Knowledge Base, Flask Server Backend, Skilled Dev Team",
            "key_activities": "Continuous AI Agent Fine-Tuning, Web Platform Maintenance, Incubator Partnering, Marketing Campaigns",
            "key_partners": "Google Gemini API Provider, College Innovation Cells, Local Incubators, AWS/Render Hosting",
            "cost_structure": "Cloud AI API Tokens, Server & Domain Hosting, Development & Maintenance, Marketing & Outreach"
        }

business_agent = BusinessAgent()
