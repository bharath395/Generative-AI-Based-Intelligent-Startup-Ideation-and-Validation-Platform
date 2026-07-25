import os

import requests


def fetch_market_news(query, max_results=3):
    """
    Fetches NewsAPI market context when NEWS_API_KEY is configured.
    Returns deterministic fallback items when the API is unavailable.
    """
    api_key = os.getenv("NEWS_API_KEY", "")
    if api_key:
        try:
            response = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": query,
                    "language": "en",
                    "sortBy": "relevancy",
                    "pageSize": max_results,
                    "apiKey": api_key,
                },
                timeout=8,
            )
            response.raise_for_status()
            articles = response.json().get("articles", [])
            if articles:
                return [
                    {
                        "title": article.get("title"),
                        "source": article.get("source", {}).get("name"),
                        "url": article.get("url"),
                        "summary": article.get("description") or article.get("content"),
                    }
                    for article in articles[:max_results]
                ]
        except Exception:
            pass

    return [
        {
            "title": f"{query.title()} adoption continues to grow",
            "source": "Heuristic News Context",
            "url": "https://newsapi.org/",
            "summary": f"Recent market signals suggest continued demand for {query} solutions.",
        }
    ]
