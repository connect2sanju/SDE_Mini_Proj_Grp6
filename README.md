# Hybrid Retrieval System

## Overview

This project implements a hybrid retrieval system that leverages both traditional keyword-based search and modern vector-based search approaches. The system is designed to be flexible and scalable, combining BM25 keyword retrieval, FAISS vector similarity retrieval, and an ensemble method to provide accurate search results.

The system includes different architectural patterns for organizing search functionalities:

- **Layered Pattern**
- **Client-Server Pattern**

## Files in the Project

### 1. `main.py`

This file defines a FastAPI web service that handles document retrieval using three types of search strategies:

- **BM25 Search**: A traditional keyword-based search using BM25 scoring.
- **FAISS Vector Search**: A similarity-based search using vector embeddings generated from OpenAI.
- **Hybrid Search (Ensemble)**: A combination of BM25 and FAISS searches using a weighted ensemble method.

#### Key Components:

- **Document List**: A small set of documents to test the search functionality.
- **Retrievers**:
  - `create_bm25_retriever`: Initializes a BM25 retriever for keyword searches.
  - `create_faiss_retriever`: Initializes a FAISS vector retriever for similarity-based searches.
  - `create_ensemble_retriever`: Combines the BM25 and FAISS retrievers for a hybrid search.

#### API Endpoints:

- **POST `/bm25_search`**: Accepts a query and performs a BM25 search.
- **POST `/faiss_search`**: Accepts a query and performs a FAISS vector search.
- **POST `/hybrid_search`**: Accepts a query and performs an ensemble search that combines BM25 and FAISS results.

#### How to Run:

1. Install dependencies (see `requirements.txt`).
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
