import os
import json
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key=None):
        if os.getenv('DISABLE_LIVE_AI', '0') == '1':
            self.api_key = ''
            self.client = None
            self.model = ''
            return

        self.api_key = api_key or os.getenv('GEMINI_API_KEY', '')
        self.model = os.getenv('GEMINI_MODEL', 'gemini-3.6-flash')
        self.client = None
        
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Google Gemini Client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize google-genai client: {e}. Falling back to AI heuristics mode.")

    def generate_content(self, prompt, system_instruction=None, response_schema_json=True):
        """
        Calls Gemini API if available, otherwise delegates to heuristic fallback.
        """
        if self.client:
            try:
                config = {}
                if response_schema_json:
                    config["response_mime_type"] = "application/json"
                if system_instruction:
                    config["system_instruction"] = system_instruction

                response = self._call_model(prompt, config)
                
                if response_schema_json:
                    return json.loads(self._extract_text(response))
                return self._extract_text(response)
            except Exception as e:
                logger.error(f"Gemini API invocation error: {e}. Utilizing fallback engine.")
        
        return None # Signal to calling agent to use heuristic fallback

    def _call_model(self, prompt, config):
        if hasattr(self.client, 'models'):
            return self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config if config else None
            )

        if hasattr(self.client, 'interactions'):
            return self.client.interactions.create(
                model=self.model,
                input=prompt
            )

        raise RuntimeError("Installed google-genai client does not expose a supported generation API.")

    @staticmethod
    def _extract_text(response):
        return getattr(response, 'text', None) or getattr(response, 'output_text', '')

gemini_service = GeminiService()
