import os
from dotenv import load_dotenv

# Ensure environment variables are loaded if .env exists
load_dotenv()

class ProviderManager:
    def __init__(self):
        # Default model routing based on task type, allowing environment variable overrides
        self.models = {
            "scan": os.getenv("MODEL_SCAN", "gpt-4o-mini"),
            "analyze": os.getenv("MODEL_ANALYZE", "gpt-4o")
        }

    def get_model(self, task_type):
        """
        Returns the model associated with a specific task type.
        Defaults to "gpt-4o-mini" for unknown task types.
        """
        return self.models.get(task_type, "gpt-4o-mini")
