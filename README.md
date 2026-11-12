# One-Tool Web Search Chat Agent

Fast, grounded conversational assistant using **exactly one model-callable tool**, `web_search` (Brave Search API). A SQLite database persists user and assistant turns, session IDs, and UTC timestamps across restarts.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-openai-key"
export BRAVE_SEARCH_API_KEY="your-brave-search-key"
python agent.py --session demo
```

Single shot: `python agent.py --session demo --ask "What is the latest Mars mission update?"`

Display dated previous questions: `python agent.py --session demo --history`

Tests: `python -m unittest discover -s tests -v`

## Key behaviors

- Model decides whether searching is needed. Stable knowledge and conversation recall avoid search when possible.
- Search capped at 2 invocations per user turn and 8 results per query, with an 8-second request timeout.
- Source URLs accompany search-derived claims; failed retrieval is explicitly surfaced.
- Local memory includes UTC timestamps and isolates sessions.
- One model-callable tool only: database is application-owned persistence, not a second tool.

## Caveats

Search returns snippets, not full pages. Factual accuracy and latency are **not yet benchmarked**. The app needs active OpenAI and Brave API credentials and does not provide a hosted service. See [design.md](design.md).
