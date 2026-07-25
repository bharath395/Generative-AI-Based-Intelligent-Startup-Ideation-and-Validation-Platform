class MemoryManager:
    """
    Manages user session context and persistent chat memory for AI Startup Mentor.
    """
    def __init__(self):
        self._conversations = {}

    def add_message(self, user_id, role, content):
        if user_id not in self._conversations:
            self._conversations[user_id] = []
        self._conversations[user_id].append({"role": role, "content": content})
        # Keep last 15 messages
        if len(self._conversations[user_id]) > 15:
            self._conversations[user_id] = self._conversations[user_id][-15:]

    def get_history(self, user_id):
        return self._conversations.get(user_id, [])

    def clear(self, user_id):
        if user_id in self._conversations:
            del self._conversations[user_id]

memory_manager = MemoryManager()
