from retrieval import Retriever
from llm import generate_answer
from guardrails import Guardrails
from config import TOP_K

guardrails = Guardrails()
retriever = Retriever()

query = "What is the weather today?"

valid, message = guardrails.validate_input(query)
if not valid: 
    print(message)
    exit()

chunks, scores = retriever.search(query, top_k=TOP_K)

valid, message = guardrails.validate_retrieval(scores)
if not valid:
    print(message)
    exit()

answer = generate_answer(query, chunks)

print("\n=== FINAL ANSWER ===\n")
print(answer)