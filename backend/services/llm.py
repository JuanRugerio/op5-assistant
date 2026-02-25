from openai import OpenAI
import os
from dotenv import load_dotenv
from config import OPENAI_MODEL, OPENAI_TEMPERATURE

load_dotenv()

#Ensembles OpenAI client to hit model endpoint. Ensembles prompt taking care of grounded answer.  
#Formats chunks to have a number, the page they came from and the text. Ensembles prompt with 
#user input and formatted retrieved chunks. Hit gpt 4o mini with prompt and 0 temperature
#(no creativity or risk freedom)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


PROMPT_TEMPLATE = """
You must ONLY answer using the provided context.

INSTRUCTIONS:
- Your answer MUST include:
  1. A clear answer to the question
  2. Supporting quotes copied EXACTLY from the context
  3. Citations for each quote in this format: (Chunk X, Page Y)

- DO NOT paraphrase the quotes.
- DO NOT use any external knowledge.
- If the answer is not explicitly in the context, say:
"I could not find this information in the Omnipod 5 user guide."

Context:
{chunks}

Question:
{user_input}

Answer format:

Answer:
<your answer>

Citations:
- "exact quote" (Chunk X, Page Y)
- "exact quote" (Chunk X, Page Y)
"""


def format_chunks(chunks):
    """
    Convert retrieved chunks into a readable context string
    with page references.
    """
    formatted = []

    for i, c in enumerate(chunks):
        formatted.append(
            f"Chunk {i+1} (Page {c['page']}):\n{c['text']}"
        )

    return "\n\n".join(formatted)


def generate_answer(user_input, retrieved_chunks):
    context = format_chunks(retrieved_chunks)

    prompt = PROMPT_TEMPLATE.format(
        chunks=context,
        user_input=user_input
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,  # fast + cheap + good enough for RAG
        messages=[
            {"role": "system", "content": "You are a precise assistant that answers only from provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=OPENAI_TEMPERATURE  # IMPORTANT: reduce hallucinations
    )

    return response.choices[0].message.content