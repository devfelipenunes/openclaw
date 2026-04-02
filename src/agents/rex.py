from src.agents.base import BaseAgent

class RexAgent(BaseAgent):
    def __init__(self):
        super().__init__("Rex", "scan")
        
    def watch_github(self, repo):
        return f"Monitorando {repo} para novos commits."
