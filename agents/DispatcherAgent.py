from transformers import pipeline
from util.gpu import get_device


class DispatcherAgent:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", device=get_device())
        self.labels = ["análisis de sentimiento", "generación de texto"]

    def route_request(self, text):
        result = self.classifier(text, candidate_labels=self.labels)
        task = result["labels"][0]

        return task
