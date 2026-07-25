from ai_engine.llm.gemini_service import gemini_service
import json

class SkillAgent:
    """
    Skill Agent:
    Performs Skill Gap Analysis based on the required technologies and the user's existing skills.
    """
    def execute(self, required_tech, user_skills=""):
        prompt = f"""
        ROLE: You are an expert technical recruiter and CTO.
        TASK: Perform a Skill Gap Analysis comparing required technologies against user existing skills.

        REQUIRED TECHNOLOGY: {required_tech}
        USER'S EXISTING SKILLS: {user_skills if user_skills else "None provided"}

        Return a JSON object with keys:
        - "matching_skills": list of strings (skills user already has)
        - "missing_skills": list of strings (skills user needs to acquire)
        - "match_percentage": number (0 to 100)
        - "analysis_markdown": formatted markdown breakdown with recommendations
        """

        try:
            response = gemini_service.generate_content(prompt, response_schema_json=True)
            if response and isinstance(response, dict) and 'matching_skills' in response:
                return response
        except Exception:
            pass

        req_list = [s.strip() for s in str(required_tech).split(',') if s.strip()]
        user_list = [s.strip() for s in str(user_skills).split(',') if s.strip()]

        matching = [s for s in req_list if any(u.lower() in s.lower() for u in user_list)]
        missing = [s for s in req_list if s not in matching]

        if not missing and not matching:
            missing = req_list

        pct = int((len(matching) / max(1, len(req_list))) * 100) if user_list else 40

        return {
            "matching_skills": matching,
            "missing_skills": missing if missing else ["Advanced System Architecture"],
            "match_percentage": pct,
            "analysis_markdown": f"**Matching Skills:** {', '.join(matching) if matching else 'None'}\n\n**Skills to Acquire:** {', '.join(missing) if missing else 'All set!'}"
        }

skill_agent = SkillAgent()
