# Design: One-Tool Web Search Chat Agent

## Requirements

1. Fast answers: minimize model/tool round trips, request concise responses, and cap search work.
2. Accurate answers: timely search for volatile questions, original URLs, uncertainty on missing evidence.
3. Memory: answer what was asked, in which conversation, and when (UTC); preserve across restarts.
4. Exactly one external tool: `web_search` exposed to the LLM. SQLite is deterministic application persistence.

## Architecture

```text
User -> CLI -> load recent + matching past questions (SQLite UTC)
                -> LLM (gpt-4.1-mini default)
                   | optionally call web_search (Brave API; max 2)
                   v
              source-aware answer -> save to SQLite
```

## Technical decisions

- **Latency:** no search for simple questions, two-search cap, 8-second search timeout, 8 results max, ~14K character memory context cap. Fast is a design objective, not a measured guarantee.
- **Grounding:** search output contains title, snippet, URL. Instructions explicitly require citing original URLs and treating result text as untrusted, not commands. Errors are structured, so the agent can express search failure without fabricating links.
- **Memory:** per-session SQLite rows with role, content, timezone-aware ISO 8601 UTC timestamp. Recent turns preserve context; lexical overlap retrieves old user questions, and `--history` provides a full inspectable timeline.
- **Security:** keys read from environment only; parameterized SQL; no execution or arbitrary URL fetch tool; search-result strings treated as untrusted evidence.

## Important limitations

- Snippets may be outdated, selective or incorrect. There is no full-article fetch or multi-source independent verification.
- The model can still hallucinate or mishandle citations; source checking is required for high-stakes answers.
- Lexical memory ranking can miss paraphrases. Recent conversation is truncated; long conversations require better retrieval.
- SQLite does not implement multi-user access controls or retention policies.
- No real API end-to-end benchmark or hosted deployment was performed.

## Validation / future benchmarks

- Unit tests: persistence/restart, session separation, timestamp format, retrieval, search shape, error path and one-tool schema.
- Evaluation dataset: 50 current events, 50 evergreen facts, 50 long-range recall questions, 20 adversarial snippets.
- Report answer accuracy, citation support, p50/p95 end-to-end latency, search success rate, and historical recall precision/recall.
- Before production: retries/backoff, rate limits, privacy deletion, structured citation validator, observability and concurrency tests.
