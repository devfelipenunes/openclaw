# Blockchain R&D Multi-Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar um esquadrão autônomo de 4 agentes (Nova, Atlas, Aria, Rex) para pesquisa técnica e monitoramento de Blockchain usando OpenClaw, otimizando custos com GPT-4o-mini e GPT-4o.

**Architecture:** O sistema utiliza um `ProviderManager` modular para roteamento de modelos, um `KnowledgeHub` baseado em ChromaDB para memória semântica (RAG) e uma estrutura de agentes especialistas que colaboram em um pipeline de Descoberta -> Análise -> Escrita -> Vigilância.

**Tech Stack:** Python 3.10+, OpenClaw, OpenAI API (GPT-4o/mini), ChromaDB, python-dotenv.

---

### Task 1: Ambiente e Configuração Inicial

**Files:**
- Create: `requirements.txt`
- Create: `.env`
- Create: `.gitignore`

- [x] **Step 1: Criar arquivo de dependências**

```text
openai
chromadb
python-dotenv
requests
pytest
```

- [x] **Step 2: Configurar variáveis de ambiente**

```bash
# .env
OPENAI_API_KEY=sk-proj-SUA_CHAVE_AQUI
MODEL_SCAN=gpt-4o-mini
MODEL_ANALYZE=gpt-4o
DB_PATH=./data/chroma
```

- [x] **Step 3: Configurar .gitignore**

```text
.env
__pycache__/
data/
venv/
.pytest_cache/
```

- [x] **Step 4: Commit inicial**

```bash
git add requirements.txt .gitignore
git commit -m "chore: setup project environment"
```

---

### Task 2: Provider Manager (Roteamento de Modelos)

**Files:**
- Create: `src/core/provider.py`
- Test: `tests/test_provider.py`

- [x] **Step 1: Escrever teste para o ProviderManager**

```python
import os
from src.core.provider import ProviderManager

def test_provider_routing():
    pm = ProviderManager()
    assert pm.get_model("scan") == "gpt-4o-mini"
    assert pm.get_model("analyze") == "gpt-4o"
```

- [x] **Step 2: Implementar ProviderManager**

```python
import os
from dotenv import load_dotenv

load_dotenv()

class ProviderManager:
    def __init__(self):
        self.models = {
            "scan": os.getenv("MODEL_SCAN", "gpt-4o-mini"),
            "analyze": os.getenv("MODEL_ANALYZE", "gpt-4o")
        }

    def get_model(self, task_type):
        return self.models.get(task_type, "gpt-4o-mini")
```

- [x] **Step 3: Validar testes e Commit**

```bash
pytest tests/test_provider.py
git add src/core/provider.py tests/test_provider.py
git commit -m "feat: add modular provider manager for model routing"
```

---

### Task 3: Knowledge Hub (Memória Semântica com ChromaDB)

**Files:**
- Create: `src/core/memory.py`
- Test: `tests/test_memory.py`

- [x] **Step 1: Escrever teste de RAG básico**

```python
from src.core.memory import KnowledgeHub

def test_knowledge_persistence():
    hub = KnowledgeHub(collection_name="test_rd")
    hub.add_document("Ethereum EIP-1559 introduces a base fee.", {"source": "eip-1559"})
    results = hub.search("base fee")
    assert len(results) > 0
    assert "EIP-1559" in results[0]
```

- [x] **Step 2: Implementar KnowledgeHub**

```python
import chromadb
import os

class KnowledgeHub:
    def __init__(self, collection_name="blockchain_rd"):
        self.client = chromadb.PersistentClient(path=os.getenv("DB_PATH", "./data/chroma"))
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_document(self, text, metadata):
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[str(hash(text))]
        )

    def search(self, query, n_results=3):
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results['documents'][0]
```

- [x] **Step 3: Validar e Commit**

```bash
pytest tests/test_memory.py
git add src/core/memory.py tests/test_memory.py
git commit -m "feat: implement semantic memory hub with ChromaDB"
```

---

### Task 4: Agentes Base e Nova (The Scout)

**Files:**
- Create: `src/agents/base.py`
- Create: `src/agents/nova.py`

- [x] **Step 1: Criar Classe Base de Agente**

```python
from src.core.provider import ProviderManager

class BaseAgent:
    def __init__(self, name, task_type):
        self.name = name
        self.model = ProviderManager().get_model(task_type)
        
    def run(self, prompt):
        # Placeholder para chamada da OpenAI
        return f"[{self.name}] Response from {self.model}"
```

- [x] **Step 2: Implementar Agente Nova (GPT-4o-mini)**

```python
from src.agents.base import BaseAgent

class NovaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Nova", "scan")
        
    def scan_arxiv(self, topic):
        # Simulação de busca no arXiv
        return f"Encontrados 3 papers sobre {topic}"
```

- [x] **Step 3: Commit**

```bash
git add src/agents/base.py src/agents/nova.py
git commit -m "feat: add BaseAgent and Nova (Scout) agent"
```

---

### Task 5: Agentes de Raciocínio (Atlas e Aria)

**Files:**
- Create: `src/agents/atlas.py`
- Create: `src/agents/aria.py`

- [x] **Step 1: Implementar Atlas (Analista - GPT-4o)**

```python
from src.agents.base import BaseAgent

class AtlasAgent(BaseAgent):
    def __init__(self):
        super().__init__("Atlas", "analyze")
        
    def analyze_paper(self, paper_content):
        return f"Análise técnica do paper: {paper_content[:50]}..."
```

- [x] **Step 2: Implementar Aria (Escritora - GPT-4o)**

```python
from src.agents.base import BaseAgent

class AriaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Aria", "analyze")
        
    def write_spec(self, analysis):
        return f"# Technical Specification\n\n{analysis}"
```

- [x] **Step 3: Commit**

```bash
git add src/agents/atlas.py src/agents/aria.py
git commit -m "feat: add Atlas (Analyst) and Aria (Writer) agents"
```

---

### Task 6: Agente Rex (Watcher) e Orquestrador Final

**Files:**
- Create: `src/agents/rex.py`
- Create: `src/main.py`

- [ ] **Step 1: Implementar Rex (Monitor - GPT-4o-mini)**

```python
from src.agents.base import BaseAgent

class RexAgent(BaseAgent):
    def __init__(self):
        super().__init__("Rex", "scan")
        
    def watch_github(self, repo):
        return f"Monitorando {repo} para novos commits."
```

- [ ] **Step 2: Criar Orquestrador Principal**

```python
from src.agents.nova import NovaAgent
from src.agents.atlas import AtlasAgent
from src.agents.aria import AriaAgent
from src.agents.rex import RexAgent

def main():
    print("Iniciando Esquadrão OpenClaw P&D Blockchain...")
    nova = NovaAgent()
    atlas = AtlasAgent()
    aria = AriaAgent()
    rex = RexAgent()
    
    # Exemplo de fluxo
    discovery = nova.scan_arxiv("Zk-Rollups")
    analysis = atlas.analyze_paper(discovery)
    spec = aria.write_spec(analysis)
    
    print(spec)
    print(rex.watch_github("ethereum/EIPs"))

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Validar Fluxo Completo e Commit**

```bash
python3 src/main.py
git add src/agents/rex.py src/main.py
git commit -m "feat: complete multi-agent squad and orchestrator"
```
