# Generative AI-Based Intelligent Startup Ideation and Validation Platform

Generative AI-Based Intelligent Startup Ideation and Validation Platform is an AI-powered platform that helps entrepreneurs and students generate innovative startup ideas and evaluate their feasibility. It uses Generative AI to suggest business ideas based on user interests, market trends, and emerging technologies. The platform also validates each idea by analysing market demand, competition, target customers, potential risks, and revenue models. It provides recommendations to improve the idea, making it easier for users to choose and develop startups with a higher chance of success.

## Documentation

- [User Guide](documentation/USER_GUIDE.md)
- [API Documentation](documentation/API_DOCUMENTATION.md)
- [Deployment Guide](documentation/DEPLOYMENT.md)
- [Technology Cost & Free-Tier Breakdown](documentation/TECHNOLOGY_COST_BREAKDOWN.md)
- [Official API & Tool Links](documentation/OFFICIAL_TOOL_LINKS.md)

## Quick Start

```bash
pip install -r requirements.txt
python init_db.py
python run.py
```

Open `http://localhost:5000` and log in with:

- Email: `student@gmail.com`
- Password: `student123`

## Optional AI/Data Settings

- `GEMINI_API_KEY`: enables live Gemini generation.
- `NEWS_API_KEY`: enables live NewsAPI market signals.
- `ENABLE_SENTENCE_TRANSFORMERS=1`: enables local transformer embeddings for RAG; first run may download the model.
- `DATABASE_URL=mysql://user:password@host/dbname`: enables MySQL through PyMySQL.
