"""
AnalystAgent — Análise técnica de papers com suporte a debate multi-perspectiva.

Substitui o AtlasAgent original com modo single (comportamento legado)
e modo debate (multi-perspectiva paralela).
"""

from src.agents.base import BaseAgent
from src.core.debate import DebateOrchestrator


class AnalystAgent(BaseAgent):
    """
    Analisa papers com suporte a dois modos:
      single — comportamento original do Atlas (análise única)
      debate — múltiplas perspectivas em paralelo com síntese
    """

    def __init__(self):
        super().__init__("Analyst", "analyze")
        self.debate = DebateOrchestrator(max_workers=3)

    def analyze(self, papers_context: str, mode: str = "single", perspectives: list[str] | None = None) -> str:
        """
        Analisa papers técnicos.

        Args:
            papers_context: Texto dos papers
            mode: "single" (legado) ou "debate" (multi-perspectiva)
            perspectives: Lista de perspectivas (apenas modo debate)

        Returns:
            Análise em texto
        """
        if mode == "debate":
            result = self.debate.analyze(papers_context, perspectives)
            return self._format_debate_result(result)

        # Modo single — comportamento original do Atlas
        prompt = (
            "Analyze the following technical papers context and extract "
            "architectural insights, trade-offs, and algorithms:\n\n"
            f"{papers_context}"
        )
        return self.run(prompt, system_prompt="You are a Senior Blockchain Architect.")

    def _format_debate_result(self, result: dict) -> str:
        """Formata o resultado do debate em texto legível."""
        lines = ["## Multi-Perspective Analysis\n"]

        for key, analysis in result.get("analyses", {}).items():
            label = DebateOrchestrator.PERSPECTIVES.get(key, {}).get("label", key)
            lines.append(f"### {label}")
            lines.append(analysis)
            lines.append("")

        lines.append("## Synthesis\n")
        lines.append(result.get("synthesis", ""))

        return "\n".join(lines)
