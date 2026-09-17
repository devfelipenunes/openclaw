"""
DebateOrchestrator — Análise multi-perspectiva com debate entre agentes.

Inspirado no PaperOrchestra (Google 2026) e Sibyl System:
- Múltiplas perspectivas analisam em paralelo (ThreadPoolExecutor)
- Moderador sintetiza consensos, divergências, questões em aberto
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from src.agents.base import BaseAgent


class DebateOrchestrator:
    """
    Orquestra debate entre múltiplas perspectivas de análise.

    Uso:
        debate = DebateOrchestrator()
        resultado = debate.analyze(papers_context, perspectives=["architecture", "security"])
    """

    PERSPECTIVES = {
        "architecture": {
            "label": "Architecture Analyst",
            "system_prompt": (
                "You are a senior systems architect specialized in blockchain and distributed systems. "
                "Analyze the technical architecture described in the papers. Focus on: "
                "system design, component interactions, data flow, consensus mechanisms, "
                "scalability approach, and layer structure. "
                "Identify architectural patterns, innovations, and potential design flaws."
            ),
        },
        "security": {
            "label": "Security Researcher",
            "system_prompt": (
                "You are a security researcher specializing in blockchain and cryptographic systems. "
                "Analyze the security aspects of the papers. Focus on: "
                "threat model, adversarial assumptions, cryptographic primitives used, "
                "attack vectors considered, formal verification, and security proofs. "
                "Highlight missing security considerations and potential vulnerabilities."
            ),
        },
        "adoption": {
            "label": "Adoption Analyst",
            "system_prompt": (
                "You are a technology adoption analyst focused on enterprise blockchain. "
                "Analyze the practical aspects. Focus on: "
                "implementation complexity, interoperability with existing systems, "
                "regulatory implications, maturity level, ecosystem support, "
                "performance trade-offs in production, and barriers to adoption."
            ),
        },
        "algorithms": {
            "label": "Algorithm Specialist",
            "system_prompt": (
                "You are an algorithms researcher. Analyze the core algorithms and protocols. "
                "Focus on: computational complexity, correctness proofs, "
                "optimization techniques, novel algorithmic contributions, "
                "asymptotic behavior, and comparison with existing approaches."
            ),
        },
        "economics": {
            "label": "Cryptoeconomics Analyst",
            "system_prompt": (
                "You are a cryptoeconomics researcher. Analyze the incentive structures. "
                "Focus on: tokenomics, incentive alignment, game-theoretic properties, "
                "mechanism design, fee models, staking/slashing conditions, "
                "and economic security guarantees."
            ),
        },
    }

    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers

    def analyze(
        self,
        papers_context: str,
        perspectives: list[str] | None = None,
    ) -> dict:
        """
        Executa análise multi-perspectiva em paralelo.

        Args:
            papers_context: Texto dos papers para analisar
            perspectives: Lista de perspectivas (default: architecture, security, adoption)

        Returns:
            dict com analyses (dict por perspectiva), synthesis (texto), consensus, divergences
        """
        if not perspectives:
            perspectives = ["architecture", "security", "adoption"]

        # Filtra apenas perspectivas válidas
        active = {k: v for k, v in self.PERSPECTIVES.items() if k in perspectives}
        if not active:
            return {"analyses": {}, "synthesis": "No valid perspectives selected."}

        # Executa análises em paralelo
        analyses = self._run_parallel(papers_context, active)

        # Moderador sintetiza
        synthesis = self._synthesize(analyses, papers_context)

        return {
            "analyses": analyses,
            "synthesis": synthesis,
            "perspectives_used": list(active.keys()),
        }

    def _run_parallel(self, context: str, perspectives: dict) -> dict:
        """Roda N análises em paralelo via ThreadPoolExecutor."""
        results = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_map = {}
            for key, config in perspectives.items():
                agent = BaseAgent(config["label"], "debate")
                prompt = f"Analyze the following research papers from a {config['label']} perspective:\n\n{context}"
                future = executor.submit(agent.run, prompt, config["system_prompt"])
                future_map[future] = key

            for future in as_completed(future_map):
                key = future_map[future]
                try:
                    results[key] = future.result()
                except Exception as e:
                    results[key] = f"[Analysis failed: {e}]"

        return results

    def _synthesize(self, analyses: dict, original_context: str) -> str:
        """Moderador sintetiza as análises em um texto coerente."""
        moderator = BaseAgent("Moderator", "analyze")

        analysis_text = "\n\n---\n\n".join(
            f"## {self.PERSPECTIVES.get(k, {}).get('label', k)}\n{v}"
            for k, v in analyses.items()
        )

        prompt = (
            "You are a research synthesis moderator. "
            "Given multiple analyses of the same papers from different perspectives:\n\n"
            f"{analysis_text}\n\n"
            "Produce a synthesis that:\n"
            "1. **Consensus**: What do all perspectives agree on?\n"
            "2. **Divergences**: Where do they disagree or focus on different aspects?\n"
            "3. **Open questions**: What remains unanswered?\n"
            "4. **Key insights**: The most important takeaways across all perspectives\n\n"
            "Be concise and structured."
        )

        return moderator.run(
            prompt,
            system_prompt="You are a research synthesis moderator. Synthesize diverse analyses into a coherent overview.",
        )
