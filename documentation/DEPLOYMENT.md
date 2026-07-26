# Deployment Guide — Render Online Hosting

This guide walks you through deploying the Student Startup Ideation & Validation Platform to **Render** (free tier).

For the full free/open-source technology breakdown, see [Technology Cost & Free-Tier Breakdown](TECHNOLOGY_COST_BREAKDOWN.md).

---

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

## Step 2: Create a New Web Service on Render

1. Log in to [dashboard.render.com](https://dashboard.render.com).
2. Click **"New +"** → **"Web Service"**.
3. Connect your GitHub account and select the repository.
4. Configure the service:

| Setting | Value |
|---|---|
| **Name** | `student-startup-ai-platform` |
| **Environment** | Python |
| **Region** | Oregon (US West) or nearest |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt && python init_db.py` |
| **Start Command** | `gunicorn run:app --config gunicorn.conf.py` |
| **Instance Type** | Free |

---

## Step 3: Set Environment Variables

In the Render dashboard, go to **Environment** tab and add:

| `SECRET_KEY` | *(auto-generated or custom string)* | Required for Flask sessions |
| `MONGO_URI` | `mongodb+srv://<username>:<password>@cluster0.xxx.mongodb.net/student_startup_db?retryWrites=true&w=majority` | Cloud MongoDB Atlas URI for persistent database storage |
| `GEMINI_API_KEY` | *(your Google API key)* | Optional — heuristic mode works without it |
| `GEMINI_MODEL` | `gemini-3.6-flash` | Current Gemini model used for live generation |
| `NEWS_API_KEY` | *(your key)* | Optional |
| `ENABLE_SENTENCE_TRANSFORMERS` | `0` | Optional — set `1` only when the host can download/load the embedding model |
| `DISABLE_LIVE_AI` | `0` | Keep disabled for normal deployments |
| `PYTHON_VERSION` | `3.11.9` | Ensures correct Python runtime |

---

## How to Set Up Persistent MongoDB (MongoDB Atlas — 100% Free)

By default, if `MONGO_URI` is not set on Render, the app uses an in-memory database (`mongomock`) so the platform works out-of-the-box. However, in-memory data resets whenever Render sleeps or restarts. 

To store registered users and startup projects **permanently**:

1. Create a free account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas).
2. Create a **Free Shared Cluster (M0)**.
3. Under **Database Access**, create a Database User (e.g., `admin`) and password.
4. Under **Network Access**, click **Add IP Address** → select **Allow Access from Anywhere (`0.0.0.0/0`)**.
5. Click **Database** → **Connect** → **Drivers** → Copy your connection string:
   `mongodb+srv://<username>:<password>@cluster0.xxxxxx.mongodb.net/student_startup_db?retryWrites=true&w=majority`
6. In your **Render Dashboard** → go to your Web Service → **Environment** tab:
   - Add Environment Variable:
     - **Key**: `MONGO_URI`
     - **Value**: *(paste your connection string from step 5)*
7. Click **Save Changes**. Render will automatically redeploy and your database will be **100% permanent**!

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

## Alternative: One-Click Deploy with `render.yaml`

The project includes a `render.yaml` Infrastructure-as-Code file. To use it:

1. Push the repository to GitHub.
2. Go to [dashboard.render.com/select-repo](https://dashboard.render.com/select-repo).
3. Click **"New Blueprint Instance"**.
4. Select your repository — Render reads `render.yaml` automatically.
5. Review settings and click **"Apply"**.

---

## Updating the Deployment

After making code changes:

```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

Render auto-deploys on every push to `main` by default.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Build fails on `reportlab` | Ensure `requirements.txt` has `reportlab==4.2.2` |
| Database errors | Check that `init_db.py` runs in the build command |
| 500 errors | Check Render logs; ensure `SECRET_KEY` is set |
| AI features return heuristic data | Set `GEMINI_API_KEY` in environment variables |
| Free tier sleep | Free Render services sleep after 15 min inactivity; first request takes ~30s to wake |

---

## Production Checklist

- [x] Set a strong `SECRET_KEY` (not the default)
- [x] Set `GEMINI_API_KEY` for live AI generation
- [x] Verify `init_db.py` seeds the database
- [x] Test all pages after deployment
- [x] Verify advanced APIs for history, comparison, recommendations, progress, notifications, and admin analytics
- [ ] (Optional) Add a custom domain in Render settings
- [ ] (Optional) Upgrade to Render paid tier for persistent disk and no sleep
