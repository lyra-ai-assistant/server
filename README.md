# Server

Lyra's backend server for local Small Language Models (SLMs). Built with FastAPI and HuggingFace Transformers. Runs entirely on-device — no internet connection or external services required.

## Architecture

The server uses a three-agent dispatch pipeline for general requests, plus a dedicated stateful chat endpoint with persistent memory:

```text
POST /              DispatcherAgent → AnalysisAgent (sentiment)
                                   → GenerationAgent (TinyLlama-1.1B)

POST /chat          SessionManager (SQLite) + SemanticMemory (ChromaDB)
                    → GenerationAgent with conversation history

POST /chat/stream   Same as /chat but streams tokens via SSE

GET  /health        Live system metrics (RAM, disk, CPU, active sessions)
```

**Persistent storage** lives at `~/.local/share/lyra/`:

| Path | Contents |
| --- | --- |
| `lyra.db` | SQLite — sessions and full message history |
| `chroma/` | ChromaDB — semantic embeddings (`all-MiniLM-L6-v2`) |

## Setup

Replace `[STAGE]` with `dev` or `build`.

### GNU/Linux

```bash
python -m venv env
source env/bin/activate
pip install -r [STAGE]-requirements.txt
```

### Windows

```bash
python -m venv env
.\env\Scripts\activate
pip install -r [STAGE]-requirements.txt
```

## Configuration

Before starting, make sure `~/.config/lyra/config.json` exists. If it doesn't, copy the template:

```bash
cp templates/config.json ~/.config/lyra/config.json
```

Edit it to match your setup:

```json
{
  "nodeEnv": "development",
  "host": "http://localhost",
  "apiPort": 4000,
  "mode": "dev",
  "verbose": "0"
}
```

Then start the server:

```bash
uvicorn main:app --reload
```

The first run will download two models:

- **TinyLlama/TinyLlama-1.1B-Chat-v1.0** (~2.2 GB) — text generation
- **all-MiniLM-L6-v2** (~80 MB) — semantic embeddings

## API

### `POST /`

Routes text through the dispatcher pipeline. Use for one-off requests.

```json
{ "text": "Analyze this: I love Linux", "context": null }
```

Response: `{ "response": "..." }`

### `POST /chat`

Stateful multi-turn conversation. Returns HTML-formatted text (markdown converted).

```json
{ "text": "How do I check disk usage?", "session_id": null }
```

Response:

```json
{ "response": "<p>Use <code>df -h</code>...</p>", "session_id": "uuid-here" }
```

Pass the returned `session_id` in every subsequent message to continue the conversation. Sessions expire after **30 minutes** of inactivity.

### `POST /chat/stream`

Same as `/chat` but streams tokens as Server-Sent Events. Ideal for the frontend to display responses token-by-token.

```text
data: {"session_id": "uuid-here"}
data: {"token": "Use"}
data: {"token": " df"}
data: {"token": " -h"}
...
data: [DONE]
```

### `DELETE /chat/{session_id}`

Clears a session and its history from the database.

### `GET /health`

Returns server status and live system metrics.

```json
{
  "status": "ok",
  "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  "active_sessions": 2,
  "memory": { "total_mb": 15987.3, "used_mb": 8241.1, "free_mb": 7746.2, "percent": 51.5 },
  "disk":   { "total_gb": 512.0,   "used_gb": 210.4,  "free_gb": 301.6,  "percent": 41.1 },
  "cpu":    { "cores": 8, "load_1m": 0.42, "load_5m": 0.38, "load_15m": 0.31 }
}
```
