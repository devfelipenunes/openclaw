"""
Coordinator — Classificador de consulta e roteador de pipeline.

Determina qual pipeline executar baseado no tipo de consulta:
  quick_scan      → busca rápida + resumo LLM
  deep_analysis   → 7 fontes + PDFs + debate + revisão
  citation_followup → grafo de citações
  survey          → multi-query exaustiva
"""

from src.agents.base import BaseAgent


class Coordinator:
    """
    Orquestrador principal do Research Squad.
    Classifica a consulta e delega ao pipeline adequado.
    """

    PIPELINES = ["quick_scan", "deep_analysis", "citation_followup", "survey"]

    def __init__(self):
        self.classifier = BaseAgent("Coordinator", "scan")

    def classify(self, query: str) -> str:
        """
        Classifica a consulta em um tipo de pipeline.

        Returns:
            "quick_scan" | "deep_analysis" | "citation_followup" | "survey"
        """
        prompt = (
            f"Classify this research query into exactly one category:\n\n"
            f"Query: \"{query}\"\n\n"
            "Categories:\n"
            "- quick_scan: Fast overview, general question, 'what is', 'explain', 'summarize'\n"
            "- deep_analysis: Technical deep dive, 'analyze', 'compare', 'how does X work', architecture\n"
            "- citation_followup: References, citations, 'who cited', 'related work'\n"
            "- survey: Comprehensive, 'state of the art', 'literature review', 'survey', comprehensive\n\n"
            "Respond with ONLY the category name, nothing else."
        )
        result = self.classifier.run(prompt, "You classify research queries into pipeline types.")
        result = result.strip().lower()

        # Valida e fallback
        for p in self.PIPELINES:
            if p in result:
                return p
        return "quick_scan"  # fallback seguro

    def plan(self, query: str) -> dict:
        """
        Gera um plano de execução para a consulta.

        Returns:
            dict com pipeline, depth, max_papers, usar_reader, usar_debate, usar_reviewer
        """
        pipeline = self.classify(query)

        plans = {
            "quick_scan": {
                "pipeline": "quick_scan",
                "depth": "quick",
                "max_papers": 5,
                "use_reader": False,
                "use_debate": False,
                "use_reviewer": False,
                "description": "Quick scan: 1 source, LLM summary, no review",
            },
            "deep_analysis": {
                "pipeline": "deep_analysis",
                "depth": "deep",
                "max_papers": 10,
                "use_reader": True,
                "use_debate": True,
                "use_reviewer": True,
                "description": "Deep analysis: 7 sources, PDFs, debate, review",
            },
            "citation_followup": {
                "pipeline": "citation_followup",
                "depth": "quick",
                "max_papers": 10,
                "use_reader": True,
                "use_debate": False,
                "use_reviewer": True,
                "description": "Citation followup: citation graph, related papers",
            },
            "survey": {
                "pipeline": "survey",
                "depth": "deep",
                "max_papers": 20,
                "use_reader": True,
                "use_debate": True,
                "use_reviewer": True,
                "description": "Survey: multi-query, comprehensive literature review",
            },
        }

        return plans.get(pipeline, plans["quick_scan"])
