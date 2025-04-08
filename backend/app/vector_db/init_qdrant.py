from app.vector_db.embeddings import VectorDBService
from qdrant_client.http import models
import numpy as np

from app.core.logger import get_logger
logger = get_logger(__name__)  # Use the centralized logger


# Sample architecture review documents
SAMPLE_DOCUMENTS = [
    """
    Architecture Review: Cloud-Native Payment System
    This microservices-based architecture implements a payment processing system using 
    containerized services deployed on Kubernetes. Key security features include end-to-end 
    encryption, mutual TLS between services, and HSM integration for key management.
    """,
    """
    Architecture Review: Data Lake Platform
    A hybrid cloud data platform utilizing AWS S3 for storage, Databricks for processing,
    and custom APIs for data access. Implements role-based access control and encryption
    at rest and in transit.
    """,
    """
    Architecture Review: Healthcare API Gateway
    HIPAA-compliant API gateway architecture with multiple layers of security controls,
    including OAuth2 authentication, request validation, and detailed audit logging.
    Deployed in a private cloud environment.
    """,
    """
    Architecture Review: Retail Order Processing
    Event-driven architecture using Apache Kafka for order processing. Implements saga
    pattern for distributed transactions, with circuit breakers and retry mechanisms
    for resilience.
    """,
    """
    Architecture Review: Financial Data Analytics
    Real-time analytics platform processing market data using Apache Flink and Redis.
    Implements strict data governance controls and maintains active-active deployment
    across multiple regions.
    """
]

def init_qdrant():
    """Initialize Qdrant with sample architecture reviews"""
    logger.info("Initializing Qdrant vector database...")
    vector_db = VectorDBService()
    
    try:
        # Create collection
        vector_db.create_collection()
        logger.info("Created vector collection")
        
        # Add sample documents
        for idx, doc in enumerate(SAMPLE_DOCUMENTS):
            # Get embeddings
            embedding = vector_db.get_embeddings(doc)
            
            # Store in Qdrant
            vector_db.client.upsert(
                collection_name=vector_db.collection_name,
                points=[
                    models.PointStruct(
                        id=idx,
                        vector=embedding.tolist(),
                        payload={"text": doc, 
                                "test_idx": idx}
                    )
                ]
            )
            logger.info(f"Added document {idx + 1}/{len(SAMPLE_DOCUMENTS)}")
        
        logger.info("Qdrant initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Error initializing Qdrant: {str(e)}")

# Optional: Test search functionality
def test_qdrant_search():
    vector_db = VectorDBService()
    test_query = "microservices security architecture"
    query_vector = vector_db.get_embeddings(test_query)
    results = vector_db.search_similar(query_vector)
    print("\nTest search results:")
    for res in results:
        print(f"Score: {res.score}, Text: {res.payload['text'][:100]}...")