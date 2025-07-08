from typing import List, Optional

import pycountry
from pydantic import BaseModel, field_validator


class SearchRequest(BaseModel):
    country: str
    query: str
    use_cache: bool = True

    @field_validator("query")
    @classmethod
    def validate_query(cls, query: str):
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        query = query.strip()

        if len(query) > 200:
            raise ValueError("Query too long (max 200 characters)")

        return query

    @field_validator("country")
    @classmethod
    def validate_country(cls, country: str):
        if not country or not country.strip():
            raise ValueError("Country cannot be empty")

        country = country.strip()

        if not pycountry.countries.get(name=country):
            raise ValueError(f"Invalid country name: {country}")

        return country


class SearchResult(BaseModel):
    title: str
    price: str
    link: Optional[str]
    currency: str
    rating: Optional[str]
    reviews_count: Optional[int]


class SearchResults(BaseModel):
    results: List[SearchResult]
