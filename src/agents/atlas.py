from src.agents.base import BaseAgent

class AtlasAgent(BaseAgent):
    def __init__(self):
        super().__init__("Atlas", "analyze")
        
    def analyze_papers(self, papers_context):
        prompt = f"Analyze the following technical papers context and extract architectural insights, trade-offs, and algorithms:\n\n{papers_context}"
        return self.run(prompt, system_prompt="You are a Senior Blockchain Architect.")
