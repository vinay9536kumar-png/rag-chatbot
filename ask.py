import os

import chromadb
from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer

load_dotenv()

MODEL = "gemini-3.8-flash"
DB_PATH = "chroma_db"
COLLECTION = "pdf_docs"

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY nahi mili. .env file check karo.")

client = genai.Client(api_key=api_key)
embedder = SentenceTransformer("all-MiniLM-L6-v2")
collection = chromadb.PersistentClient(path=DB_PATH).get_collection(COLLECTION)


def ask(question):
    q_emb = embedder.encode([question]).tolist()
    result = collection.query(query_embeddings=q_emb, n_results=3)
    chunks = result["documents"][0]
    pages = sorted({m["page"] for m in result["metadatas"][0]})

    context = "\n\n".join(chunks)
    prompt = (
        "Answer the question using only the context below. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}"
    )
    reply = client.models.generate_content(model=MODEL, contents=prompt)
    return reply.text, pages


def main():
    print("PDF chatbot ready. Band karne ke liye 'exit' likho.\n")
    while True:
        question = input("Sawal: ").strip()
        if question.lower() in ("exit", "quit", ""):
            break
        answer, pages = ask(question)
        print(f"\nJawab: {answer}")
        print(f"(Source pages: {pages})\n")


if __name__ == "__main__":
    main()
    