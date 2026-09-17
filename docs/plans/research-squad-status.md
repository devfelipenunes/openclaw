# Research Squad — Status

> Última atualização: 08/07/2026

## ✅ Concluído

### Código (100% implementado)

- [x] ProviderManager com DeepSeek (`src/core/provider.py`)
- [x] BaseAgent genérico multi-provider (`src/agents/base.py`)
- [x] Librarian — ChromaDB + Obsidian export (`src/core/librarian.py`)
- [x] SearcherAgent — 7 fontes via Academic Hunter (`src/agents/searcher.py`)
- [x] ReaderAgent — PDF download + extração (`src/agents/reader.py`)
- [x] AnalystAgent — análise single + debate (`src/agents/analyst.py`)
- [x] DebateOrchestrator — 5 perspectivas paralelas (`src/core/debate.py`)
- [x] WriterAgent — geração de relatórios (`src/agents/writer.py`)
- [x] ReviewerAgent — revisão + loop de iteração (`src/agents/reviewer.py`)
- [x] Coordinator — classificação + roteamento (`src/coordinator.py`)
- [x] 4 pipelines (quick_scan, deep_analysis, citation_followup, survey) (`src/core/pipeline.py`)
- [x] CLI completa com argparse (`src/main.py`)

### Infraestrutura

- [x] Dockerfile.squad (container unificado)
- [x] Dockerfile.mcp (Academic Hunter MCP sidecar)
- [x] docker-compose.yml (5 serviços)
- [x] 7 Skills do Gateway OpenClaw
- [x] `docs/config-guide.md`
- [x] 5/5 testes passando

## ⏳ Pendente

- [ ] **Task 1:** Configurar `.env` com DeepSeek
  ```
  LLM_API_KEY=sk-...
  LLM_BASE_URL=https://api.deepseek.com
  MODEL_SCAN=deepseek-chat
  MODEL_ANALYZE=deepseek-chat
  MODEL_DEBATE=deepseek-chat
  MODEL_REVIEW=deepseek-chat
  MODEL_WRITE=deepseek-chat
  OBSIDIAN_PATH=/l/disk0/fnunes/obsidian
  DB_PATH=./data/chroma
  ```
- [ ] **Task 2:** Testar Quick Scan
  ```bash
  python -m src.main --topic "ZK-Rollups"
  ```
- [ ] **Task 3:** Testar Deep Analysis
  ```bash
  python -m src.main --topic "CBDC" --pipeline deep_analysis
  ```
- [ ] **Task 4:** Testar Citation Followup
  ```bash
  python -m src.main --doi "10.1234/example" --pipeline citation_followup
  ```
- [ ] **Task 5:** Testar Survey + Obsidian
  ```bash
  python -m src.main --topic "Layer 2 scalability" --pipeline survey --export-obsidian
  ```
- [ ] **Task 6:** Testar Docker Compose
  ```bash
  docker-compose up
  ```
- [ ] **Task 7:** Ajustes finos

## Como retomar

1. Atualize o `.env` com as vars acima (a chave é a mesma do DeepSeek)
2. Rode `python -m src.main --topic "ZK-Rollups"` pra validar
3. Depois teste os pipelines mais complexos

## Arquivos principais

| Arquivo                  | Descrição                       |
| ------------------------ | ------------------------------- |
| `src/main.py`            | Entry point CLI                 |
| `src/coordinator.py`     | Classificador de consulta       |
| `src/agents/searcher.py` | Busca 7 fontes acadêmicas       |
| `src/agents/reader.py`   | Download + extração de PDFs     |
| `src/agents/analyst.py`  | Análise com debate              |
| `src/core/debate.py`     | Orquestrador de debate paralelo |
| `src/agents/writer.py`   | Geração de relatórios           |
| `src/agents/reviewer.py` | Revisão + iteração              |
| `src/core/librarian.py`  | ChromaDB + Obsidian             |
| `src/core/pipeline.py`   | 4 pipelines de execução         |
| `docker-compose.yml`     | 5 serviços Docker               |
