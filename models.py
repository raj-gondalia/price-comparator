from typing import List, Optional

from pydantic import BaseModel


class SearchRequest(BaseModel):
    country: str
    query: str


class SearchResult(BaseModel):
    title: str
    price: str
    link: Optional[str]
    currency: str
    rating: Optional[str]
    reviews_count: Optional[int]


class SearchResults(BaseModel):
    results: List[SearchResult]
