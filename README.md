# Agentic RAG Workspace

This repository implements an Adaptive Retrieval-Augmented Generation (RAG) pipeline using Azure OpenAI, LangChain, CartesiaAI, and AssemblyAI. It includes model configuration, ingestion, and graph-based orchestration.

## Directory Structure

```
.env                      # Environment variables for API keys and config
main.py                   # Entry point for running the pipeline
model.py                  # LLM and embedding model configuration
ingestion.py              # Data ingestion utilities
assembly.py               # AssemblyAI integration
cartesiaai.py             # CartesiaAI integration
graph/
  ├── graph.py            # Graph orchestration logic
  ├── state.py            # State management
  ├── consts.py           # Graph constants
  ├── chains/             # Chain definitions
  └── nodes/              # Node definitions
FAISS_index/              # FAISS vector index files
static/                   # Static assets (images, HTML)
requirements.txt          # Python dependencies
```

## Setup

1. **Clone the repository**

   ```sh
   git clone <repo-url>
   cd agentic-rag
   ```
2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```
3. **Configure environment variables**
   Edit `.env` with your API keys and endpoints. Example:

   ```
   AZURE_OPENAI_API_KEY=...
   AZURE_OPENAI_DEPLOYMENT_NAME=...
   AZURE_OPENAI_API_VERSION=...
   AZURE_OPENAI_ENDPOINT=...
   AZURE_EMBEDDING_DEPLOYMENT_NAME=...
   CARTESIA_API_KEY=...
   CARTESIA_API_URL=...
   ASSEMBLYAI_API_KEY=...
   LANGSMITH_API_KEY=...
   ```

## Usage

Run the main pipeline:

```sh
python main.py
```

## Components

- **Model Configuration:** [`model.py`](model.py)
- **Data Ingestion:** [`ingestion.py`](ingestion.py)
- **Graph Orchestration:** [`graph/graph.py`](graph/graph.py)
- **CartesiaAI Integration:** [`cartesiaai.py`](cartesiaai.py)
- **AssemblyAI Integration:** [`assembly.py`](assembly.py)

## Notes

- Ensure all API keys in `.env` are valid.
- FAISS index files are stored in [`FAISS_index/`](FAISS_index/).
- Static assets (images, HTML) are in [`static/`](static/).
