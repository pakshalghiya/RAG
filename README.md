# RAG → Agent

Session code for building a job-matching AI agent, from a PDF to a working web app.

```
Day 1   resume.pdf ──► chunks ──► embeddings ──► vector store ──► RAG answers
Day 2   tools ──► an LLM that decides which to call ──► MCP ──► Gradio UI
```

## Files

| File | Day | What it is |
|---|---|---|
| `llm.py` | 1 | Wraps the local Ollama model (`qwen3:0.6b`) |
| `rag.py` | 1 | PDF → chunks → embeddings → Chroma, plus a retrieval chain |
| `resume.pdf` | 1 | The sample resume that gets indexed |
| `shared_tools.py` | 2 | The three tools: web search, job search, resume lookup |
| `system_prompts.py` | 2 | The agent's standing instructions |
| `mcp_server.py` | 2 | The same tools, served over HTTP as an MCP server |
| `agent.py` | 2 | Model + tools + prompt, wrapped in a Gradio UI |
| `day2_walkthrough.ipynb` | 2 | **Start here** — every piece above, run one cell at a time |

## Setup

```bash
# 1. environment (Python 3.10+; 3.12 recommended)
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. the local model
#    install Ollama from https://ollama.com first
ollama pull qwen3:0.6b
ollama serve                       # leave this running

# 3. API keys (Day 2 only)
cp .env.example .env               # then paste your free Adzuna keys in
```

## Running it

**The notebook — recommended.** It explains each piece and shows the output of every
step.

```bash
jupyter notebook day2_walkthrough.ipynb
```

Every cell is written to fail politely: if Ollama is not running, or the MCP server is
down, or your Adzuna keys are missing, the cell tells you what to start instead of
throwing a traceback. Read it straight through, then go back and re-run the parts you
have set up.

**The scripts.** Each file runs on its own, and prints something useful:

```bash
python llm.py            # ask the model a question
python rag.py            # ask a question about the resume
python shared_tools.py   # call a tool directly
python agent.py          # launch the Gradio app at http://127.0.0.1:7860
```

`agent.py` expects the MCP server to be up. In a second terminal:

```bash
source .venv/bin/activate
python mcp_server.py     # serves the tools on http://localhost:8001/mcp
```

To skip MCP entirely, edit `agent.py` and use the commented-out line that imports the
tools directly instead:

```python
tools = [web_search_tool, get_job_recommendation, get_resume_data]
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Connection refused` on port 11434 | `ollama serve` is not running |
| `{"exception": "AUTH_FAIL"}` | Adzuna keys missing from `.env` |
| `Connection refused` on port 8001 | Start `python mcp_server.py` in another terminal |
| `Could not import sentence_transformers` | `pip install sentence-transformers` |
| DuckDuckGo search errors intermittently | Rate limiting — wait and re-run |
| `vector_db/` missing after ingestion | The run failed; it should contain a sqlite file and a collection folder |
