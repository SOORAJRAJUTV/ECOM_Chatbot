import sqlite3
from langchain_community.vectorstores import FAISS
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

DB_PATH = "sqlite:///./ecom.db"
FAISS_INDEX_PATH = "faiss_store"

# Initialize embeddings (open-source model)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_faiss_index():
    conn = sqlite3.connect("ecom.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price FROM products")
    rows = cursor.fetchall()
    conn.close()

    documents = []
    for r in rows:
        product_id, name, desc, price = r
        text = f"{name}. {desc}. Price: {price}"
        documents.append(Document(page_content=text, metadata={"id": product_id, "name": name, "price": price}))

    # Build FAISS
    vectorstore = FAISS.from_documents(documents, embedding_model)
    vectorstore.save_local(FAISS_INDEX_PATH)
    return vectorstore

def load_faiss_index():
    return FAISS.load_local(FAISS_INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)

if __name__ == "__main__": 
    build_faiss_index()
