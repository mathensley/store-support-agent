# Empório da Música Support Agent

An agent prototype for answering customer messages about the "Empório da Música". It uses the supplied catalog, order records, and store policy manual to answer routine questions while keeping a friendly, professional Brazilian Portuguese voice.

## Setup

You need Python 3.12, [`uv`](https://docs.astral.sh/uv/), and an OpenAI API key with access to the configured model. From the repository root:

```sh
uv sync
cp .env.example .env
```

Replace `OPENAI_PROVIDER_KEY` in `.env` with your API key. The file also sets `MODEL="gpt-6-luna"`; change it to another compatible OpenAI model if needed. The CLI loads `.env` with `python-dotenv`.

## Run the agent

Send one message and exit:

```sh
uv run python -m src.main "Quais violões disponíveis custam até mil reais?"
```

Start an interactive conversation:

```sh
uv run python -m src.main
```

Type a message and press Enter. Enter `exit` to finish. The simple CLI streams the agent's text as it is generated. A single interactive run keeps one conversation history; a new process starts a new conversation. For an order query, provide the order number when the agent asks for it.

## Test the tools

Run the local CSV and PDF tool tests, without calling the OpenAI API:

```sh
uv run python -m unittest discover -s tests -p "test_*tool*.py" -v
```

These tests cover catalog filtering and promotions, order lookup, and retrieval of policy sections across PDF pages.

## Example conversations

The recorded conversations include the tool calls used by the agent, alongside the customer-facing replies:

- [Catalog search and recommendation](examples/01_catalog.md)
- [Store information and payment](examples/02_store_information.md)
- [Order status and return policy](examples/03_order_and_return.md)
- [Combined promotion, delivery, and installment rules](examples/04_combined_pricing_and_delivery.md)

## Architecture and technical choices

**Agent and model.** I chose LangChain because I have more experience with it and `create_agent` makes function calling straightforward for this small set of customer support tasks. If the scope grows, [middleware](https://docs.langchain.com/oss/python/langchain/middleware/overview) provides a clear way to add capabilities such as guardrails, retries, and observability without building a custom graph immediately. The model is supplied through `ChatOpenAI`. I chose `gpt-6-luna` as the default for its cost and quality balance: it is a lower-cost model suited to focused, frequent support requests. The `MODEL` environment variable keeps this choice configurable. See the [OpenAI model documentation](https://developers.openai.com/api/docs/models/gpt-6-luna).

**Interface and memory.** A CLI is quick to run and inspect during a demo. It accepts either a single question or a multi-turn conversation. LangGraph's `InMemorySaver` keeps short-term history under one `thread_id` for the duration of the process. A database/datastore is unnecessary for this initial local interaction pattern.

**Data access.** Tools are organized around customer tasks rather than one tool per CSV:

| Tool | Source | Responsibility |
| --- | --- | --- |
| `buscar_produtos` | `products.csv`, `categories.csv`, `promotions.csv` | Searches names, descriptions, and specifications; filters category, price, and availability; calculates active promotional prices with `Decimal`. |
| `consultar_pedidos` | `orders.csv` | Looks up one order by number and returns its recorded date, status, total, payment method, tracking code, estimated delivery, and notes. |
| `consultar_politicas` | `politicas_da_loja.pdf` | Extracts one of ten numbered policy sections and returns its text with source page numbers. |

The CSV tools read the files on each call, so a local file edit is visible to the next lookup. The files are still a supplied snapshot, not a live store database. `customers.csv` and `order_items.csv` are not needed for the current queries. Exposing raw tables or using Text-to-SQL would add complexity without improving these small, defined lookups.

**Policy retrieval.** The policy PDF has eight pages and a stable numbered structure. `pypdf` extracts sections, including those that cross page boundaries; the result is cached for the life of the process. A section lookup gives the agent relevant evidence and page provenance without placing the whole manual in every prompt. Embeddings and a vector database would add infrastructure before there is a larger document set to search.

**Prompt.** The system prompt lives in [`src/prompt/support_agent.md`](src/prompt/support_agent.md) and is loaded as text when the agent is created. It defines the store persona, directs price and order questions to CSV tools and policy questions to the PDF tool, asks for concise answers in pt-BR, and tells the agent to acknowledge missing evidence and redirect out-of-scope requests.

## Known limitations and next steps

- The CSVs contain historical sample records. Prices, stock, promotions, and order status do not reflect a live commerce system. A production version would query an authoritative service or database.
- An order number alone is **not authentication**. The supplied IDs are sequential, and the order tool exposes transactional fields. Production use would require customer authentication, authorization, rate limits, and guardrails around personal and order data.
- Conversation history disappears when the CLI exits. A multi-instance service would need a shared checkpointer, such as PostgreSQL, plus a defined retention policy.
- The PDF lookup depends on the current numbered headings and caches the manual until restart. The manual also contains conflicting contact details. I would validate policy content with the store, then add retrieval evaluation and a RAG pipeline if more documents or frequent revisions make section lookup insufficient.
- For deployment, I would add a container, an asynchronous service path for concurrent requests, and an API (either via Fast API or Flask) that a frontend or messaging channel can call. If product and order data grew into a frequently updated database, I would reassess structured queries and consider a constrained Text-to-SQL approach only with schema and access controls.
- Tool tests cover deterministic lookups, and the recorded conversations show four paths through the agent. With more time, I would build a golden set of representative questions with expected tool calls and grounded answers, then use it to evaluate tool choice, ambiguity, out-of-scope behavior, and regressions after changes.

## AI-assisted workflow

This README was drafted with Codex's assistance, following my guidance, and I reviewed and edited it afterward.