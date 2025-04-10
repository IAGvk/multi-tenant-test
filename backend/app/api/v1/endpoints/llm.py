from fastapi import APIRouter, Depends, HTTPException
from app.schemas.llm import LLMRequest, LLMResponse, RagRequest, FinalAnalysisRequest
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
    return LLMResponse(answer="This is a static response from the dummy LLM. Input image is a cloud based data and AI platform")

@router.post("/rag-query", response_model=LLMResponse)
async def rag_query(request: RagRequest):
    try:
        # Get embeddings
        query_vector = vector_db.get_embeddings(request.initial_response)
        
        # Search similar cases
        similar_cases = vector_db.search_similar(query_vector)
        
        # Construct the list of similar cases
        similar_cases_list = [
            {
                "id": str(idx),
                "text": case.payload.get('text'),
                "score": round(float(case.score), 3)
            }
            for idx, case in enumerate(similar_cases)
        ]

        return LLMResponse(
            answer=f"This is the Initial Response : {request.initial_response}",
            retrieved_contexts=similar_cases_list
        )
    except Exception as e:
        logger.error(f"Error in RAG query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 

@router.post("/final-analysis", response_model=LLMResponse)
async def final_analysis(request: FinalAnalysisRequest):
    try:
        final_response = f"""
        Initial Analysis:
        {request.initial_response}

        Enhanced Analysis based on selected similar cases:
        {'-' * 50}
        {chr(10).join(request.selected_contexts)}
        {'-' * 50}

        Final Recommendations:
        1. Security considerations identified
        2. Compliance requirements noted
        3. Architecture improvements suggested
        """
        
        return LLMResponse(answer=final_response)
    except Exception as e:
        logger.error(f"Error in final analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))