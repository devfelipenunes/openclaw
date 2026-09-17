# arXiv & OpenAI Real Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Conectar o esquadrão à API do arXiv e ativar o processamento real via OpenAI (GPT-4o/mini) com rastreamento de consumo de tokens.

**Architecture:** Atualizaremos a `BaseAgent` para realizar chamadas reais à API da OpenAI e a `NovaAgent` para consumir o wrapper `arxiv`. Introduziremos um sistema de logs para monitorar o uso de tokens por agente.

**Tech Stack:** Python, OpenAI SDK, `arxiv` library, ChromaDB, python-dotenv.

---

### Task 1: Instalação de Dependências e Setup do arXiv

**Files:**
- Modify: `requirements.txt`
- Modify: `src/agents/nova.py`

- [x] **Step 1: Adicionar biblioteca arxiv às dependências**

```text
openai
chromadb
python-dotenv
requests
pytest
arxiv
```

- [x] **Step 2: Instalar novas dependências**

Run: `pip install -r requirements.txt`

- [x] **Step 3: Implementar busca real na NovaAgent**

```python
import arxiv
from src.agents.base import BaseAgent

class NovaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Nova", "scan")
        self.client = arxiv.Client()
        
    def scan_arxiv(self, topic, max_results=10):
        # Busca híbrida recomendada: termo + categorias blockchain
        query = f'all:"{topic}" AND (cat:cs.CR OR cat:cs.DC OR cat:cs.NI)'
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        results = []
        for result in self.client.results(search):
            results.append({
                "title": result.title,
                "summary": result.summary,
                "url": result.pdf_url,
                "published": result.published.strftime("%Y-%m-%d")
            })
        return results
```

- [ ] **Step 4: Commit**

```bash
git add requirements.txt src/agents/nova.py
git commit -m "feat: integrate real arXiv API search in NovaAgent"
```

---

### Task 2: Ativação das Chamadas OpenAI (BaseAgent)

**Files:**
- Modify: `src/agents/base.py`

- [x] **Step 1: Implementar chamadas reais na BaseAgent**

```python
import os
from openai import OpenAI
from src.core.provider import ProviderManager

class BaseAgent:
    def __init__(self, name, task_type):
        self.name = name
        self.model = ProviderManager().get_model(task_type)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def run(self, prompt, system_prompt="You are a specialized Blockchain R&D assistant."):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        usage = response.usage
        
        # Log de consumo de tokens
        print(f"[{self.name}] Model: {self.model} | Tokens: {usage.total_tokens} (Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens})")
        
        return content
```

- [x] **Step 2: Commit**

```bash
git add src/agents/base.py
git commit -m "feat: enable real OpenAI API calls in BaseAgent with token logging"
```

---

### Task 3: Triagem Inteligente e Persistência (Nova -> Memory)

**Files:**
- Modify: `src/agents/nova.py`
- Modify: `src/main.py`

- [ ] **Step 1: Adicionar lógica de filtragem na NovaAgent**

```python
# No src/agents/nova.py
    def filter_relevant_papers(self, papers, topic):
        if not papers: return []
        
        prompt = f"Based on the research topic '{topic}', analyze these paper summaries and return ONLY the titles of the 3 most technically relevant for Blockchain R&D. Format as a simple list.\n\n"
        for p in papers:
            prompt += f"Title: {p['title']}\nSummary: {p['summary']}\n---\n"
            
        selected_titles = self.run(prompt, system_prompt="You are a technical filter for Blockchain papers.")
        
        return [p for p in papers if p['title'] in selected_titles]
```

- [ ] **Step 2: Atualizar fluxo no main.py para usar dados reais**

```python
from src.agents.nova import NovaAgent
from src.core.memory import KnowledgeHub
# ... outros imports

def main():
    hub = KnowledgeHub()
    nova = NovaAgent()
    # ... outros agentes
    
    topic = "Zk-Rollups"
    raw_papers = nova.scan_arxiv(topic)
    filtered_papers = nova.filter_relevant_papers(raw_papers, topic)
    
    for paper in filtered_papers:
        hub.add_document(
            text=f"Title: {paper['title']}\nSummary: {paper['summary']}",
            metadata={"url": paper['url'], "source": "arxiv", "topic": topic}
        )
```

- [ ] **Step 3: Commit**

```bash
git add src/agents/nova.py src/main.py
git commit -m "feat: implement smart paper filtering and RAG ingestion"
```

---

### Task 4: Análise e Redação Real (Atlas & Aria)

**Files:**
- Modify: `src/agents/atlas.py`
- Modify: `src/agents/aria.py`

- [ ] **Step 1: Atualizar Atlas para usar run() real**

```python
from src.agents.base import BaseAgent

class AtlasAgent(BaseAgent):
    def __init__(self):
        super().__init__("Atlas", "analyze")
        
    def analyze_papers(self, papers_context):
        prompt = f"Analyze the following technical papers context and extract architectural insights, trade-offs, and algorithms:\n\n{papers_context}"
        return self.run(prompt, system_prompt="You are a Senior Blockchain Architect.")
```

- [ ] **Step 2: Atualizar Aria para usar run() real**

```python
from src.agents.base import BaseAgent

class AriaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Aria", "analyze")
        
    def write_spec(self, analysis, topic):
        prompt = f"Create a detailed technical implementation specification for '{topic}' based on this analysis:\n\n{analysis}"
        return self.run(prompt, system_prompt="You are a Technical Writer specializing in Blockchain specs.")
```

- [ ] **Step 3: Commit**

```bash
git add src/agents/atlas.py src/agents/aria.py
git commit -m "feat: enable real technical analysis and spec writing"
```

---

### Task 5: Validação Final do Fluxo Real

- [x] **Step 1: Rodar o orquestrador com um tema real**

Run: `PYTHONPATH=. python3 src/main.py`
Expected: Ver logs de consumo de tokens reais e saída de especificação baseada em papers reais do arXiv.

- [x] **Step 2: Commit final de conclusão de integração**

```bash
git commit -m "feat: complete end-to-end integration with arXiv and OpenAI"
```
