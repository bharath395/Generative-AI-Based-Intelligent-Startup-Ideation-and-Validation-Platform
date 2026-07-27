"""
Test Suite: Integrated free/open-source tools added to the platform.
"""
from pathlib import Path

from ai_engine.tools.analytics_tool import (
    build_market_projection,
    build_plotly_market_projection,
    generate_matplotlib_projection_chart,
)
from ai_engine.tools.news_tool import fetch_market_news
from ai_engine.tools.search_tool import scrape_page_summary
from ai_engine.tools.langchain_tools import LANGCHAIN_STARTUP_TOOLS
from ai_engine.tools.trend_tool import fetch_google_trends_score
from app.models import StartupProject, User
from config import DATABASE_DIR


def test_analytics_tools_generate_projection_and_charts(tmp_path):
    projection = build_market_projection()
    plotly_chart = build_plotly_market_projection(projection)
    chart_path = tmp_path / "projection.png"

    generated_path = generate_matplotlib_projection_chart(projection, chart_path)

    assert len(projection) == 6
    assert "data" in plotly_chart
    assert Path(generated_path).exists()


def test_news_tool_fallback(monkeypatch):
    monkeypatch.setenv("NEWS_API_KEY", "")
    news = fetch_market_news("student startup", max_results=1)

    assert len(news) == 1
    assert "title" in news[0]


def test_beautifulsoup_scraper(monkeypatch):
    class FakeResponse:
        text = "<html><head><title>Demo</title><meta name='description' content='Startup market page'></head></html>"

        def raise_for_status(self):
            return None

    monkeypatch.setattr("ai_engine.tools.search_tool.requests.get", lambda *args, **kwargs: FakeResponse())

    summary = scrape_page_summary("https://example.com")

    assert summary["title"] == "Demo"
    assert summary["summary"] == "Startup market page"


def test_langchain_tool_registry_available():
    tool_names = {tool.name for tool in LANGCHAIN_STARTUP_TOOLS}

    assert "startup_web_search" in tool_names
    assert "startup_trend_score" in tool_names
    assert "startup_market_news" in tool_names
    assert "startup_page_summary" in tool_names


def test_chroma_persistent_store_created():
    from ai_engine.rag.retriever import retriever_instance

    assert retriever_instance.query("startup market", top_k=1)
    assert (DATABASE_DIR / "chroma_store").exists()


def test_trend_tool_returns_score():
    trend = fetch_google_trends_score("AI", ["startup"])

    assert "score" in trend
    assert 0 <= trend["score"] <= 100


def test_market_insights_endpoint(client, app):
    with app.app_context():
        user = User(
            name='Insight User',
            email='insight@test.com',
            department='CSE',
            skills='Python, AI',
        )
        user.set_password('password123')
        user.save()

        startup = StartupProject(
            user_id=user.id,
            startup_name='Insight AI',
            domain='AI',
            problem='Manual research',
            solution='Automated market intelligence',
            technology='Python, Flask, AI',
            target_customer='Students',
        )
        startup.save()

        client.post('/api/v1/login', json={
            'email': 'insight@test.com',
            'password': 'password123',
        })
        res = client.get(f'/api/v1/market-insights/{startup.id}')
        data = res.get_json()

        assert res.status_code == 200
        assert data['status'] == 'success'
        assert 'plotly_chart' in data
        assert 'projection' in data
        assert 'news' in data
