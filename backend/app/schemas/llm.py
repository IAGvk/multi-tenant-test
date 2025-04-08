from pydantic import BaseModel

class LLMRequest(BaseModel):
    question: str
    context: str

class RagRequest(BaseModel):
    initial_response: str

class LLMResponse(BaseModel):
    answer: str