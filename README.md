# Knowledge Graph with Personality

## Overview

Turn raw text or a document into a rich knowledge graph augmented with inferred “personality/traits” for entities, and visualize it interactively in the browser.

This project uses:
- LangChain’s LLMGraphTransformer to extract entities and relationships
- An Ollama local LLM (default: `llama3.2:latest`) for both graph extraction and trait inference
- A small async enrichment pass to attach concise traits to each node
- PyVis to render the interactive graph to `knowledge_graph_with_personality.html`
- A Flask web app to accept text or file uploads and serve the result

## Features

- Input via web UI (text box or .txt/.pdf upload)
- Async pipeline for extraction and enrichment
- Traits added to node tooltips for quick inspection
- One-click HTML graph output you can open and share

## Detailed Report
Detailed Report can be found [here](https://docs.google.com/document/d/1xkIOr3CDakKEGTqouVpoL3e_e873aIolpy-TLIxBcLA/edit?usp=sharing)


## Project structure

```
knowledge_graph/
├─ app.py                          # Flask web server (text/file input → pipeline → serve HTML)
├─ knowledge_graph_with_personality.html   # Generated visualization
├─ requirements.txt                      # Sample text
└─ modules/
	 ├─ pipeline.py                  # async generate_knowledge_graph(...) end-to-end pipeline
	 ├─ graph_extraction.py          # LLMGraphTransformer setup and async extraction
	 ├─ personality_enrichment.py    # async trait inference per node
	 ├─ visualization.py             # PyVis rendering
	 └─ file_utils.py                # PDF/txt readers and input resolution
```

## Prerequisites

- Python 3.10+ (tested with 3.12 on Windows)
- [Ollama](https://ollama.ai) installed and running locally
	- Pull the model used in this project:
		- `ollama pull llama3.2:latest` (or your preferred compatible model)
	- If you use a different model tag, update it in `modules/pipeline.py`.

## How to run the project

```powershell
# From the project root
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
python app.py
```


## Usage:
1. Open the printed URL (default: http://127.0.0.1:5000)
2. Enter text or choose a `.txt`/`.pdf`
3. Click Submit
4. The app will generate and immediately serve `knowledge_graph_with_personality.html`

The output file is also saved to the project root for later viewing.

