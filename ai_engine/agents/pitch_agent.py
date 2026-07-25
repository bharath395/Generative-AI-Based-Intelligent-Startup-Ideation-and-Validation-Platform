from ai_engine.llm.gemini_service import gemini_service

class PitchAgent:
    """
    Agent 8: Pitch Deck Generation Agent
    Generates investor pitch deck content.
    """
    def execute(self, startup_name, domain, problem, solution):
        prompt = f"""
        ROLE: Pitch Deck Expert.
        TASK: Create pitch deck content for '{startup_name}' in domain '{domain}'.
        PROBLEM: {problem}
        SOLUTION: {solution}

        Return JSON object with keys:
        "startup_name", "tagline", "problem", "solution", "market_opportunity",
        "business_model", "investment_requirement", "future_vision"
        """

        response = gemini_service.generate_content(prompt, response_schema_json=True)
        if response and isinstance(response, dict) and 'tagline' in response:
            return response

        # Heuristic fallback
        return {
            "startup_name": startup_name,
            "tagline": f"Empowering the Next Generation of {domain} Innovation with AI",
            "problem": problem,
            "solution": solution,
            "market_opportunity": f"$10B+ global market with 20%+ annual growth in {domain}.",
            "business_model": "Freemium SaaS subscription with premium analytics and report export options.",
            "investment_requirement": "$50,000 for initial 12-month platform development and user acquisition.",
            "future_vision": f"To become the premiere global AI ecosystem for {domain} ideation, incubation, and scaling."
        }

pitch_agent = PitchAgent()
