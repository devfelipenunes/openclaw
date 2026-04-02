from src.agents.base import BaseAgent

class AriaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Aria", "analyze")
        
    def write_spec(self, analysis):
        return f"# Technical Specification\n\n{analysis}"
