# Spec: Integração Híbrida OpenClaw + Ollama

## 1. Objetivo
Evoluir o sistema de provedores do OpenClaw para suportar múltiplos backends de LLM (OpenAI e Ollama local) de forma híbrida e explícita, permitindo que cada agente utilize o modelo e provedor mais adequados para sua tarefa.

## 2. Arquitetura Proposta

### 2.1. ProviderManager (`src/core/provider.py`)
O `ProviderManager` será o ponto central de decisão. Ele lerá as variáveis de ambiente para determinar:
- **Provider**: `openai` ou `ollama`.
- **Model**: Nome do modelo (ex: `gpt-4o-mini`, `llama3.2:3b`).
- **Base URL**: URL para o provedor (padrão `http://localhost:11434/v1` para Ollama).

### 2.2. BaseAgent (`src/agents/base.py`)
O `BaseAgent` será modificado para instanciar o cliente `OpenAI` dinamicamente com base nas configurações retornadas pelo `ProviderManager`.
- Se `provider == "ollama"`, o `api_key` será "ollama" (fictício) e o `base_url` será a URL do Ollama.
- Se `provider == "openai"`, usará a `OPENAI_API_KEY` e a URL padrão da OpenAI.

## 3. Configuração (.env)
O sistema utilizará prefixos para cada tipo de tarefa (SCAN, ANALYZE, WRITE):
```bash
# Configurações Globais
OLLAMA_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=sk-...

# Configuração por Agente (Exemplo Híbrido)
SCAN_PROVIDER=ollama
SCAN_MODEL=llama3.2:3b

ANALYZE_PROVIDER=ollama
ANALYZE_MODEL=deepseek-coder-v2:16b

WRITE_PROVIDER=openai
WRITE_MODEL=gpt-4o-mini
```

## 4. Estratégia de Teste de Modelos
Antes da implementação final, realizaremos um teste de "smoke test" com os modelos locais disponíveis:
1. **Llama3.2:3b**: Avaliar para extração e filtragem rápida (Nova).
2. **Deepseek-coder-v2:16b**: Avaliar para análise técnica profunda (Atlas).
3. **Qwen2.5-coder:7b**: Avaliar para geração de especificações (Aria).

## 5. Critérios de Sucesso
- O sistema deve ser capaz de alternar entre OpenAI e Ollama apenas alterando o `.env`.
- O `BaseAgent` deve logar corretamente qual modelo e provedor está sendo usado em cada chamada.
- O fluxo completo de R&D (Nova -> Atlas -> Aria) deve funcionar usando 100% Ollama se configurado.
