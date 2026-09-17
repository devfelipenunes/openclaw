from openai import OpenAI
from src.core.provider import ProviderManager


class BaseAgent:
    """
    Agente base com suporte a múltiplos provedores LLM
    (DeepSeek, OpenAI, Ollama — qualquer API OpenAI-compatible).
    """

    def __init__(self, name: str, task_type: str):
        self.name = name
        self.provider = ProviderManager()
        self.model = self.provider.get_model(task_type)
        self.client = OpenAI(
            api_key=self.provider.get_api_key(),
            base_url=self.provider.get_base_url(),
        )

    def run(self, prompt: str, system_prompt: str = "You are a specialized Blockchain R&D assistant.") -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        content = response.choices[0].message.content
        usage = response.usage

        print(
            f"[{self.name}] Model: {self.model} "
            f"| Tokens: {usage.total_tokens} "
            f"(Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens})"
        )

        return content
