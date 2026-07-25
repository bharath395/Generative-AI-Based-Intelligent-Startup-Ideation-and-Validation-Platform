import os

import numpy as np
import pandas as pd


def calculate_trend_score(domain, keywords):
    """
    Evaluates market interest score (0-100) based on domain and technology keywords.
    """
    high_growth_terms = ['ai', 'machine learning', 'agritech', 'fintech', 'edtech', 'healthtech', 'saas', 'iot', 'robotics', 'cloud', 'cybersecurity']
    score = 75.0
    combined = f"{domain} {' '.join(keywords)}".lower()
    
    for term in high_growth_terms:
        if term in combined:
            score += 4.5

    return min(98.5, round(score, 1))


def fetch_google_trends_score(domain, keywords=None):
    """
    Uses pytrends to calculate a Google Trends interest score.
    Falls back to the local heuristic when live trends are unavailable.
    """
    keywords = keywords or []
    terms = [domain] + list(keywords)
    terms = [term for term in terms if term][:5]

    try:
        from pytrends.request import TrendReq
        proxies = [
            proxy.strip()
            for proxy in os.getenv("PYTRENDS_PROXIES", "").split(",")
            if proxy.strip()
        ]
        timeout = (
            int(os.getenv("PYTRENDS_CONNECT_TIMEOUT", "5")),
            int(os.getenv("PYTRENDS_READ_TIMEOUT", "10")),
        )
        pytrends = TrendReq(
            hl=os.getenv("PYTRENDS_LANGUAGE", "en-US"),
            tz=int(os.getenv("PYTRENDS_TIMEZONE", "330")),
            timeout=timeout,
            proxies=proxies,
            retries=int(os.getenv("PYTRENDS_RETRIES", "2")),
            backoff_factor=float(os.getenv("PYTRENDS_BACKOFF_FACTOR", "0.1")),
        )
        pytrends.build_payload(terms, timeframe="today 12-m")
        frame = pytrends.interest_over_time()
        if not frame.empty:
            numeric = frame.drop(columns=["isPartial"], errors="ignore")
            average_interest = float(numeric.mean().mean())
            momentum = float(numeric.tail(4).mean().mean() - numeric.head(4).mean().mean())
            score = np.clip(average_interest + (momentum * 0.4), 0, 100)
            return {
                "score": round(float(score), 1),
                "source": "Google Trends via pytrends",
                "series": numeric.reset_index().tail(12).to_dict(orient="records"),
            }
    except Exception:
        pass

    return {
        "score": calculate_trend_score(domain, keywords),
        "source": "Heuristic trend model",
        "series": pd.DataFrame({
            "keyword": terms or [domain],
            "interest": [calculate_trend_score(domain, keywords)] * max(1, len(terms or [domain])),
        }).to_dict(orient="records"),
    }
