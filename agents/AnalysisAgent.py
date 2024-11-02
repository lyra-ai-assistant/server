from transformers import pipeline
from autogen import Agent

from util.gpu import get_device


class AnalysisAgent(Agent):
    def __init__(self):
        self.model = pipeline("sentiment-analysis", device=get_device())

    def handle_request(self, text):
        return self.model(text)
