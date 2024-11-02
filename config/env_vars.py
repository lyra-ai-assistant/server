from types import SimpleNamespace
from util.dirs import load_config

CONFIG_PATH = "~/.config/lyra/config.json"
config = load_config(CONFIG_PATH)

env_vars = SimpleNamespace(
    firebase=config["firebase"],
    host=config["host"],
    ngrok_port=config["ngrokPort"],
    api_port=config["apiPort"],
    mode=config["mode"],
    verbose=config["verbose"] == "1",
)
