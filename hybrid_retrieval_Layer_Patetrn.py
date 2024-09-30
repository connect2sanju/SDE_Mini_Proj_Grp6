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

def create_bm25_retriever(docs, k=2):
    """Initialize and return a BM25 retriever."""
    retriever = BM25Retriever.from_texts(docs)
    retriever.k = k
    return retriever

def create_faiss_retriever(docs, embedding, k=2):
    """Initialize and return a FAISS retriever."""
    faiss_vectorstore = FAISS.from_texts(docs, embedding)
    return faiss_vectorstore.as_retriever(search_kwargs={"k": k})

def perform_bm25_search(retriever, query):
    """Perform a BM25 search and return the results."""
    return retriever.get_relevant_documents(query)

def perform_faiss_search(retriever, query):
    """Perform a FAISS search and return the results."""
    return retriever.get_relevant_documents(query)

def create_ensemble_retriever(bm25_retriever, faiss_retriever):
    """Initialize and return an ensemble retriever."""
    return EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever],
                             weights=[0.5, 0.5])

def perform_ensemble_search(ensemble_retriever, query):
    """Perform a hybrid search and return the results."""
    return ensemble_retriever.get_relevant_documents(query)

def main():
    # Create retrievers
    bm25_retriever = create_bm25_retriever(doc_list)
    faiss_retriever = create_faiss_retriever(doc_list, embedding)

    bm25_query_2 = "Apple and a green fruit"
    bm25_results_2 = perform_bm25_search(bm25_retriever, bm25_query_2)
    print("\n==>BM25 Search Results for query '{}':".format(bm25_query_2))
    for doc in bm25_results_2:
        print(" -", doc)

    # Vector Search: Using FAISS Retriever
    faiss_query = "Apple and a green fruit"
    faiss_results = perform_faiss_search(faiss_retriever, faiss_query)
    print("\n==>FAISS Search Results for query '{}':".format(faiss_query))
    for doc in faiss_results:
        print(" -", doc)

    # Hybrid Search: Using Ensemble Retriever
    ensemble_retriever = create_ensemble_retriever(bm25_retriever, faiss_retriever)
    ensemble_query = "Apple and a green fruit"
    ensemble_results = perform_ensemble_search(ensemble_retriever, ensemble_query)
    print("\n==>Hybrid Search Results for query '{}':".format(ensemble_query))
    for doc in ensemble_results:
        print(" -", doc)

if __name__ == "__main__":
    main()
