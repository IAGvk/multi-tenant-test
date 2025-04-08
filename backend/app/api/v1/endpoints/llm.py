from fastapi import APIRouter, Depends, HTTPException
from app.schemas.llm import LLMRequest, LLMResponse, RagRequest
from app.vector_db.embeddings import VectorDBService
# import openai
# from app.core.config import settings

# router = APIRouter()

# @router.post("/query", response_model=LLMResponse)
# async def query_llm(request: LLMRequest, tenant_id: str = Depends()):
#     try:
#         openai.api_key = settings.OPENAI_API_KEY
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": request.question},
#                 {"role": "user", "content": f"Context: {request.context}"}
#             ]
#         )
#         return LLMResponse(answer=response["choices"][0]["message"]["content"])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



router = APIRouter()

vector_db = VectorDBService()

@router.post("/query", response_model=LLMResponse)
async def query_llm(request: LLMRequest):
    # Initial dummy response
    return LLMResponse(answer="This is a static response from the dummy LLM.")

@router.post("/rag-query", response_model=LLMResponse)
async def rag_query(request: RagRequest):
    # Get embeddings
    query_vector = vector_db.get_embeddings(request.initial_response)
    
    # Search similar cases
    similar_cases = vector_db.search_similar(query_vector)
    
    # Combine with initial response for final output
    enriched_response = f"""
    Initial Analysis: {request.initial_response}
    
    Similar Cases Found:
    {[case.payload.get('text') for case in similar_cases]}
    
    Final Enhanced Response: This is a RAG-enriched dummy response.
    """
    
    return LLMResponse(answer=enriched_response)