import os
from dotenv import load_dotenv

load_dotenv()

class ProviderManager:
    """
    Gerencia roteamento de modelos LLM com suporte a
    provedores OpenAI-compatible (DeepSeek, Ollama, etc.).

    Configurável via .env:
      LLM_BASE_URL     — base_url do provider (default: https://api.deepseek.com)
      LLM_API_KEY      — chave da API
      MODEL_SCAN       — modelo para varredura rápida
      MODEL_ANALYZE    — modelo para análise técnica
      MODEL_DEBATE     — modelo para debate multi-perspectiva
      MODEL_REVIEW     — modelo para revisão
      MODEL_WRITE      — modelo para escrita de relatórios
    """

    DEFAULTS = {
        "base_url": "https://api.deepseek.com",
        "scan": "deepseek-chat",
        "analyze": "deepseek-chat",
        "debate": "deepseek-chat",
        "review": "deepseek-chat",
        "write": "deepseek-chat",
    }

    def __init__(self):
        self.base_url = os.getenv("LLM_BASE_URL", self.DEFAULTS["base_url"])
        self.api_key = os.getenv("LLM_API_KEY", "")

        self.models = {
            "scan": os.getenv("MODEL_SCAN", self.DEFAULTS["scan"]),
            "analyze": os.getenv("MODEL_ANALYZE", self.DEFAULTS["analyze"]),
            "debate": os.getenv("MODEL_DEBATE", self.DEFAULTS["debate"]),
            "review": os.getenv("MODEL_REVIEW", self.DEFAULTS["review"]),
            "write": os.getenv("MODEL_WRITE", self.DEFAULTS["write"]),
        }

    def get_base_url(self) -> str:
        return self.base_url

    def get_api_key(self) -> str:
        return self.api_key

    def get_model(self, task_type: str) -> str:
        """Retorna o modelo configurado para o tipo de tarefa."""
        return self.models.get(task_type, "deepseek-chat")
