import os
from logging import getLogger

import requests

from exceptions import SearchAPIError
from models import SearchResult, SearchResults

logger = getLogger(__name__)


def search_product_urls(query: str, country: str) -> SearchResults:
    payload = {
        "source": "google_shopping_search",
        "geo_location": country,
        "parse": True,
        "query": query,
        "context": [{"key": "results_language", "value": "en"}],
    }

    response = requests.request(
        "POST",
        "https://realtime.oxylabs.io/v1/queries",
        auth=(os.environ.get("OXYLABS_USERNAME"), os.environ.get("OXYLABS_PASSWORD")),
        json=payload,
    )

    if response.status_code != 200:
        raise SearchAPIError(
            f"Error searching for {query} in {country}: {response.text}"
        )

    results = (
        response.json()["results"][0]
        .get("content", {})
        .get("results", {})
        .get("organic", [])
    )

    logger.info(f"Found {len(results)} results for {query} in {country}")

    search_results = []
    for result in results:
        search_results.append(
            SearchResult(
                title=result.get("title"),
                price=result.get("price_str"),
                link=result.get("merchant", {}).get("url"),
                currency=result.get("currency"),
                rating=str(result.get("rating")),
                reviews_count=result.get("reviews_count"),
            )
        )

    return SearchResults(results=search_results)
