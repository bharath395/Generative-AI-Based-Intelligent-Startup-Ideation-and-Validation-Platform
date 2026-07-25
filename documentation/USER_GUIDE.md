# User Guide — Generative AI-Based Intelligent Startup Ideation and Validation Platform

## Getting Started

### 1. Register an Account
1. Navigate to the landing page at `http://localhost:5000`.
2. Click **"Register as Student"** or **"Get Started"**.
3. Fill in your Full Name, Email, Department, Technical Skills, and a password.
4. Click **"Create Account"** — you'll be redirected to the Dashboard.

### 2. Login
1. Go to the Login page.
2. Enter your registered email and password.
3. Optionally check "Remember me" for persistent sessions.
4. Click **"Log In"**.

**Demo Credentials** (auto-created by `init_db.py`):
- Email: `student@gmail.com`
- Password: `student123`

For free/open-source technology and API cost details, see [Technology Cost & Free-Tier Breakdown](TECHNOLOGY_COST_BREAKDOWN.md).

---

## Core Features

### 🧠 AI Startup Idea Generator
1. Navigate to **AI Generator** from the navbar or sidebar.
2. Enter your **Target Domain** (e.g., Agriculture, Healthcare, EdTech).
3. Enter your **Technical Skills** (e.g., Python, Machine Learning, IoT).
4. Select your **Budget Range**.
5. Optionally add your **Interest Area**.
6. Click **"Launch Multi-Agent AI Pipeline"**.
7. Watch the animated pipeline progress as 10 specialized AI agents work:
   - Idea Generation → Market Research → Competitor Analysis → Validation Scoring → Business Canvas → Financial Planning → Risk Assessment → Pitch Content
8. View the generated startup idea with Problem, Solution, Tech Stack, and Innovation Score.

### 📊 Dashboard
- View summary statistics: Total Ideas, Average Validation Score, Reports Created, Saved Projects.
- Interactive **Domain Distribution** bar chart (Chart.js).
- **Market Growth Projection** line chart (2023–2028).
- Table of all your startup projects with actions.
- Track startup progress, recent notifications, and saved project history through the advanced APIs.

### 📈 Market Analysis
- View estimated **Market Size** (TAM), **Growth Rate** (CAGR), **Trend Score**, and **Customer Demand Level**.
- Interactive growth valuation trend chart.

### 🏢 Competitor Matrix
- Side-by-side comparison table of competitor companies.
- Strengths, weaknesses, pricing, and technology comparison.
- Identified **Market Gaps** and opportunities.

### ⭐ Validation Score
- **Weighted Formula**: `Overall = (Innovation × 25%) + (Market × 30%) + (Tech × 25%) + (Business × 20%)`
- Radar chart visualization of score breakdown.
- Progress bars for each parameter.
- Risk level assessment and recommendation.

### 🧩 Business Model Canvas
- Full 9-block interactive Business Model Canvas:
  - Key Partners, Key Activities, Value Proposition, Customer Relationships, Customer Segments, Cost Structure, Revenue Streams, Channels, Key Resources.

### 🎤 Pitch Deck Generator
- AI-generated investor pitch content organized as slide cards.
- Covers: Tagline, Problem, Solution, Market Opportunity, Business Model, Investment Ask, Future Vision.

### 💬 AI Startup Mentor Chat
- 24/7 interactive chatbot for startup guidance.
- Powered by RAG (Retrieval-Augmented Generation) knowledge base.
- Maintains conversation context and memory.
- Ask about market sizing, pricing strategies, technical architecture, etc.

### Idea Comparison & Recommendations
- Compare two or more saved startup ideas to identify the strongest weighted validation score.
- Get AI-style startup direction recommendations based on your skills, interests, and previous project domains.

### 📄 PDF Report Downloads
- Click **"Generate New Report"** to compile a professional PDF.
- Report includes: Executive Summary, Validation Score Table, Business Model Overview, Financial Projections, Strategic Recommendations.
- Click **"Download PDF"** to save the report.

### 👤 Profile Management
- Update your Name, Department, Skills, and Interest areas.
- Email is read-only after registration.

---

## Theme Toggle
- Click the **🌙 Dark / ☀️ Light** button in the navbar to switch between dark and light modes.
- Your preference is saved in localStorage.

---

## Keyboard Shortcuts
- **Enter** in chat input sends the message.
- **Tab** navigates between form fields.
