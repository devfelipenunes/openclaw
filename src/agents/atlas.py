from src.agents.base import BaseAgent

class AtlasAgent(BaseAgent):
    def __init__(self):
        super().__init__("Atlas", "analyze")
        
    def analyze_paper(self, paper_content):
        return f"Análise técnica do paper: {paper_content[:50]}..."
