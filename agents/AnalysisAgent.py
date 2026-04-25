from transformers import pipeline

from util.gpu import get_device


class AnalysisAgent:
    def __init__(self):
        self.model = pipeline("sentiment-analysis", device=get_device())

    def handle_request(self, text: str):
        return self.model(text)
