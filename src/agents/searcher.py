"""
SearcherAgent — Motor de busca acadêmica com 7 fontes.

Substitui o NovaAgent original (arXiv-only) pelo Academic Hunter,
que busca em: arXiv, Crossref, OpenAlex, Semantic Scholar, CORE, DBLP, DOAJ
com NLP scoring, dedup, e grafo de citações.
"""

import os
import sys

# Garante que o Academic Hunter seja encontrável
_HUNTER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "pesquisa_academica", "src")
)
if os.path.isdir(_HUNTER_PATH) and _HUNTER_PATH not in sys.path:
    sys.path.insert(0, _HUNTER_PATH)

from academic_hunter import AcademicHunter
from academic_hunter.core.nlp.scorer import AcademicScorer
from src.agents.base import BaseAgent


class SearcherAgent(BaseAgent):
    """
    Busca acadêmica multi-fontes com NLP scoring.

    Modos:
      quick — apenas Semantic Scholar (~20s), ideal para scan rápido
      deep  — todas as 7 fontes com NLP scoring completo (~3min)
    """

    CONFIG_PATH = os.path.join(os.path.dirname(_HUNTER_PATH), "config.json")

    def __init__(self):
        super().__init__("Searcher", "scan")
        self.hunter = AcademicHunter(config_path=self.CONFIG_PATH)

    def search(self, topic: str, depth: str = "quick", max_results: int = 10) -> list[dict]:
        """
        Busca papers sobre o tópico.

        Args:
            topic: Tema da pesquisa (ex: "ZK-Rollups")
            depth: "quick" (1 fonte) | "deep" (7 fontes)
            max_results: Máximo de resultados

        Returns:
            Lista de papers com Relevance_Score, title, abstract, url, doi, etc.
        """
        self._configure_for_topic(topic)

        if depth == "quick":
            papers = self._search_quick(topic, max_results)
        else:
            papers = self._search_deep(topic, max_results)

        # Ordena por relevância (decrescente)
        papers.sort(key=lambda p: p.get("Relevance_Score", 0), reverse=True)
        return papers[:max_results]

    def search_citations(self, doi: str, direction: str = "citations", max_results: int = 10) -> list[dict]:
        """
        Explora o grafo de citações de um paper.

        Args:
            doi: DOI do paper
            direction: "citations" (quem cita) | "references" (referências)
            max_results: Máximo de resultados

        Returns:
            Lista de papers relacionados
        """
        try:
            from academic_hunter.plugins.connectors.semanticscholar import SemanticScholarConnector

            connector = SemanticScholarConnector(config={})
            results = connector.fetch_citation_graph(doi, direction=direction, limit=max_results)
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "doi": r.get("doi", ""),
                    "year": r.get("year", ""),
                    "citations": r.get("citationCount", 0),
                    "source": f"citation_graph/{direction}",
                }
                for r in results
            ]
        except Exception as e:
            print(f"[Searcher] Citation graph error: {e}")
            return []

    # ---- Internals ----

    def _configure_for_topic(self, topic: str):
        """Configura anchors e tech_strings dinamicamente para o tópico."""
        self.hunter.config.anchors = {
            "Primary": [topic],
            "Related": self._generate_related_terms(topic),
        }
        # Recria o scorer com as novas configs
        self.hunter.scorer = AcademicScorer(
            self.hunter.config.anchors,
            self.hunter.config.technical_strings,
            self.hunter.config.technical_weights,
            self.hunter.config.context_rules,
            self.hunter.config.settings,
        )

    def _search_quick(self, topic: str, max_results: int) -> list[dict]:
        """Busca rápida — apenas Semantic Scholar."""
        print(f"[Searcher] Quick scan: Semantic Scholar only")
        try:
            from academic_hunter.plugins.connectors.semanticscholar import SemanticScholarConnector

            connector = SemanticScholarConnector(config={})
            raw = connector.fetch(
                anchors=[topic],
                tech_strings=[],
                limit=max_results,
            )
            return self._normalize(raw, "semantic_scholar")
        except Exception as e:
            print(f"[Searcher] Quick scan failed: {e}")
            return []

    def _search_deep(self, topic: str, max_results: int) -> list[dict]:
        """Busca completa — todas as 7 fontes com NLP scoring."""
        print(f"[Searcher] Deep scan: all 7 sources with NLP scoring")
        try:
            self.hunter.run(limit_per_source=max_results * 3)
            return self._normalize(
                list(self.hunter.consolidated_results.values()), "academic_hunter"
            )
        except Exception as e:
            print(f"[Searcher] Deep scan failed: {e}")
            return []

    def _normalize(self, raw_papers: list[dict], source: str) -> list[dict]:
        """Normaliza papers de diferentes conectores para formato padrao."""
        normalized = []
        for p in raw_papers:
            normalized.append({
                "title": p.get("title", ""),
                "summary": p.get("summary", p.get("abstract", "")),
                "abstract": p.get("abstract", p.get("summary", "")),
                "url": p.get("url", p.get("pdf_url", "")),
                "doi": p.get("doi", ""),
                "year": p.get("year", p.get("published", ""))[:4] if p.get("year") or p.get("published") else "",
                "citations": p.get("citations", p.get("citationCount", 0)),
                "authors": p.get("authors", ""),
                "source": source,
                "Relevance_Score": p.get("Relevance_Score", p.get("score", 0)),
                "topic": p.get("topic", ""),
            })
        return normalized

    def _generate_related_terms(self, topic: str) -> list[str]:
        """Gera termos relacionados ao tópico (pode ser expandido com LLM no futuro)."""
        # Por enquanto, retorna o próprio tópico em variações
        return [topic, topic.lower(), topic.upper()]
