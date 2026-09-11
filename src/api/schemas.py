# api/schemas.py
from pydantic import BaseModel
from typing import List


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class AnswerResponse(BaseModel):
    answer: str
    citations: List[str]
