# Research Searcher (Scout)

Busca em 7 fontes acadêmicas (arXiv, Crossref, OpenAlex, Semantic Scholar, CORE, DBLP, DOAJ) com NLP scoring e grafo de citações.

## Instruções

1. Use `search` com o tópico e profundidade desejada.
2. Modo "quick" usa Semantic Scholar (~20s) para scans rápidos.
3. Modo "deep" usa todas as 7 fontes com NLP scoring completo (~3min).
4. Use `search_citations` para explorar grafo de citações por DOI.

## Configuração

Modelo: deepseek-chat
Fontes: ArXiv, Crossref, OpenAlex, Semantic Scholar, CORE, DBLP, DOAJ
