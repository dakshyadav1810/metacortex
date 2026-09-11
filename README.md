# MetaCortex

A Graph-of-Thought (GoT) based reasoning system for MetaKGP wiki using LLaMA 3.3 70B for claim extraction, verification, and answer synthesis.

## Features

- **Vector Search**: FAISS-based semantic search over wiki content
- **Graph-of-Thought Reasoning**: Constructs knowledge graphs from claims
- **Multi-Expert Verification (MoE)**: 
  - Source Matcher: Verifies claims against source text
  - Hallucination Hunter: Detects hallucinations
  - Logic Checker: Ensures logical consistency
- **LLaMA 3.3 Integration**: Uses LLaMA 3.3 70B for language understanding

## Requirements

### Hardware Requirements

**For LLaMA 3.3 70B:**
- GPU with at least 40GB VRAM (with 8-bit quantization)
- GPU with at least 80GB VRAM (without quantization)

**Note:** If you don't have a GPU, the model will run on CPU but will be significantly slower.

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/dakshyadav1810/metacortex.git
cd MetaCortex
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up Hugging Face access (for LLaMA 3.3)**

You need to get access to LLaMA 3.3 models:
- Go to https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct
- Accept the license agreement
- Create a Hugging Face token: https://huggingface.co/settings/tokens
- Login via CLI:
```bash
huggingface-cli login
```

4. **Configure the model**

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` to choose your model:
```bash
LLAMA_MODEL=meta-llama/Llama-3.3-70B-Instruct

# Use 8-bit quantization (recommended)
USE_8BIT=true
```

## Data Preparation

Before running the app, you need to build the search index:

1. **Scrape MetaKGP wiki** (optional, if you don't have data):
```bash
python -m src.scraper.run
```

2. **Build the FAISS index**:
```bash
python -m src.retrieval.index
```

This will create `data/index/faiss.index` and `data/index/metadata.pkl`.

## Running the Application

Start the FastAPI server:

```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Usage

### Query Endpoint

**POST** `/query`

Request:
```json
{
  "query": "Who is the governor of Azad Hall?",
  "top_k": 5
}
```

Response:
```json
{
  "answer": "Based on the verified information...",
  "citations": [
    "https://wiki.metakgp.org/w/Azad_Hall",
    "https://wiki.metakgp.org/w/Halls_of_Residence"
  ]
}
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation.

## Architecture

```
Query → Vector Search → Claim Extraction → Graph Building → Path Sampling → MoE Verification → Answer Synthesis
                ↓              ↓                                      ↓
           FAISS Index    LLaMA 3.3 70B                     Multi-Expert Verification
```

## Project Structure

```
MetaCortex/
├── src/
│   ├── api/           # FastAPI application
│   ├── chatbot/       # Answer synthesis and citations
│   ├── reasoning/     # Graph-of-Thought components
│   ├── retrieval/     # Vector search and indexing
│   ├── scraper/       # Wiki scraping tools
│   └── verification/  # Multi-Expert verification
├── data/
│   ├── raw/          # Scraped wiki pages
│   ├── chunked/      # Chunked documents
│   └── index/        # FAISS index and metadata
└── requirements.txt
```

## Troubleshooting

### Out of Memory Error
- Enable 8-bit quantization: `USE_8BIT=true` in `.env`
- Reduce batch size or context length

### Model Download Issues
- Ensure you have accepted the LLaMA 3.3 license on Hugging Face
- Check your Hugging Face token is valid: `huggingface-cli whoami`

### Empty Search Results
- Ensure the FAISS index is built: `python -m src.retrieval.index`
- Check that data exists in `data/chunks/chunks.jsonl`

## License

This project uses LLaMA 3.3, which requires accepting Meta's license agreement on Hugging Face.
