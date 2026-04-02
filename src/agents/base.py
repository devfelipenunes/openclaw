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
