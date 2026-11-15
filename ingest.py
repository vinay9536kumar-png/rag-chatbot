import fitz  # PyMuPDF
import chromadb
from sentence_transformers import SentenceTransformer

PDF_PATH = "sample.pdf"
DB_PATH = "chroma_db"
COLLECTION = "pdf_docs"


def load_pages(path):
    doc = fitz.open(path)
    return [(i + 1, page.get_text()) for i, page in enumerate(doc)]


def chunk_text(text, size=800, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


def main():
    print("Loading embedding model (first run downloads it)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION)

    ids, docs, metas = [], [], []
    for page_no, text in load_pages(PDF_PATH):
        for j, chunk in enumerate(chunk_text(text)):
            if chunk.strip():
                ids.append(f"p{page_no}_c{j}")
                docs.append(chunk)
                metas.append({"page": page_no})

    print(f"Created {len(docs)} chunks. Embedding...")
    embeddings = model.encode(docs).tolist()
    collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings)
    print(f"Done. Stored {len(docs)} chunks in '{DB_PATH}'.")


if __name__ == "__main__":
    main()
