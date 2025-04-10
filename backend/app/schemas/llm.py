from pydantic import BaseModel
from typing import List, Optional

class LLMRequest(BaseModel):
    question: str
    context: str

class RagRequest(BaseModel):
    initial_response: str

class FinalAnalysisRequest(BaseModel):
    initial_response: str
    selected_contexts: List[str]

class RetrievedContext(BaseModel):
    id: str
    text: str
    score: float

class LLMResponse(BaseModel):
    answer: str
    retrieved_contexts: Optional[List[RetrievedContext]] = None