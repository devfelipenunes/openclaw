import arxiv
from src.agents.base import BaseAgent

class NovaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Nova", "scan")
        self.arxiv_client = arxiv.Client(
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
        for result in self.arxiv_client.results(search):
            results.append({
                "title": result.title,
                "summary": result.summary,
                "url": result.pdf_url,
                "published": result.published.strftime("%Y-%m-%d")
            })
        return results

    def filter_relevant_papers(self, papers, topic):
        if not papers: return []
        
        prompt = f"Based on the research topic '{topic}', analyze these paper summaries and return ONLY the titles of the 3 most technically relevant for Blockchain R&D. Format as a simple list.\n\n"
        for p in papers:
            prompt += f"Title: {p['title']}\nSummary: {p['summary']}\n---\n"
            
        selected_titles = self.run(prompt, system_prompt="You are a technical filter for Blockchain papers.")
        
        return [p for p in papers if p['title'] in selected_titles]
