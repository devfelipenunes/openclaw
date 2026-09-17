# Academic Research Squad

Orquestrador multi-agente de pesquisa acadêmica com 7 fontes, debate multi-perspectiva, revisão por pares, e exportação para Obsidian.

## Instruções

1. Classifique a consulta: automático (Coordinator) ou manual (quick_scan, deep_analysis, citation_followup, survey).
2. Pipeline quick_scan: Searcher (1 fonte) → Librarian → Writer.
3. Pipeline deep_analysis: Searcher (7 fontes) → Reader → Analyst (debate) → Writer → Reviewer → Librarian.
4. Pipeline citation_followup: Searcher (grafo) → Reader → Writer → Librarian.
5. Pipeline survey: Searcher (multi-query) → Reader → Analyst (debate 5x) → Writer → Reviewer (loop) → Librarian.
6. Exporte para Obsidian automaticamente.

## Pipelines

| Pipeline          | Fontes | Tempo  | Saída                          |
| ----------------- | ------ | ------ | ------------------------------ |
| quick_scan        | 1      | ~30s   | Resumo LLM                     |
| deep_analysis     | 7      | ~5min  | Relatório completo com revisão |
| citation_followup | Grafo  | ~2min  | Análise de citações            |
| survey            | 7×N    | ~15min | Literature review exaustiva    |

## Configuração

Modelo: deepseek-chat
