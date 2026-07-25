import logging
from ai_engine.agents.idea_agent import idea_agent
from ai_engine.agents.market_agent import market_agent
from ai_engine.agents.competitor_agent import competitor_agent
from ai_engine.agents.validation_agent import validation_agent
from ai_engine.agents.business_agent import business_agent
from ai_engine.agents.finance_agent import finance_agent
from ai_engine.agents.risk_agent import risk_agent
from ai_engine.agents.pitch_agent import pitch_agent
from ai_engine.agents.report_agent import report_agent

logger = logging.getLogger(__name__)

class AIOrchestrator:
    """
    AI Orchestrator Agent:
    Coordinates multi-agent flow, passing inputs and outputs between agents sequentially or on demand.
    """
    def run_full_pipeline(self, domain, budget="50000", target_customers="", business_type="", goal="", skills="", preferred_tech="", location=""):
        # 1. AI Idea Generation (Generates 3 Ideas)
        try:
            ideas_list = idea_agent.execute(domain, budget, target_customers, business_type, goal, skills, preferred_tech, location)
        except Exception as e:
            logger.error(f"Error in idea_agent: {e}")
            ideas_list = [
                {
                    "id": 1,
                    "startup_name": f"Smart {domain} Hub",
                    "tagline": "AI-Driven Automation",
                    "problem": goal if goal else "Manual workflows",
                    "solution": "Automated AI platform",
                    "technology": preferred_tech if preferred_tech else "Python, Web",
                    "target_customer": target_customers if target_customers else "Students and SMBs",
                    "innovation_score": 92.0
                }
            ]

        if not isinstance(ideas_list, list) or len(ideas_list) == 0:
            ideas_list = [{
                "id": 1,
                "startup_name": f"Smart {domain} Assistant",
                "tagline": "Automated Assistant",
                "problem": goal if goal else "Manual tasks",
                "solution": "Smart AI Workflow",
                "technology": preferred_tech if preferred_tech else "Python",
                "target_customer": target_customers if target_customers else "General",
                "innovation_score": 88.0
            }]

        from ai_engine.agents.skill_agent import skill_agent
        # 2. Compute Skill Gap Analysis for all generated ideas
        for idea in ideas_list:
            req_tech = idea.get('technology', preferred_tech)
            try:
                idea['skill_gap'] = skill_agent.execute(req_tech, skills)
            except Exception as e:
                logger.error(f"Error in skill_agent for idea {idea.get('id')}: {e}")
                idea['skill_gap'] = {
                    "matching_skills": [],
                    "missing_skills": [req_tech],
                    "match_percentage": 50,
                    "analysis_markdown": f"Recommended Skills: {req_tech}"
                }

        # Select primary idea for deep dive validation
        primary_idea = ideas_list[0]
        startup_name = primary_idea.get('startup_name', f"Smart {domain} Startup")

        # 3. Market Research
        try:
            market_res = market_agent.execute(startup_name, domain)
        except Exception as e:
            logger.error(f"Error in market_agent: {e}")
            market_res = {}

        # 4. Competitor Analysis
        try:
            competitors = competitor_agent.execute(startup_name, domain)
        except Exception as e:
            logger.error(f"Error in competitor_agent: {e}")
            competitors = []

        # 5. Validation Scoring
        try:
            validation_res = validation_agent.execute(
                innovation_score=primary_idea.get('innovation_score', 90.0),
                market_score=market_res.get('trend_score', 85.0),
                tech_score=82.0,
                biz_score=88.0
            )
        except Exception as e:
            logger.error(f"Error in validation_agent: {e}")
            validation_res = {}

        # 6. Business Model Canvas
        try:
            business_res = business_agent.execute(
                startup_name, domain, primary_idea.get('problem', ''), primary_idea.get('solution', '')
            )
        except Exception as e:
            logger.error(f"Error in business_agent: {e}")
            business_res = {}

        # 7. Financial Planning
        try:
            finance_res = finance_agent.execute(budget=budget)
        except Exception as e:
            logger.error(f"Error in finance_agent: {e}")
            finance_res = {}

        # 8. Risk Analysis
        try:
            risk_res = risk_agent.execute(domain, primary_idea.get('technology', ''))
        except Exception as e:
            logger.error(f"Error in risk_agent: {e}")
            risk_res = {}

        # 9. AI Suggestions & SWOT
        from ai_engine.agents.suggestion_agent import suggestion_agent
        try:
            swot_res = suggestion_agent.execute(
                startup_name, domain, primary_idea.get('problem', ''), primary_idea.get('solution', ''), location
            )
        except Exception as e:
            logger.error(f"Error in suggestion_agent: {e}")
            swot_res = ""

        # 10. Pitch Generation
        try:
            pitch_res = pitch_agent.execute(
                startup_name, domain, primary_idea.get('problem', ''), primary_idea.get('solution', '')
            )
        except Exception as e:
            logger.error(f"Error in pitch_agent: {e}")
            pitch_res = {}

        return {
            "ideas": ideas_list,
            "primary_idea": primary_idea,
            "idea": primary_idea, # backwards compatibility
            "market": market_res,
            "competitors": competitors,
            "validation": validation_res,
            "business_model": business_res,
            "financials": finance_res,
            "risk": risk_res,
            "swot": swot_res,
            "pitch": pitch_res
        }

orchestrator = AIOrchestrator()
