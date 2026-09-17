"""
WriterAgent — Geração de relatórios técnicos e especificações.

Substitui o AriaAgent original. Foco em geração pura (sem auto-revisão).
A revisão fica a cargo do ReviewerAgent (separação judge/doer).
"""

from src.agents.base import BaseAgent


class WriterAgent(BaseAgent):
    """
    Gera relatórios técnicos, especificações e literature reviews.
    Sem auto-revisão — a qualidade é garantida pelo ReviewerAgent.
    """

    def __init__(self):
        super().__init__("Writer", "write")

    def write_spec(self, analysis: str, topic: str) -> str:
        """
        Gera uma especificação técnica detalhada.

        Args:
            analysis: Análise dos papers
            topic: Tópico da pesquisa

        Returns:
            Especificação técnica em markdown
        """
        prompt = (
            f"Create a detailed technical implementation specification for '{topic}' "
            f"based on this analysis:\n\n{analysis}"
        )
        return self.run(prompt, system_prompt="You are a Technical Writer specializing in Blockchain specs.")

    def write_report(self, analysis: str, topic: str, papers: list[dict] | None = None) -> str:
        """
        Gera um relatório de pesquisa completo.

        Args:
            analysis: Análise dos papers
            topic: Tópico da pesquisa
            papers: Lista de papers usados (opcional, para incluir referências)

        Returns:
            Relatório em markdown
        """
        papers_section = ""
        if papers:
            refs = "\n".join(
                f"- {p.get('title', 'Untitled')} — {p.get('url', '')}"
                for p in papers if p.get('title')
            )
            papers_section = f"\n\n## References\n{refs}\n"

        prompt = (
            f"Write a comprehensive research report on '{topic}'.\n\n"
            f"## Analysis\n{analysis}\n"
            f"{papers_section}\n"
            "Structure: Introduction, Key Findings, Technical Analysis, Conclusion."
        )
        return self.run(prompt, system_prompt="You are a Technical Researcher writing academic-quality reports.")

    def revise(self, draft: str, feedback: str) -> str:
        """
        Revisa um relatório baseado no feedback do Reviewer.

        Args:
            draft: Rascunho atual
            feedback: Críticas e sugestões do Reviewer

        Returns:
            Versão revisada
        """
        prompt = (
            "Revise the following report based on the reviewer's feedback.\n\n"
            f"## Draft\n{draft}\n\n"
            f"## Reviewer Feedback\n{feedback}\n\n"
            "Address all issues raised. Improve citations, clarity, and completeness."
        )
        return self.run(prompt, system_prompt="You are a Technical Writer revising a report based on peer review.")
