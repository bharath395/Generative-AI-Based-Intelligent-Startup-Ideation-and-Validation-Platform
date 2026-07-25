from ai_engine.llm.gemini_service import gemini_service
from ai_engine.rag.retriever import retriever_instance
from ai_engine.memory.memory_manager import memory_manager

class MentorAgent:
    """
    Agent 9: AI Startup Mentor Chat Agent
    Provides 24/7 interactive startup guidance using conversation context and RAG knowledge retrieval.
    """
    def execute(self, user_id, user_message):
        # Retrieve relevant RAG context
        rag_docs = retriever_instance.query(user_message, top_k=2)
        context_str = "\n".join([f"- {d['title']}: {d['content']}" for d in rag_docs])

        # Save user message to memory
        memory_manager.add_message(user_id, "user", user_message)
        history = memory_manager.get_history(user_id)

        prompt = f"""
        ROLE: You are an expert 24/7 AI Startup Mentor & Consultant advising engineering students.
        RELEVANT KNOWLEDGE BASE:
        {context_str}

        CONVERSATION HISTORY:
        {history}

        USER QUESTION: {user_message}

        Provide a supportive, structured, actionable response with bullet points and concrete business guidance.
        """

        response = gemini_service.generate_content(prompt, response_schema_json=False)
        if response and isinstance(response, str) and len(response.strip()) > 10:
            memory_manager.add_message(user_id, "assistant", response)
            return response

        # Heuristic fallback
        reply = (
            f"Hello! As your AI Startup Mentor, regarding '{user_message}':\n\n"
            f"1. **Validation First**: Ensure you interview at least 15 target users in your target market to confirm the problem is urgent.\n"
            f"2. **Build an MVP**: Focus on a simple, fast web application built with Flask or HTML/JS to demonstrate the core value proposition.\n"
            f"3. **Financial Planning**: Keep initial operational costs low by leveraging cloud free-tier hosting (like Render) and open-source libraries.\n\n"
            f"What specific area would you like to explore next—market sizing, pitch presentation, or competitor comparison?"
        )

        memory_manager.add_message(user_id, "assistant", reply)
        return reply

mentor_agent = MentorAgent()
