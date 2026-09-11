# api/app.py
from fastapi import FastAPI
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.api.schemas import QueryRequest, AnswerResponse

from src.retrieval.search import VectorSearcher
from src.reasoning.extract_claims import extract_claims_from_chunk
from src.reasoning.graph_builder import build_graph
from src.reasoning.path_sampler import sample_paths
from src.verification.moe import MoEVerifier
from src.chatbot.answer import synthesize_answer


# -----------------------------
# LLaMA-2 LLM Configuration
# -----------------------------
LLAMA_MODEL_NAME = os.getenv("LLAMA_MODEL", "meta-llama/Meta-Llama-3.1-8B-Instruct")  # e.g., 8B-Instruct or 70B-Instruct
USE_8BIT = os.getenv("USE_8BIT", "true").lower() == "true"  # Use 8-bit quantization to reduce memory

class LLaMALLM:
    def __init__(self):
        print(f"Loading LLaMA-2 model: {LLAMA_MODEL_NAME}")
        print(f"8-bit quantization: {USE_8BIT}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(LLAMA_MODEL_NAME)
        
        # Load model with 8-bit quantization if enabled (saves memory)
        if USE_8BIT:
            self.model = AutoModelForCausalLM.from_pretrained(
                LLAMA_MODEL_NAME,
                load_in_8bit=True,
                device_map="auto",
                torch_dtype=torch.float16
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                LLAMA_MODEL_NAME,
                device_map="auto",
                torch_dtype=torch.float16
            )
        
        self.model.eval()
        print("LLaMA-2 model loaded successfully")
    
    def generate(self, prompt: str, max_new_tokens: int = 256, temperature: float = 0.1) -> str:
        """
        Generate text using Llama 3.1 Instruct format.
        Uses lower temperature for more deterministic outputs.
        """
        # Format prompt for Llama 3.1 Instruct
        # Llama 3.x uses simple instruct-style prompts; we keep it minimal.
        chat_prompt = prompt.strip()
        
        inputs = self.tokenizer(chat_prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=True if temperature > 0 else False,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode and extract generated text
        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Heuristic: remove the original prompt prefix if present
        if full_text.startswith(chat_prompt):
            response = full_text[len(chat_prompt):].strip()
        else:
            response = full_text.strip()
        
        return response


# Initialize LLaMA-2
llama_llm = LLaMALLM()

def llm(prompt: str) -> str:
    """
    LLM interface using LLaMA-2 13B/7B.
    """
    return llama_llm.generate(prompt)


# -----------------------------
# Initialize components once
# -----------------------------
searcher = VectorSearcher()
verifier = MoEVerifier(llm)

app = FastAPI(title="GraphMind API")


@app.post("/query", response_model=AnswerResponse)
def query_graphmind(req: QueryRequest):
    # 1. Retrieval
    chunks = searcher.search(req.query, top_k=req.top_k)

    if not chunks:
        return AnswerResponse(
            answer="I don’t know based on the available MetaKGP data.",
            citations=[]
        )

    # 2. Claim extraction (GoT nodes)
    nodes = []
    for chunk in chunks:
        nodes.extend(extract_claims_from_chunk(chunk, llm))

    if not nodes:
        return AnswerResponse(
            answer="I don’t know based on the available MetaKGP data.",
            citations=[]
        )

    # 3. Graph construction
    edges = build_graph(nodes)

    # 4. Path sampling
    paths = sample_paths(nodes, edges)

    # 5. MoE verification
    verified_paths = []
    for path in paths:
        ok, _ = verifier.verify(path)
        if ok:
            verified_paths.append(path)

    # 6. Final answer
    result = synthesize_answer(verified_paths, llm)

    return AnswerResponse(
        answer=result["answer"],
        citations=result["citations"]
    )
