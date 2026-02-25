from fastapi import APIRouter
from pydantic import BaseModel
import time

from backend.services.guardrails import Guardrails
from backend.services.retrieval import Retriever
from backend.services.llm import generate_answer
from config import PDF_URL, TOP_K

#Establish how the input to endpoint must be. Install endpoint which will receive info and extract
#message.  Runs guardrails. Runs retrieval. Validates retrieval. Generates answer. Then citations. 
#Then prints together with latency. Health endpoint just verifies server is running. 
router = APIRouter()

guardrails = Guardrails()
retriever = Retriever()


# -----------------------------
# Request Schema
# -----------------------------
class ChatRequest(BaseModel):
    session_id: str
    message: str


# -----------------------------
# /chat endpoint
# -----------------------------
@router.post("/chat")
def chat(request: ChatRequest):
    try:
        start_time = time.time()

        query = request.message

        # --- BAD INPUT ---
        if not query or not query.strip():
            return {
                "answer": "Invalid input. Please provide a non-empty message.",
                "citations": [],
                "refused": True
            }
        
        # -----------------------------
        # 1. INPUT GUARDRAILS
        # -----------------------------
        valid, message = guardrails.validate_input(query)
        if not valid:
            return {
                "answer": message,
                "citations": [],
                "refused": True
            }

        # -----------------------------
        # 2. RETRIEVAL
        # -----------------------------
        chunks, scores = retriever.search(query, top_k=TOP_K)

        if not chunks:
                return {
                    "answer": "Knowledge base is empty or not initialized.",
                    "citations": [],
                    "refused": True
                }

        # -----------------------------
        # 3. RETRIEVAL GUARDRAILS
        # -----------------------------
        valid, message = guardrails.validate_retrieval(scores)
        if not valid:
            return {
                "answer": message,
                "citations": [],
                "refused": True
            }

    # -----------------------------
    # 4. GENERATE ANSWER
    # -----------------------------
            # --- LLM ---
        try:
            answer_text = generate_answer(query, chunks)
        except Exception as e:
            print("LLM ERROR:", str(e))
            return {
                "answer": "An internal error occurred while generating the answer.",
                "citations": [],
                "refused": True
            }
        # -----------------------------
        # 5. BUILD CITATIONS
        # -----------------------------
        citations = [
            {
                "source_url": PDF_URL,
                "page": c["page"],
                "quote": c["text"][:200]
            }
            for c in chunks
        ]

        # -----------------------------
        # 6. LOGGING
        # -----------------------------
        latency = time.time() - start_time
        print(f"Query={query} | Latency={latency:.2f}s | Chunks={len(chunks)}")

        return {
            "answer": answer_text,
            "citations": citations,
            "refused": False
        }

    except Exception as e:
            print("FATAL ERROR:", str(e))

            return {
                "answer": "A system error occurred. Please try again later.",
                "citations": [],
                "refused": True
            }

# -----------------------------
# /health endpoint
# -----------------------------
@router.get("/health")
def health():
    return {"status": "ok"}