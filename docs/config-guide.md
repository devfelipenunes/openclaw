# Configuração do OpenClaw (DeepSeek)

Configure as variáveis no `.env` (crie a partir deste guia):

```env
# --- Provedor LLM (DeepSeek) ---
LLM_API_KEY=sk-your-deepseek-key
LLM_BASE_URL=https://api.deepseek.com

# --- Modelos por tipo de tarefa ---
MODEL_SCAN=deepseek-chat
MODEL_ANALYZE=deepseek-chat
MODEL_DEBATE=deepseek-chat
MODEL_REVIEW=deepseek-chat
MODEL_WRITE=deepseek-chat

# --- Caminhos ---
DB_PATH=./data/chroma
```
