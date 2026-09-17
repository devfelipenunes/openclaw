"""
Pipeline — Definições dos pipelines de execução do Research Squad.

Cada pipeline é uma função que orquestra os agentes necessários.
"""

import os
from src.agents.searcher import SearcherAgent
from src.agents.reader import ReaderAgent
from src.agents.analyst import AnalystAgent
from src.agents.writer import WriterAgent
from src.agents.reviewer import ReviewerAgent
from src.core.librarian import Librarian


def _get_librarian():
    return Librarian(
        obsidian_path=os.getenv("OBSIDIAN_PATH", "/l/disk0/fnunes/obsidian")
    )


def run_quick_scan(topic: str, max_papers: int = 5) -> dict:
    """
    Pipeline rápido: busca 1 fonte + resumo LLM.
    ~30 segundos.
    """
    lib = _get_librarian()
    searcher = SearcherAgent()

    papers = searcher.search(topic, depth="quick", max_results=max_papers)
    lib.add_papers(papers)

    # Resumo via LLM
    analyst = AnalystAgent()
    context = lib.search(topic, top_k=min(3, len(papers)))
    summary = analyst.analyze(
        "\n\n".join(c["text"] for c in context),
        mode="single"
    )

    return {
        "topic": topic,
        "pipeline": "quick_scan",
        "papers": papers,
        "total_papers": len(papers),
        "analysis": summary,
        "librarian": lib,
    }


def run_deep_analysis(topic: str, max_papers: int = 10) -> dict:
    """
    Pipeline completo: 7 fontes → PDFs → debate → escrita → revisão.
    ~5-10 minutos.
    """
    lib = _get_librarian()
    searcher = SearcherAgent()
    reader = ReaderAgent()
    analyst = AnalystAgent()
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    # 1. Busca em 7 fontes
    papers = searcher.search(topic, depth="deep", max_results=max_papers)
    lib.add_papers(papers)
    print(f"[Pipeline] {len(papers)} papers encontrados")

    # 2. Lê PDFs dos top papers
    for p in papers[:3]:
        result = reader.read_paper(p)
        if result["success"]:
            lib.add_paper(
                text=result["text"][:5000],
                metadata={"title": result["title"], "source": "pdf", "topic": topic}
            )
            print(f"[Pipeline] PDF lido: {result['title'][:60]}...")

    # 3. Debate multi-perspectiva
    context = lib.search(topic, top_k=5)
    context_text = "\n\n".join(c["text"] for c in context)
    analysis = analyst.analyze(context_text, mode="debate")
    print(f"[Pipeline] Debate concluído")

    # 4. Escrita
    draft = writer.write_report(analysis, topic, papers)

    # 5. Revisão
    review_result = reviewer.review_and_iterate(writer, draft, context_text)
    print(f"[Pipeline] Revisão: {review_result['iterations']} iterações, passed={review_result['passed']}")

    return {
        "topic": topic,
        "pipeline": "deep_analysis",
        "papers": papers,
        "total_papers": len(papers),
        "analysis": analysis,
        "report": review_result["final_report"],
        "review": review_result,
        "librarian": lib,
    }


def run_citation_followup(doi: str, max_papers: int = 10) -> dict:
    """
    Pipeline de citações: explora grafo de citações de um paper.
    ~2-3 minutos.
    """
    lib = _get_librarian()
    searcher = SearcherAgent()
    writer = WriterAgent()

    papers = searcher.search_citations(doi, max_results=max_papers)
    lib.add_papers(papers)

    context = lib.search(doi, top_k=3)
    context_text = "\n\n".join(c["text"] for c in context)
    report = writer.write_report(context_text, f"Citation Analysis: {doi}")

    return {
        "topic": doi,
        "pipeline": "citation_followup",
        "papers": papers,
        "total_papers": len(papers),
        "report": report,
        "librarian": lib,
    }


def run_survey(topic: str, max_papers: int = 20) -> dict:
    """
    Pipeline survey: múltiplas queries, análise exaustiva.
    ~15-30 minutos.
    """
    lib = _get_librarian()
    searcher = SearcherAgent()
    reader = ReaderAgent()
    analyst = AnalystAgent()
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    # Múltiplas queries para cobrir diferentes ângulos
    subtopics = [topic, f"{topic} architecture", f"{topic} security", f"{topic} challenges"]
    all_papers = []

    for sub in subtopics:
        papers = searcher.search(sub, depth="deep", max_results=max_papers // len(subtopics))
        all_papers.extend(papers)

    # Dedup por título
    seen = set()
    unique_papers = []
    for p in all_papers:
        t = p.get("title", "").lower().strip()
        if t and t not in seen:
            seen.add(t)
            unique_papers.append(p)

    lib.add_papers(unique_papers)
    print(f"[Pipeline] Survey: {len(unique_papers)} papers únicos")

    # Lê PDFs dos top 5
    for p in unique_papers[:5]:
        result = reader.read_paper(p)
        if result["success"]:
            lib.add_paper(
                text=result["text"][:5000],
                metadata={"title": result["title"], "source": "pdf", "topic": topic}
            )

    # Debate completo (5 perspectivas)
    context = lib.search(topic, top_k=8)
    context_text = "\n\n".join(c["text"] for c in context)
    analysis = analyst.analyze(
        context_text,
        mode="debate",
        perspectives=["architecture", "security", "adoption", "algorithms", "economics"]
    )

    # Escrita + revisão em loop
    draft = writer.write_report(analysis, topic, unique_papers)
    review_result = reviewer.review_and_iterate(writer, draft, context_text, max_iterations=3)

    return {
        "topic": topic,
        "pipeline": "survey",
        "papers": unique_papers,
        "total_papers": len(unique_papers),
        "analysis": analysis,
        "report": review_result["final_report"],
        "review": review_result,
        "librarian": lib,
    }
