DEFAULT_KNOWLEDGE_BASE = [
    {
        "category": "Startup Knowledge",
        "title": "SaaS B2B Pricing Models",
        "content": "Tiered subscription pricing ($29/mo, $99/mo, $299/enterprise) yields 80%+ gross margins for AI applications."
    },
    {
        "category": "Agritech Knowledge",
        "title": "Smart Farming Trends",
        "content": "IoT soil sensors paired with AI predictive crop yield models reduce fertilizer waste by 35% and boost farmer productivity."
    },
    {
        "category": "EdTech Knowledge",
        "title": "AI Learning Assistants",
        "content": "Personalized student tutoring bots increase course completion rates by 42% through interactive flashcards and quiz feedback."
    },
    {
        "category": "Healthcare Knowledge",
        "title": "Predictive Diagnostics",
        "content": "Early symptom checker apps using mobile vision AI reduce clinic queue wait times and facilitate telehealth triage."
    }
]

def load_knowledge_documents():
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except Exception:
        return DEFAULT_KNOWLEDGE_BASE

    splitter = RecursiveCharacterTextSplitter(chunk_size=450, chunk_overlap=60)
    chunked_docs = []
    for doc in DEFAULT_KNOWLEDGE_BASE:
        chunks = splitter.split_text(doc["content"])
        for index, chunk in enumerate(chunks):
            chunked_docs.append({
                **doc,
                "title": doc["title"] if len(chunks) == 1 else f"{doc['title']} Part {index + 1}",
                "content": chunk,
            })
    return chunked_docs or DEFAULT_KNOWLEDGE_BASE
