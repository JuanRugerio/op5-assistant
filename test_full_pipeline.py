from backend.services.retrieval import Retriever
from backend.services.llm import generate_answer
from backend.services.guardrails import Guardrails

query = "How do I change a pod?"

guardrails = Guardrails()
retriever = Retriever()

# -----------------------------
# 1. INPUT GUARDRAILS
# -----------------------------
valid, message = guardrails.validate_input(query)
if not valid:
    print("BLOCKED:", message)
    exit()

# -----------------------------
# 2. RETRIEVAL
# -----------------------------
chunks, scores = retriever.search(query, top_k=5)

print("\n--- DEBUG ---")
print("Scores:", scores)
print("Top chunk preview:", chunks[0]["text"][:200] if chunks else "NONE")
print("---------------\n")

# -----------------------------
# 3. RETRIEVAL GUARDRAILS
# -----------------------------
valid, message = guardrails.validate_retrieval(scores)
if not valid:
    print("BLOCKED:", message)
    exit()

# -----------------------------
# 4. LLM
# -----------------------------
answer = generate_answer(query, chunks)

print("\n=== FINAL ANSWER ===\n")
print(answer)