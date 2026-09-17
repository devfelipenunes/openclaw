"""
OpenClaw Research Squad — Esquadrão multi-agente de pesquisa acadêmica.

Uso:
    python -m src.main --topic "ZK-Rollups"
    python -m src.main --topic "CBDC" --pipeline deep_analysis
    python -m src.main --topic "Bridges" --pipeline survey --export-obsidian
    python -m src.main --doi "10.1234/example" --pipeline citation_followup
"""

import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Garante que o Academic Hunter seja encontrável
_HUNTER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "pesquisa_academica", "src")
)
if os.path.isdir(_HUNTER_PATH) and _HUNTER_PATH not in sys.path:
    sys.path.insert(0, _HUNTER_PATH)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Research Squad")
    parser.add_argument("--topic", type=str, default=None, help="Tópico de pesquisa")
    parser.add_argument("--doi", type=str, default=None, help="DOI para follow-up de citações")
    parser.add_argument(
        "--pipeline", type=str,
        choices=["auto", "quick_scan", "deep_analysis", "citation_followup", "survey"],
        default="auto",
        help="Pipeline a executar (auto = classifica automaticamente)"
    )
    parser.add_argument("--max-papers", type=int, default=10, help="Máximo de papers")
    parser.add_argument("--export-obsidian", action="store_true", help="Exportar para Obsidian")
    args = parser.parse_args()

    # --- Determina pipeline ---
    if args.doi:
        args.pipeline = "citation_followup"
        args.topic = args.doi

    if args.pipeline == "auto" and args.topic:
        from src.coordinator import Coordinator
        coord = Coordinator()
        args.pipeline = coord.classify(args.topic)
        plan = coord.plan(args.topic)
        print(f"[Coordinator] Classified as: {args.pipeline}")
        print(f"[Coordinator] Plan: {plan['description']}")

    # --- Executa pipeline ---
    from src.core.pipeline import (
        run_quick_scan,
        run_deep_analysis,
        run_citation_followup,
        run_survey,
    )

    PIPELINES = {
        "quick_scan": run_quick_scan,
        "deep_analysis": run_deep_analysis,
        "citation_followup": run_citation_followup,
        "survey": run_survey,
    }

    runner = PIPELINES.get(args.pipeline, run_quick_scan)

    print("=" * 60)
    print(f"  OpenClaw — Research Squad")
    print(f"  Pipeline: {args.pipeline}")
    print(f"  Tópico:   {args.topic}")
    print("=" * 60)

    if args.pipeline == "citation_followup":
        result = runner(args.topic, args.max_papers)
    else:
        result = runner(args.topic, args.max_papers)

    # --- Saída ---
    print("\n" + "=" * 60)
    print(f"RESULTADO: {result.get('topic', '')}")
    print(f"Pipeline: {result.get('pipeline', '')}  |  Papers: {result.get('total_papers', 0)}")
    print("=" * 60)

    if "report" in result:
        print(result["report"])
    elif "analysis" in result:
        print(result["analysis"])

    print("=" * 60)

    # --- Exporta para Obsidian ---
    if args.export_obsidian and "librarian" in result:
        content = result.get("report") or result.get("analysis") or ""
        path = result["librarian"].export_to_obsidian(
            args.topic or "research",
            content,
            tags=["research-squad", args.pipeline],
        )
        if path:
            print(f"\n[✓] Exportado para Obsidian: {path}")

    # --- Estatísticas ---
    if "librarian" in result:
        stats = result["librarian"].stats()
        print(f"\n📚 Librarian: {stats['total_docs']} documentos no ChromaDB")
        print(f"   Obsidian: {stats['obsidian_path']}")

    print("\n[✓] Processo completo.")


if __name__ == "__main__":
    main()
