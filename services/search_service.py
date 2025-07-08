import requests

from config import settings
from exceptions import SearchAPIError
from models import SearchResult, SearchResults
from utils.logging_config import LoggingConfig

logger = LoggingConfig.get_logger(__name__)


class SearchService:
    def __init__(self):
        self.api_url = "https://realtime.oxylabs.io/v1/queries"

    def search_products(self, query: str, country: str) -> SearchResults:
        logger.info(f"Searching for '{query}' in {country}")

        payload = {
            "source": "google_shopping_search",
            "geo_location": country,
            "parse": True,
            "query": query,
            "context": [{"key": "results_language", "value": "en"}],
        }

        response = requests.request(
            "POST",
            self.api_url,
            auth=(settings.oxylabs_username, settings.oxylabs_password),
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
