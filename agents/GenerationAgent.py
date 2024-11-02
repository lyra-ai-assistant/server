from transformers import pipeline
from autogen import Agent

from util.gpu import get_device


class GenerationAgent(Agent):
    def __init__(self):
        super().__init__()
        self.model = pipeline("text-generation", model="gpt2", device=get_device())

    def handle_request(self, prompt, context=None):
        if context:
            prompt = f"{context}\n\n{prompt}"
        response = self.model(prompt, max_length=150, do_sample=True, temperature=0.7)
        return response[0]["generated_text"]
