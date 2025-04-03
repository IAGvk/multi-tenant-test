from fastapi import APIRouter, Depends, HTTPException
from app.schemas.llm import LLMRequest, LLMResponse
import openai
from app.core.config import settings

router = APIRouter()

@router.post("/query", response_model=LLMResponse)
async def query_llm(request: LLMRequest, tenant_id: str = Depends()):
    try:
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.question},
                {"role": "user", "content": f"Context: {request.context}"}
            ]
        )
        return LLMResponse(answer=response["choices"][0]["message"]["content"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))