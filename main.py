from logging import getLogger
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from core.filter import filter_results
from core.search import search_product_urls
from models import SearchRequest, SearchResults

logger = getLogger(__name__)

load_dotenv()

app = FastAPI()


@app.post("/search", response_model=SearchResults)
def search(request: SearchRequest) -> List[Dict]:
    try:
        logger.info(f"Searching for {request.query} in {request.country}")

        search_results: SearchResults = search_product_urls(
            request.query, request.country
        )
        if not search_results.results:
            raise HTTPException(status_code=404, detail="No results found.")

        filtered_results: SearchResults = filter_results(search_results, request.query)

        return filtered_results
    except Exception as e:
        logger.error(f"Error searching for {request.query} in {request.country}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
