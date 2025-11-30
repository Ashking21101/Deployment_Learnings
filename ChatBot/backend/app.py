import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from fastapi.middleware.cors import CORSMiddleware




load_dotenv()

DB_FAISS_PATH = "faiss_db"

# Load vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

# LLM model
llm = ChatOpenAI(model="gpt-4o-mini")  # cheap + good for chatbot

app = FastAPI()


class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    retriever = vectorstore.as_retriever()
    docs = retriever.invoke(query.question)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are a customer support assistant of a clothing brand.
Answer only based on this info below (do not create anything extra):

=== INFO ===
{context}
=== END INFO ===

User question: {query.question}
Answer:
"""

    response = llm.invoke(prompt)
    return {"answer": response.content}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
