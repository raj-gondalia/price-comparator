from typing import Optional

import openai

from config import settings
from exceptions import OpenAIError
from models import SearchResults
from prompts import FILTER_SEARCH_RESULTS_PROMPT
from utils.logging_config import LoggingConfig

logger = LoggingConfig.get_logger(__name__)


class FilterService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)

    def _format_results(self, search_results: SearchResults) -> str:
        formatted_results = []

        for i, result in enumerate(search_results.results):
            formatted_result = (
                f"{i+1}. Title: {result.title}\n"
                f"   Price: {result.price} {result.currency}\n"
                f"   Link: {result.link}\n"
                f"   Rating: {result.rating}\n"
                f"   Reviews: {result.reviews_count}"
            )
            formatted_results.append(formatted_result)

        return "\n".join(formatted_results)

    def _build_messages(self, user_query: str, formatted_results: str) -> list:
        return [
            {
                "role": "system",
                "content": FILTER_SEARCH_RESULTS_PROMPT.format(
                    user_query=user_query, formatted_results=formatted_results
                ),
            },
            {"role": "user", "content": "Remove the irrelevant results."},
        ]

    def _call_openai_api(
        self, messages: list, model: str, temperature: float
    ) -> SearchResults:
        try:
            response = self.client.beta.chat.completions.parse(
                model=model,
                temperature=temperature,
                messages=messages,
                response_format=SearchResults,
            )

            return response.choices[0].message.parsed

        except openai.APIError as e:
            raise OpenAIError(f"OpenAI API error: {e}")
        except Exception as e:
            raise OpenAIError(f"Error filtering results: {e}")

    def filter_results(
        self,
        search_results: SearchResults,
        user_query: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> SearchResults:
        """Filter search results using OpenAI"""
        model = model or settings.openai_model
        temperature = temperature or settings.openai_temperature

        if not search_results.results:
            logger.warning("No results to filter")
            return search_results

        logger.info(
            f"Filtering {len(search_results.results)} results for query: '{user_query}'"
        )

        formatted_results = self._format_results(search_results)
        messages = self._build_messages(user_query, formatted_results)
        filtered_results = self._call_openai_api(messages, model, temperature)

        logger.info(
            f"Filtered {len(search_results.results)} results to {len(filtered_results.results)} results"
        )

        return filtered_results
