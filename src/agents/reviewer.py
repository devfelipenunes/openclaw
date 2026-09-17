"""
ReviewerAgent — Revisão independente de relatórios técnicos.

Separação judge/doer (Anthropic best practice):
O Writer gera, o Reviewer critica.
"""

from src.agents.base import BaseAgent


class ReviewerAgent(BaseAgent):
    """
    Revisor independente que avalia qualidade de relatórios técnicos.

    Critérios:
      - Acurácia das citações (papers suportam as afirmações?)
      - Cobertura (trabalhos relacionados mencionados?)
      - Consistência lógica (contradições internas?)
      - Clareza técnica (conceitos explicados adequadamente?)
    """

    def __init__(self):
        super().__init__("Reviewer", "review")

    def review(self, report: str, papers_context: str = "") -> dict:
        """
        Avalia um relatório e retorna críticas estruturadas.

        Args:
            report: Relatório a ser revisado
            papers_context: Contexto dos papers originais (opcional)

        Returns:
            dict com: issues (lista), score (0.0-1.0), passed (bool), feedback (texto)
        """
        prompt = (
            "Review the following research report critically.\n\n"
            f"## Report\n{report}\n"
        )
        if papers_context:
            prompt += f"\n## Original Papers Context\n{papers_context}\n"

        prompt += (
            "\nEvaluate on these criteria:\n"
            "1. **Citation accuracy**: Do the cited papers actually support the claims?\n"
            "2. **Coverage**: Are important related works mentioned?\n"
            "3. **Logical consistency**: Any internal contradictions?\n"
            "4. **Technical clarity**: Are concepts explained adequately?\n"
            "5. **Completeness**: Are there obvious gaps?\n\n"
            "Respond in this exact format:\n"
            "SCORE: X.XX (0.0-1.0)\n"
            "PASSED: YES/NO\n"
            "ISSUES:\n"
            "- Issue 1 description\n"
            "- Issue 2 description\n"
            "FEEDBACK:\n"
            "Detailed feedback text here..."
        )

        result = self.run(prompt, system_prompt="You are a strict peer reviewer for academic research. Be critical and specific.")

        # Parse resultado estruturado
        return self._parse_review(result)

    def review_and_iterate(self, writer, report: str, papers_context: str = "", max_iterations: int = 3) -> dict:
        """
        Loop de revisão: critica → writer.revise → critica → ... até passar.

        Args:
            writer: Instância de WriterAgent
            report: Rascunho inicial
            papers_context: Contexto dos papers
            max_iterations: Máximo de iterações

        Returns:
            dict com final_report, iterations, passed
        """
        current = report
        history = []

        for i in range(max_iterations):
            review_result = self.review(current, papers_context)
            history.append({"iteration": i + 1, "review": review_result})

            if review_result.get("passed", False):
                return {
                    "final_report": current,
                    "iterations": i + 1,
                    "passed": True,
                    "history": history,
                }

            # Revisa baseado no feedback
            current = writer.revise(current, review_result.get("feedback", ""))
            print(f"[Reviewer] Iteration {i + 1}: score={review_result.get('score', 0):.2f}, revising...")

        # Última verificação
        final_review = self.review(current, papers_context)
        return {
            "final_report": current,
            "iterations": max_iterations,
            "passed": final_review.get("passed", False),
            "final_score": final_review.get("score", 0),
            "history": history,
        }

    def _parse_review(self, text: str) -> dict:
        """Parseia a resposta do revisor para formato estruturado."""
        score = 0.5
        passed = False
        issues = []
        feedback = text

        for line in text.split("\n"):
            if line.startswith("SCORE:"):
                try:
                    score = float(line.split(":")[1].strip())
                except ValueError:
                    score = 0.5
            elif line.startswith("PASSED:"):
                passed = "YES" in line.upper()
            elif line.startswith("- "):
                issues.append(line[2:].strip())

        # Extrai feedback após "FEEDBACK:"
        if "FEEDBACK:" in text:
            feedback = text.split("FEEDBACK:", 1)[1].strip()

        return {
            "score": score,
            "passed": passed,
            "issues": issues,
            "feedback": feedback,
        }
