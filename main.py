from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status

from exceptions import OpenAIError, SearchAPIError
from models import SearchRequest, SearchResults
from services.filter_service import FilterService
from services.search_service import SearchService
from utils.cache_manager import cache_manager
from utils.logging_config import LoggingConfig
from utils.middleware import log_requests_middleware

# Initialize logging
logger = LoggingConfig.get_logger(__name__)

load_dotenv()

app = FastAPI()

# Add middleware
app.middleware("http")(log_requests_middleware)

# Initialize services
search_service = SearchService()
filter_service = FilterService()


@app.post("/search", response_model=SearchResults)
def search(request: SearchRequest) -> SearchResults:
    """Search for products and return filtered results"""
    try:
        logger.info(f"Searching for '{request.query}' in {request.country}")

        # Check cache first if enabled
        if request.use_cache:
            cached_results = cache_manager.get(request.query, request.country)
            if cached_results:
                logger.info(
                    f"Using cached filtered results for '{request.query}' in {request.country}"
                )
                return cached_results

        # Cache miss - perform search
        search_results = search_service.search_products(
            query=request.query, country=request.country
        )

        if not search_results.results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No results found"
            )

        # Filter results using OpenAI
        filtered_results = filter_service.filter_results(
            search_results=search_results, user_query=request.query
        )

        cache_manager.set(request.query, request.country, filtered_results)

        return filtered_results

    except SearchAPIError as e:
        logger.error(f"Search API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Search service unavailable"
        )
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Filtering service unavailable",
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}
