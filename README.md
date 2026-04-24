# Server

Lyra's default server for SLMs (Small Language Models). Built with FastAPI and HuggingFace Transformers, it exposes a single `POST /` endpoint that routes requests through a three-agent pipeline: dispatcher → analysis or generation.

## Setup

Replace `[STAGE]` with `dev` or `build`.

### GNU/Linux

```bash
python -m venv env
source env/bin/activate
pip install -r ./[STAGE]-requirements.txt
```

### Windows

```bash
python -m venv env
.\env\Scripts\activate
pip install -r ./[STAGE]-requirements.txt
```

## Running

Before starting, make sure `~/.config/lyra/config.json` exists. If it doesn't, copy the template:

```bash
cp templates/config.json ~/.config/lyra/config.json
```

Then start the server:

```bash
uvicorn main:app --reload
```

## API

`POST /` — accepts `{ "text": "...", "context": "..." }` and returns `{ "response": "..." }`.
