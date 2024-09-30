from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

# Initialize OpenAI embeddings
embedding = OpenAIEmbeddings()

# Sample documents
doc_list = [
    "I like apples",
    "I like oranges",
    "Apples and oranges are fruits",
    "I like computers by Apple",
    "I love fruit juice"
]

app = FastAPI()

def create_bm25_retriever(docs, k=2):
    retriever = BM25Retriever.from_texts(docs)
    retriever.k = k
    return retriever

def create_faiss_retriever(docs, embedding, k=2):
    faiss_vectorstore = FAISS.from_texts(docs, embedding)
    return faiss_vectorstore.as_retriever(search_kwargs={"k": k})

def perform_bm25_search(retriever, query):
    return retriever.get_relevant_documents(query)

def perform_faiss_search(retriever, query):
    return retriever.get_relevant_documents(query)

def create_ensemble_retriever(bm25_retriever, faiss_retriever):
    return EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever],
                             weights=[0.5, 0.5])

def perform_ensemble_search(ensemble_retriever, query):
    return ensemble_retriever.get_relevant_documents(query)

# Initialize retrievers once when the application starts
bm25_retriever = create_bm25_retriever(doc_list)
faiss_retriever = create_faiss_retriever(doc_list, embedding)
ensemble_retriever = create_ensemble_retriever(bm25_retriever, faiss_retriever)

# Define request body model
class Query(BaseModel):
    query: str

@app.post("/bm25_search")
async def bm25_search(query: Query):
    results = perform_bm25_search(bm25_retriever, query.query)
    return {"results": results}

@app.post("/faiss_search")
async def faiss_search(query: Query):
    results = perform_faiss_search(faiss_retriever, query.query)
    return {"results": results}

@app.post("/hybrid_search")
async def hybrid_search(query: Query):
    results = perform_ensemble_search(ensemble_retriever, query.query)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    # Start the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
