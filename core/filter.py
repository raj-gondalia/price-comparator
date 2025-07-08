from logging import getLogger

import openai

from exceptions import OpenAIError
from models import SearchResults
from prompts import FILTER_SEARCH_RESULTS_PROMPT

logger = getLogger(__name__)


def filter_results(
    search_results: SearchResults, user_query: str, model="gpt-4o-mini", temperature=0.7
) -> SearchResults:
    formatted_results = "\n".join(
        [
            f"{i+1}. Title: {r.title}\n   Price: {r.price} {r.currency}\n   Link: {r.link}\n   Rating: {r.rating}\n   Reviews: {r.reviews_count}"
            for i, r in enumerate(search_results.results)
        ]
    )

    messages = [
        {
            "role": "system",
            "content": FILTER_SEARCH_RESULTS_PROMPT.format(
                user_query=user_query, formatted_results=formatted_results
            ),
        },
        {"role": "user", "content": "Remove the irrelevnat results."},
    ]

    try:
        client = openai.OpenAI()

        response = client.beta.chat.completions.parse(
            model=model,
            temperature=temperature,
            messages=messages,
            response_format=SearchResults,
        )

        filtered_results = response.choices[0].message.parsed

        logger.info(
            f"Filtered {len(search_results.results)} results to {len(filtered_results.results)} results"
        )

        return filtered_results
    except Exception as e:
        raise OpenAIError(f"Error filtering results: {e}")
