import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load OPENAI_API_KEY
load_dotenv()

DATA_PATH = "/Users/ashishtak/ChatBott/backend/data/faq.txt"
DB_FAISS_PATH = "faiss_db"

def create_vector_store():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = f.read()

    # Split data into small chunks for embedding
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs = splitter.split_text(data)

    # Create vector embeddings
    embeddings = OpenAIEmbeddings()

    # Build FAISS vector DB
    vectorstore = FAISS.from_texts(docs, embedding=embeddings)

    # Save locally
    vectorstore.save_local(DB_FAISS_PATH)
    print("FAISS vector store created successfully!")

if __name__ == "__main__":
    create_vector_store()
