# Deployment Guide — 100% Free Options (No Paid Features Required)

This guide walks you through deploying the Student Startup Ideation & Validation Platform using **completely free** hosting options.

For the full free/open-source technology breakdown, see [Technology Cost & Free-Tier Breakdown](TECHNOLOGY_COST_BREAKDOWN.md).

---

## ⚠️ Important: Render Blueprint (render.yaml) is Paid

The `render.yaml` file in the project uses Render's **Blueprint** feature, which requires a **paid Render subscription**. Instead, use the **Manual Web Service** method below which works on Render's **Free Tier**.

---

# Option 1: Render (Free Tier — Manual Setup) ✅ Recommended

## Prerequisites

1. A **GitHub account** with a repository containing this project.
2. A **Render account** (free at [render.com](https://render.com)).
3. (Optional) A **Google Gemini API Key** for live AI generation.

---

## Step 1: Push Code to GitHub

```bash
# Initialize git repository (if not already)
git init
git add .
git commit -m "Initial commit: Student Startup AI Platform"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/student-startup-ai-platform.git
git branch -M main
git push -u origin main
```

---

## Step 2: Create a New Web Service on Render (Manual — FREE)

> **Note:** Do NOT use "Blueprint" — that requires payment. Use the manual Web Service method below.

1. Log in to [dashboard.render.com](https://dashboard.render.com).
2. Click **"New +"** → **"Web Service"**.
3. Connect your GitHub account and select your repository.
4. Configure the service:

| Setting | Value |
|---|---|
| **Name** | `student-startup-ai-platform` |
| **Environment** | Python |
| **Region** | Oregon (US West) or nearest |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt && python init_db.py` |
| **Start Command** | `gunicorn run:app --config gunicorn.conf.py` |
| **Instance Type** | **Free** ✅ |

---

## Step 3: Set Environment Variables

In the Render dashboard, go to **Environment** tab and add:

| Key | Value | Required? |
|---|---|---|
| `SECRET_KEY` | *(generate a random secure string)* | ✅ Required |
| `GEMINI_API_KEY` | *(your Google Gemini API key)* | ⚠️ Optional — works without it |
| `NEWS_API_KEY` | *(your NewsAPI key)* | ⚠️ Optional |
| `ENABLE_SENTENCE_TRANSFORMERS` | `0` | ⚠️ Optional |
| `DISABLE_LIVE_AI` | `0` | ⚠️ Optional |
| `PYTHON_VERSION` | `3.12.0` | ✅ Recommended |

---

## Step 4: Deploy

1. Click **"Create Web Service"**.
2. Render will automatically:
   - Install Python dependencies from `requirements.txt`
   - Run `python init_db.py` to create the database and seed demo data
   - Start the Gunicorn WSGI server
3. Wait for the build to complete (typically 2–4 minutes).
4. Your app will be live at: `https://student-startup-ai-platform.onrender.com`

---

## Step 5: Verify Deployment

1. Open the Render URL in your browser.
2. You should see the glassmorphic landing page.
3. Log in with demo credentials:
   - **Email**: `student@gmail.com`
   - **Password**: `student123`
4. Test the AI Idea Generator, Dashboard, and Mentor Chat.

---

# Option 2: PythonAnywhere (Free Tier) 🐍

PythonAnywhere offers a **free tier** perfect for Flask apps. No credit card required.

## Step 1: Create Account
- Go to [pythonanywhere.com](https://www.pythonanywhere.com) and sign up for a **Free** account.

## Step 2: Upload Code
- Open the **Dashboard** → **Files** tab.
- Upload your project files (or clone from GitHub via the **Bash console**):
  ```bash
  git clone https://github.com/YOUR_USERNAME/student-startup-ai-platform.git
  ```

## Step 3: Set Up Virtual Environment
- Open a **Bash console** from the Dashboard.
- Run:
  ```bash
  cd student-startup-ai-platform
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python init_db.py
  ```

## Step 4: Configure Web App
- Go to **Web** tab → **Add a new web app**.
- Choose **Manual configuration** → **Python 3.10**.
- In the **Code** section:
  - **Source code:** `/home/YOUR_USERNAME/student-startup-ai-platform`
  - **Working directory:** `/home/YOUR_USERNAME/student-startup-ai-platform`
  - **WSGI configuration file:** Click the link to edit, replace content with:

```python
import sys
import os

path = '/home/YOUR_USERNAME/student-startup-ai-platform'
if path not in sys.path:
    sys.path.append(path)

os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-secure-random-key-here'

from app import create_app
application = create_app('production')
```

> **Replace `YOUR_USERNAME`** with your actual PythonAnywhere username.

- In **Environment variables** section (under Web tab), add:
  - `FLASK_ENV` = `production`
  - `SECRET_KEY` = `your-secure-random-string`
  - `GEMINI_API_KEY` = `your-key` (optional)

## Step 5: Reload
- Click the green **Reload** button.
- Your app will be live at: `https://YOUR_USERNAME.pythonanywhere.com`

---

# Option 3: Railway (Free Tier with Monthly Credits) 🚂

Railway offers **$5 free credits monthly** — enough for a small Flask app.

## Step 1: Create Account
- Go to [railway.app](https://railway.app) and sign up with GitHub.

## Step 2: Deploy
- Click **New Project** → **Deploy from GitHub repo**.
- Select your repository.
- Add environment variables (same as Render list above).
- Railway auto-detects Python and uses:
  - **Build Command:** `pip install -r requirements.txt && python init_db.py`
  - **Start Command:** `gunicorn run:app --config gunicorn.conf.py`

## Step 3: Access
- Railway provides a `.railway.app` URL automatically.

---

# Option 4: Koyeb (Free Tier) 🌍

Koyeb offers a **free tier** with always-on instances (no sleep!).

## Step 1: Create Account
- Go to [koyeb.com](https://www.koyeb.com) and sign up with GitHub.

## Step 2: Deploy
- Click **Create App** → **Deploy from GitHub**.
- Select your repository.
- Set **Builder** to **Docker** or use these settings:
  - **Run Command:** `gunicorn run:app --config gunicorn.conf.py`
  - **Environment Variables:** Add same as Render list.

---

## Updating Your Deployment (Any Platform)

After making code changes:

```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

- **Render:** Auto-deploys on push
- **PythonAnywhere:** Open the Web tab and click **Reload**
- **Railway:** Auto-deploys on push
- **Koyeb:** Auto-deploys on push

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Build fails on `reportlab` | Ensure `requirements.txt` has `reportlab==4.2.2` |
| Build fails on `tokenizers` / Rust compilation error | **Fix:** A `runtime.txt` file has been added to the project root with `python-3.12.0` to force Python 3.12. Render's default Python 3.14 doesn't have prebuilt wheels for `tokenizers`. Also `tokenizers==0.20.3` has been removed from `requirements.txt` — `transformers` will install a compatible version automatically. |
| Database errors | Check that `init_db.py` runs in the build command |
| 500 errors | Check platform logs; ensure `SECRET_KEY` is set |
| AI features return heuristic data | Set `GEMINI_API_KEY` in environment variables |
| Render free tier sleep | Free Render services sleep after 15 min inactivity; first request takes ~30s to wake |
| PythonAnywhere free tier limits | Outbound HTTP blocked on free tier (AI search/trends won't work); use Render instead if you need AI features |

---

## Production Checklist

- [x] Set a strong `SECRET_KEY` (not the default)
- [x] Set `GEMINI_API_KEY` for live AI generation
- [x] Verify `init_db.py` seeds the database
- [x] Test all pages after deployment
- [ ] (Optional) Add a custom domain in hosting settings
