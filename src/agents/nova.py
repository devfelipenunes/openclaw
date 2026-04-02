from src.agents.base import BaseAgent

class NovaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Nova", "scan")
        
    def scan_arxiv(self, topic):
        # Simulação de busca no arXiv
        return f"Encontrados 3 papers sobre {topic}"
