# Design: Esquadrão de P&D Blockchain (OpenClaw UI & Docker)

**Data:** 2026-04-02
**Contexto:** OpenClaw Multi-Agent Framework - Full Stack Integration
**Foco:** Dockerização, Interface de Controle (Dashboard) e Cadeia de Skills (Workflows).

## 1. Visão Geral
Este design migra o esquadrão de pesquisa de um script Python isolado para um ecossistema de microserviços dockerizados. A interação ocorrerá via **OpenClaw Control UI**, onde cada agente (Nova, Atlas, Aria, Rex) será representado por uma **Skill** dedicada, permitindo chamadas individuais ou a execução de um workflow completo de P&D (o "Botão Único").

## 2. Arquitetura de Containers (Docker Compose)
Utilizaremos 3 containers principais para garantir isolamento e escalabilidade:
1.  **`openclaw-gateway`**: O motor principal do OpenClaw (Node.js/TypeScript). Expõe a UI na porta **18789**.
2.  **`chromadb`**: Banco de vetores para a memória semântica (RAG) da equipe.
3.  **`blockchain-tools`**: Container Python contendo nossa lógica atual (arXiv API, Processamento de Texto) exposta como ferramentas (Tools) para o Gateway.

## 3. Estrutura de Skills (Multi-Agentes na UI)
Para que o usuário possa chamar cada agente ou o esquadrão completo, definiremos as seguintes Skills no diretório `skills/`:

### 3.1. Agentes Individuais (Modularidade)
*   **`blockchain_nova` (Scout)**: Skill focada em busca no arXiv e GitHub.
*   **`blockchain_atlas` (Analyst)**: Skill focada em extração de lógica técnica do ChromaDB.
*   **`blockchain_aria` (Writer)**: Skill focada em redação de especificações e relatórios.
*   **`blockchain_rex` (Watcher)**: Skill de monitoramento em background.

### 3.2. O Orquestrador (Workflow de Botão Único)
*   **`blockchain_research_squad`**: Uma Skill Mestre (Workflow) que encadeia as outras:
    1.  Chama a `Nova` para descobrir papers.
    2.  Aciona o `Atlas` para analisar o contexto salvo.
    3.  Finaliza com a `Aria` gerando o documento final no Canvas da UI.

## 4. Estratégia de Modelos & Custo (Token Optimization)
*   **Roteamento Padrão**: `gpt-4o-mini` para todas as skills (máxima economia).
*   **Override de Performance**: Opção de ativar o `gpt-4o` ou `claude-3-5-sonnet` via interface se o usuário solicitar "análise profunda".

## 5. Fluxo de Trabalho (Workflow)
1.  **Início:** Usuário acessa `http://localhost:18789` e digita: *"@squad Pesquise sobre Rollups de Soberania"*.
2.  **Processamento:** O Gateway orquestra as ferramentas do container Python.
3.  **Visualização:** O progresso de cada agente (Nova buscando, Atlas analisando) aparece em tempo real no Dashboard.
4.  **Entrega:** O relatório final é exibido em Markdown no chat e salvo na base de conhecimento.

## 6. Próximos Passos (Plano de Implementação)
1.  Criar o arquivo `docker-compose.yml` unificado.
2.  Definir os arquivos `SKILL.md` para cada agente (Nova, Atlas, Aria, Rex).
3.  Implementar o `tool-server` em Python para expor a lógica atual via HTTP/JSON.
4.  Configurar o roteamento de modelos `gpt-4o-mini` no arquivo `openclaw.json`.
