from pydantic import BaseModel

class LLMRequest(BaseModel):
    question: str
    context: str

class LLMResponse(BaseModel):
    answer: str