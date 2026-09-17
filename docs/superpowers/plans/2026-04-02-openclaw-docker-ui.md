# OpenClaw Docker & UI Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dockerizar o esquadrão de P&D Blockchain e integrá-lo como Skills oficiais na Control UI do OpenClaw (porta 18789), otimizando custos com GPT-4o-mini.

**Architecture:** O sistema utilizará `docker-compose` para subir o Gateway do OpenClaw e o ChromaDB. A lógica Python será exposta como ferramentas para o Gateway, e cada agente será uma Skill (`SKILL.md`) que o Dashboard visualiza e orquestra.

**Tech Stack:** Docker, Docker Compose, OpenClaw Framework, Python, ChromaDB.

---

### Task 1: Estrutura de Diretórios e Docker Compose

**Files:**
- Create: `docker-compose.yml`
- Create: `Dockerfile.tools`

- [ ] **Step 1: Criar o docker-compose.yml unificado**

```yaml
version: '3.8'
services:
  openclaw-gateway:
    image: openclaw/openclaw:latest
    ports:
      - "18789:18789"
    volumes:
      - ./skills:/app/skills
      - ./.env:/app/.env
    environment:
      - OPENCLAW_PORT=18789
    depends_on:
      - chromadb
      - blockchain-tools

  chromadb:
    image: chromadb/chroma:latest
    volumes:
      - ./data/chroma:/chroma/chroma
    ports:
      - "8000:8000"

  blockchain-tools:
    build:
      context: .
      dockerfile: Dockerfile.tools
    volumes:
      - .:/app
    env_file:
      - .env
```

- [ ] **Step 2: Criar Dockerfile para as ferramentas Python**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
CMD ["python", "src/main.py"] 
```

- [ ] **Step 3: Commit**

```bash
git add docker-compose.yml Dockerfile.tools
git commit -m "chore: add docker-compose and tools dockerfile"
```

---

### Task 2: Definindo as Skills (Persona Agents)

**Files:**
- Create: `skills/blockchain_nova/SKILL.md`
- Create: `skills/blockchain_atlas/SKILL.md`
- Create: `skills/blockchain_aria/SKILL.md`

- [ ] **Step 1: Criar Skill da Nova (Scout)**

```markdown
# Blockchain Scout (Nova)
Encontre papers acadêmicos e técnicos sobre Blockchain no arXiv.

## Instruções
Sempre use a ferramenta `search_arxiv` para buscar temas.
Filtre por relevância técnica em criptografia e sistemas distribuídos.

## Configuração
Modelo: gpt-4o-mini
```

- [ ] **Step 2: Criar Skill do Atlas (Analyst)**

```markdown
# Blockchain Analyst (Atlas)
Analise insights técnicos de papers e extraia arquitetura.

## Instruções
Use a ferramenta `rag_search` para consultar a base de conhecimento no ChromaDB.
Foque em trade-offs de segurança e escalabilidade.

## Configuração
Modelo: gpt-4o-mini
```

- [ ] **Step 3: Criar Skill da Aria (Writer)**

```markdown
# Blockchain Writer (Aria)
Escreva especificações técnicas e relatórios profissionais.

## Instruções
Redija documentos Markdown baseados nas análises do Atlas.
Mantenha um tom profissional e densidade técnica.

## Configuração
Modelo: gpt-4o-mini
```

- [ ] **Step 4: Commit**

```bash
git add skills/
git commit -m "feat: define modular OpenClaw skills for each agent"
```

---

### Task 3: O Orquestrador (Botão Único)

**Files:**
- Create: `skills/research_squad/SKILL.md`

- [ ] **Step 1: Criar a Skill Mestre de Workflow**

```markdown
# Blockchain Research Squad
Executa o fluxo completo de P&D (Nova -> Atlas -> Aria).

## Instruções
Ao receber um tema:
1. Chame a Skill `blockchain_nova` para buscar dados.
2. Chame a Skill `blockchain_atlas` para analisar os dados.
3. Chame a Skill `blockchain_aria` para gerar o relatório final.

## Configuração
Modelo: gpt-4o-mini
```

- [ ] **Step 2: Commit**

```bash
git add skills/research_squad/SKILL.md
git commit -m "feat: add master research squad skill for single-button workflow"
```

---

### Task 4: Configuração do Gateway e Modelos

**Files:**
- Create: `openclaw.json`

- [ ] **Step 1: Configurar roteamento de modelos global**

```json
{
  "gateway": {
    "port": 18789
  },
  "models": {
    "default": "gpt-4o-mini",
    "mappings": {
      "analyze": "gpt-4o-mini",
      "scan": "gpt-4o-mini"
    }
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add openclaw.json
git commit -m "config: setup model routing for cost optimization"
```

---

### Task 5: Lançamento e Validação na UI

- [ ] **Step 1: Subir os containers**

Run: `docker-compose up -d --build`

- [ ] **Step 2: Validar acesso à UI**

Acesse: `http://localhost:18789`
Verifique se as skills `blockchain_nova`, `blockchain_atlas`, `blockchain_aria` e `research_squad` aparecem no menu lateral.

- [ ] **Step 3: Executar o "Botão Único"**

No chat da UI, digite: `@squad Inicie pesquisa sobre Optimistic Rollups`.
Observe no Canvas visual os agentes trabalhando em sequência.
