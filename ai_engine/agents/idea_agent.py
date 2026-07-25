from ai_engine.llm.gemini_service import gemini_service

class IdeaAgent:
    """
    Agent 1: Startup Idea Generation Agent
    Generates innovative startup concepts based on student domain, skills, budget, and interest.
    """
    def execute(self, domain="", budget="50000", target_customers="", business_type="", goal="", skills="", preferred_tech="", location=""):
        domain = domain.strip() if domain else "Artificial Intelligence & Automation"
        budget = budget.strip() if budget else "$25,000"
        target_customers = target_customers.strip() if target_customers else "Students & Small Businesses"
        business_type = business_type.strip() if business_type else "SaaS Platform"
        goal = goal.strip() if goal else f"automate manual tasks and increase efficiency in {domain}"

        prompt = f"""

        ROLE: You are an expert startup incubator mentor and innovation consultant.
        TASK: Generate THREE (3) distinct, creative, and viable startup ideas based on the user's input.

        INPUT DETAILS:
        - Area of Interest / Domain: {domain}
        - Budget: {budget}
        - Target Customers: {target_customers}
        - Business Goal / Problem: {goal}
        - Preferred Business Type: {business_type}
        - User's Existing Skills: {skills if skills else "Not specified"}
        - Preferred Technology: {preferred_tech if preferred_tech else "Any modern stack"}
        - Location: {location if location else "Global"}

        Return a JSON object with a single key "ideas" containing an array of 3 distinct startup objects.
        Each object MUST have:
        - "id": number (1, 2, or 3)
        - "startup_name": short catchy startup name
        - "tagline": 1-line pitch
        - "problem": problem statement targeted at {target_customers}
        - "solution": AI/Tech solution solving {goal}
        - "technology": required technical stack (comma separated)
        - "target_customer": target customer segment
        - "innovation_score": number between 75 and 98
        """

        try:
            response = gemini_service.generate_content(prompt, response_schema_json=True)
            if response and isinstance(response, dict) and 'ideas' in response and isinstance(response['ideas'], list) and len(response['ideas']) > 0:
                return response['ideas']
        except Exception:
            pass

        # Heuristic fallback: 3 distinct ideas
        clean_domain = domain.capitalize() if domain else "Technology"
        clean_goal = goal if goal else f"optimize {clean_domain.lower()} workflows"
        clean_tech = preferred_tech if preferred_tech else (skills if skills else "AI, Web/Mobile")

        tagline_1 = f"AI Automation to {goal}" if goal else f"AI-Powered Automation for {clean_domain}"

        return [
            {
                "id": 1,
                "startup_name": f"Smart {clean_domain} Hub",
                "tagline": tagline_1,
                "problem": f"Current solutions in {clean_domain} are manual, slow, and expensive.",
                "solution": f"An automated {business_type if business_type else 'SaaS'} platform leveraging smart agents.",
                "technology": f"{clean_tech}, Python, Cloud APIs",
                "target_customer": target_customers if target_customers else f"SMBs in {clean_domain}",
                "innovation_score": 92.0
            },
            {
                "id": 2,
                "startup_name": f"{clean_domain} Pulse AI",
                "tagline": f"Predictive Analytics & Monitoring for {clean_domain}",
                "problem": f"Lack of real-time visibility and proactive insights for {target_customers if target_customers else 'users'}.",
                "solution": f"Real-time IoT & AI monitoring dashboard for instant anomaly detection.",
                "technology": f"IoT Sensors, Python, React, Data Analytics",
                "target_customer": target_customers if target_customers else f"Enterprise clients in {clean_domain}",
                "innovation_score": 87.5
            },
            {
                "id": 3,
                "startup_name": f"Eco{clean_domain} Direct",
                "tagline": f"Decentralized & Low-Cost {clean_domain} Assistant",
                "problem": f"High operational costs and resource wastage in traditional {clean_domain} practices.",
                "solution": f"Mobile-first assistant providing automated resource optimization recommendations.",
                "technology": f"Mobile App, Flutter, Lightweight ML models",
                "target_customer": target_customers if target_customers else f"Individual users & small teams",
                "innovation_score": 85.0
            }
        ]

idea_agent = IdeaAgent()
