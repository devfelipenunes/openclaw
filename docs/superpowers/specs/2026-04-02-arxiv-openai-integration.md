# Design: Integração arXiv & Ativação de Inteligência (P&D Blockchain)

**Data:** 2026-04-02
**Contexto:** OpenClaw Multi-Agent Framework - Integração Real
**Foco:** Conectar o esquadrão à API do arXiv e ativar o consumo de tokens OpenAI.

## 1. Visão Geral
Este design visa substituir as simulações atuais por chamadas reais de API e processamento de modelos de linguagem (LLMs). O objetivo é que a agente **Nova** busque papers reais no arXiv, filtre-os usando inteligência artificial de baixo custo (GPT-4o-mini) e os agentes de elite (**Atlas** e **Aria**) processem o conhecimento técnico usando modelos de alta performance (GPT-4o).

## 2. Componentes de Integração

### 2.1. Motor de Busca Acadêmica (Nova Agent)
*   **Biblioteca:** `arxiv` (Python Wrapper).
*   **Parâmetros de Busca:**
    *   **Categorias:** `cs.CR` (Cryptography and Security), `cs.DC` (Distributed, Parallel, and Cluster Computing), `cs.NI` (Networking and Internet Architecture).
    *   **Ordenação:** `arxiv.SortCriterion.SubmittedDate` (Sempre os mais recentes).
*   **Triagem:** A `Nova` (GPT-4o-mini) analisará os resumos (*abstracts*) brutos e selecionará os 3 mais relevantes para o tema de P&D atual.

### 2.2. Camada de Inteligência (OpenAI API)
*   **BaseAgent:** Atualização da classe base para realizar chamadas reais via `openai.ChatCompletion`.
*   **Estratégia de Roteamento:**
    *   **GPT-4o-mini:** Triagem (Nova), Monitoramento (Rex).
    *   **GPT-4o:** Análise Técnica (Atlas), Redação de Especificações (Aria).
*   **Segurança:** Chave de API lida estritamente do arquivo `.env`.

### 2.3. Persistência de Conhecimento (ChromaDB)
*   **Ingestão:** Os resumos selecionados e as URLs dos PDFs serão salvos no `KnowledgeHub`.
*   **Metadados:** Data de publicação, autores e link original serão preservados para citações precisas pela `Aria`.

## 3. Fluxo de Dados Real
1.  **Requisição:** Usuário solicita pesquisa (ex: "Zk-Rollups").
2.  **Busca Bruta:** `Nova` chama a API do arXiv e obtém metadados de 10-20 papers recentes.
3.  **Filtragem:** `Nova` (GPT-4o-mini) seleciona os 3 melhores abstracts baseados na relevância técnica.
4.  **Análise:** `Atlas` (GPT-4o) processa os abstracts selecionados e gera insights de arquitetura.
5.  **Relatório:** `Aria` (GPT-4o) consulta o `ChromaDB` e redige a especificação técnica final.

## 4. Monitoramento de Custos
*   Implementação de um log de `Usage` que exibirá no terminal a quantidade de tokens consumidos por cada agente ao final de cada ciclo de pesquisa.

## 5. Próximos Passos (Plano de Implementação)
1.  Instalar a biblioteca `arxiv`.
2.  Atualizar o `BaseAgent` para chamadas reais da OpenAI.
3.  Implementar o método de busca real na `NovaAgent`.
4.  Atualizar os prompts de cada agente para lidar com dados reais.
5.  Configurar o sistema de logs de consumo de tokens.
