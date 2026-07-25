# Technology Cost & Free-Tier Breakdown

Most technologies used or recommended for the Student Startup Ideation & Validation Platform are free, open source, or available with a free tier. Free-tier limits can change, so verify provider quotas before final deployment.

## Core Stack

| Component | Technology | Free? | Notes |
|---|---|---|---|
| Frontend | HTML5 | Yes, 100% free | Open standard |
| Frontend | CSS3 | Yes, 100% free | Open standard |
| Frontend | JavaScript | Yes, 100% free | Open standard |
| Frontend | Bootstrap 5 | Yes, 100% free | Open source |
| Charts | Chart.js | Yes, 100% free | MIT License |
| Backend | Python | Yes, 100% free | Open source |
| Backend | Flask | Yes, 100% free | BSD License |
| Authentication | Flask-Login | Yes, 100% free | Open source |
| ORM | SQLAlchemy | Yes, 100% free | Open source |
| Database | SQLite | Yes, 100% free | Built into Python |
| Database | MySQL Community | Yes, 100% free | Community Edition |
| AI Framework | LangChain | Yes, 100% free | Open source; optional enhancement |
| Vector Database | ChromaDB | Yes, 100% free | Open source; optional enhancement |
| Embeddings | Sentence Transformers | Yes, 100% free | Open source; optional enhancement |
| AI Model | Google Gemini API | Free tier | Daily/monthly usage limits apply |
| PDF Generation | ReportLab | Yes, 100% free | Community Edition is sufficient for project reports |
| Web Scraping | BeautifulSoup4 | Yes, 100% free | Open source |
| HTTP Requests | Requests | Yes, 100% free | Open source |
| Search | DuckDuckGo Search / ddgs | Yes, 100% free | No API key needed with supported libraries |
| Trends | pytrends | Yes, 100% free | Unofficial Google Trends client; optional enhancement |
| Data Processing | Pandas | Yes, 100% free | Open source; optional enhancement |
| Data Processing | NumPy | Yes, 100% free | Open source; optional enhancement |
| Visualization | Matplotlib | Yes, 100% free | Open source; optional enhancement |
| Visualization | Plotly | Yes, 100% free | Open source; optional enhancement |
| Environment Variables | python-dotenv | Yes, 100% free | Open source |
| Version Control | Git | Yes, 100% free | Open source |
| Repository Hosting | GitHub | Free plan | Suitable for student projects |
| Deployment | Render | Free tier | Good for demos and college projects |
| Deployment | Railway | Limited free usage | May require a paid plan if usage exceeds free credits |

## External APIs

| API | Free? | Notes |
|---|---|---|
| Google Gemini API | Free tier | Free quota with rate limits |
| Google Trends via pytrends | Yes | No API key required |
| DuckDuckGo Search / ddgs | Yes | Free search access via supported libraries |
| NewsAPI | Free developer plan | Limited daily requests; attribution may be required |

## Implementation Status

Deployment platforms are excluded from this status table. The project now implements the core web app, authentication, database, AI fallback/Gemini integration, search, charts, PDF reporting, vector retrieval, live trend/news hooks, and analytics/visualization utilities.

| Technology | Current Status | Evidence |
|---|---|---|
| HTML5 | Implemented | Flask templates in `app/templates/` |
| CSS3 | Implemented | Stylesheets in `app/static/css/` |
| JavaScript | Implemented | Scripts in `app/static/js/` |
| Bootstrap 5 | Implemented | Loaded in `app/templates/base.html` |
| Chart.js | Implemented | Loaded in `app/templates/base.html` and used by dashboard charts |
| Python | Implemented | Flask backend and AI engine |
| Flask | Implemented | App factory in `app/__init__.py` |
| Flask-Login | Implemented | Session auth in `app/routes/auth_routes.py` |
| SQLAlchemy | Implemented | Models in `app/models/__init__.py` |
| SQLite | Implemented | Default database in `config.py` |
| MySQL Community | Implemented as configurable database support | `config.py` supports `mysql://` URLs through PyMySQL |
| Google Gemini API | Implemented | `ai_engine/llm/gemini_service.py` uses Gemini when `GEMINI_API_KEY` is configured |
| ReportLab | Implemented | PDF tools in `ai_engine/tools/pdf_tool.py` |
| BeautifulSoup4 | Implemented | `ai_engine/tools/search_tool.py` can extract page titles and summaries |
| Requests | Implemented | Used by API/news tooling |
| DuckDuckGo Search / ddgs | Implemented | Search tool in `ai_engine/tools/search_tool.py` supports `ddgs` and legacy `duckduckgo_search` |
| python-dotenv | Implemented | Environment loading supported by project configuration |
| LangChain | Implemented | Used for knowledge chunking and startup tool wrappers |
| ChromaDB | Implemented | Used as a persistent vector store in `database/chroma_store` |
| Sentence Transformers | Implemented as optional runtime model | `ENABLE_SENTENCE_TRANSFORMERS=1` enables transformer embeddings; lightweight fallback remains default |
| pytrends | Implemented | Used by `ai_engine/tools/trend_tool.py` for Google Trends scoring |
| Pandas | Implemented | Used by analytics and trend utilities |
| NumPy | Implemented | Used by analytics and trend scoring |
| Matplotlib | Implemented | Generates market projection image charts |
| Plotly | Implemented | Powers advanced interactive market projection charts |
| NewsAPI | Implemented | `ai_engine/tools/news_tool.py` uses `NEWS_API_KEY` when configured |
| Git | Project tool, not app feature | Use for version control outside the running app |

## Project Recommendation

For a final-year college demo, the recommended zero-cost path is:

1. Use `SQLite` locally and on demo deployments.
2. Use heuristic AI fallbacks when `GEMINI_API_KEY` is not configured.
3. Use `Render` free tier for hosting demos.
4. Use `GitHub` free plan for repository hosting.
5. Keep `ENABLE_SENTENCE_TRANSFORMERS=0` for fast demos, or set it to `1` when you want transformer-based local embeddings.
