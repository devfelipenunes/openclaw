import arxiv
from src.agents.base import BaseAgent

class NovaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Nova", "scan")
        self.client = arxiv.Client(
            num_retries=3,
            delay_seconds=3
        )
        
    def scan_arxiv(self, topic, max_results=10):
        # Busca híbrida recomendada: termo + categorias blockchain
        query = f'all:"{topic}" AND (cat:cs.CR OR cat:cs.DC OR cat:cs.NI)'
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        results = []
        for result in self.client.results(search):
            results.append({
                "title": result.title,
                "summary": result.summary,
                "url": result.pdf_url,
                "published": result.published.strftime("%Y-%m-%d")
            })
        return results
