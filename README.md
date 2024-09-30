# Hybrid Retrieval System

The **Hybrid Retrieval System** is a document retrieval system that uses both **BM25** and **FAISS** algorithms to perform searches. The system is built using FastAPI and is deployed on Google Kubernetes Engine (GKE), ensuring scalability and reliability. This repository contains the code for the hybrid document retrieval engine, its configuration, and deployment details.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Cloud Infrastructure](#cloud-infrastructure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Deploying to Google Cloud](#deploying-to-google-cloud)
- [API Endpoints](#api-endpoints)
- [Input](#input)
- [Output](#output)

## Overview

The **Hybrid Retrieval System** is designed to perform document searches using a combination of the BM25 algorithm and FAISS-based retrieval. By leveraging the strengths of both methods, the system provides a hybrid search mechanism for more effective document retrieval.

## Features

- **BM25 Retriever**: Efficient lexical-based document search.
- **FAISS Retriever**: Fast approximate nearest neighbor search using embeddings generated via OpenAI API.
- **Hybrid Search**: Combines BM25 and FAISS search results to provide a robust and comprehensive search mechanism.
- **FastAPI**: A modern web framework to provide REST API endpoints for document search.
- **Google Cloud Deployment**: Scalable and reliable deployment using Kubernetes Engine and Container Registry.

## Architecture

The system is structured in a layered architecture as follows:

1. **Configuration Layer**: Manages environment variables and API keys.
2. **Service Layer**: Handles document retrieval services (BM25, FAISS, and hybrid retrieval).
3. **Business Logic Layer**: Implements core functionalities for searching documents.
4. **Presentation Layer**: Manages user interactions and outputs results.
5. **Data Layer**: Manages the documents and embeddings used in the search process.
6. **Cloud Infrastructure Layer**: Deploys the service on Google Cloud using Kubernetes for scalability and high availability.

## Cloud Infrastructure

### Google Cloud Components:
- **Google Cloud Container Registry**: Stores the Docker image for the application.
- **Google Kubernetes Engine (GKE)**: Manages the deployment, scaling, and orchestration of the containerized application.

### Deployment Features:
- **Kubernetes Pods**: Runs the FastAPI-based retrieval service.
- **Horizontal Pod Autoscaling**: Automatically scales the number of pods based on traffic.
- **Load Balancing**: Distributes traffic across multiple instances of the service for optimal performance.

## Installation

### Prerequisites:
- Python 3.8 or later
- Docker (Optional)
- Google Cloud SDK (for deployment) (Optional)
- Kubernetes command-line tool (`kubectl`) (Optional)

### Steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/connect2sanju/SDE_Mini_Proj_Grp6.git
    cd SDE_Mini_Proj_Grp6
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
   Create a `.env` file with the following:
    ```bash
    OPENAI_API_KEY=<your_openai_api_key>
    ```

4. **Build Docker Image**:
    ```bash
    docker build -t hybrid-retrieval-system .
    ```

## Running the Application

To run the application locally:

1. **Start the FastAPI application**:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

## Deploying to Google Cloud

### Steps:

1. **Build and push the Docker image to Google Cloud Container Registry**:
    ```bash
    gcloud builds submit --tag gcr.io/<your_project_id>/hybrid-retrieval-system
    ```

2. **Create a Kubernetes cluster**:
    ```bash
    gcloud container clusters create hybrid-retrieval-cluster --zone us-central1-a
    ```

3. **Create a Kubernetes namespace**
    ```bash
    kubectl create namespace <namespace-name>
    ```

4. **Deploy the application to GKE**:
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: hybrid-doc-retrieval
    namespace: <namespace-name>
    spec:
    replicas: 1
    selector:
        matchLabels:
        app: hybrid-doc-retrieval
    template:
        metadata:
        labels:
            app: hybrid-doc-retrieval
        spec:
        containers:
        - name: hybrid-doc-retrieval
            image: gcr.io/<your_project_id>/hybrid-retrieval-system:latest
            ports:
            - containerPort: 8000
    ```
    - Apply Kubernetes configurations using `kubectl`:
    ```bash
    kubectl apply -f deployment.yaml
    ```

5. **Expose the service**:
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
    name: hybrid-doc-retrieval-service
    namespace: <namespace-name>
    spec:
    selector:
        app: hybrid-doc-retrieval
    ports:
        - protocol: TCP
        port: 8000
        targetPort: 8000
    # type: ClusterIP  # Internal access only
    type: LoadBalancer  # Expose the service to the internet via LoadBalancer
    ```
    ```bash
    kubectl apply -f service.yaml
    ```

5. **Access the application**:
    Once the service is deployed, get the external IP
    ```bash
    kubectl get services -n 
    ```

## API Endpoints

- **/bm25_search**: Perform a search using the BM25 algorithm.
- **/faiss_search**: Perform a search using FAISS embeddings.
- **/hybrid_search**: Perform a hybrid search combining BM25 and FAISS.

## Input
```json
{
    "query": "Apple and a green fruit"
}
```

## Output
```json
{
    "results": [
        {
            "id": null,
            "metadata": {},
            "page_content": "I love fruit juice",
            "type": "Document"
        },
        {
            "id": null,
            "metadata": {},
            "page_content": "I like apples",
            "type": "Document"
        },
        {
            "id": null,
            "metadata": {},
            "page_content": "I like computers by Apple",
            "type": "Document"
        },
        {
            "id": null,
            "metadata": {},
            "page_content": "Apples and oranges are fruits",
            "type": "Document"
        }
    ]
}
```
