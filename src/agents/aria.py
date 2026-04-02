from src.agents.base import BaseAgent

class AriaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Aria", "analyze")
        
    def write_spec(self, analysis, topic):
        prompt = f"Create a detailed technical implementation specification for '{topic}' based on this analysis:\n\n{analysis}"
        return self.run(prompt, system_prompt="You are a Technical Writer specializing in Blockchain specs.")
