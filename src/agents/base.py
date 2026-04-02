from src.core.provider import ProviderManager

class BaseAgent:
    def __init__(self, name, task_type):
        self.name = name
        self.model = ProviderManager().get_model(task_type)
        
    def run(self, prompt):
        # Placeholder para chamada da OpenAI
        return f"[{self.name}] Response from {self.model}"
