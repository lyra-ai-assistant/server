from transformers import pipeline

from util.gpu import get_device_config
from util.formatting import clean_response

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

SYSTEM_PROMPT = (
    "You are Lyra, a helpful GNU/Linux assistant. You provide accurate and relevant "
    "information, answer questions, and help with various Linux-related tasks. Keep "
    "responses concise for simple questions and detailed for complex ones. Use markdown "
    "for code blocks, JSON examples, and tables."
)


class GenerationAgent:
    def __init__(self):
        cfg = get_device_config()
        self.pipe = pipeline(
            "text-generation",
            model=MODEL_ID,
            torch_dtype=cfg["torch_dtype"],
            device_map=cfg["device_map"] if cfg["device_map"] else cfg["device"],
        )

    def handle_request(self, text: str, history: list | None = None) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": text})

        prompt = self.pipe.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        output = self.pipe(
            prompt,
            max_new_tokens=1024,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )
        raw: str = output[0]["generated_text"]

        # Extract only the new assistant turn from the full decoded output
        assistant_marker = "<|assistant|>"
        if assistant_marker in raw:
            raw = raw.split(assistant_marker)[-1]

        return clean_response(raw)
