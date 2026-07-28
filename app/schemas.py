from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    found: bool
    content: str | None = None
    message: str | None = None


class GenerateRequest(BaseModel):
    query: str


class GenerateResponse(BaseModel):
    success: bool
    message: str
    content: str | None
    file_path: str | None
