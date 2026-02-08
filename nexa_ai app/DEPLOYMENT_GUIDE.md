# 🚀 NEXA AI — Render Deployment Guide (Detailed)

This guide walks you through preparing your repository and deploying the `NEXA AI` Flask app to Render.com. It includes exact commands, environment variable setup, verification steps, and troubleshooting.

---

## Quick checklist (summary)

- Ensure `requirements.txt`, `Procfile`, and `runtime.txt` exist
- Ensure `app.py` exposes `app` (Flask app instance)
- Commit and push to GitHub
- Create Render Web Service and connect repo
- Add `SECRET_KEY` env var on Render
- Deploy and verify logs

---

## 1. Prepare your repository (local machine)

Open a terminal / PowerShell in your project root (the folder that contains `app.py`):

```powershell
cd "C:\Users\Administrator\Documents\nexa_ai app"

# Initialize git if needed
git init

# Add files and commit
git add .
git commit -m "Initial NEXA AI deployment"

# (Optional) Create remote repository on GitHub and add as origin
# Replace YOUR_USERNAME and repo name as appropriate
git remote add origin https://github.com/YOUR_USERNAME/nexa-ai-app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Notes:
- If you prefer the GitHub web UI: create a repo and upload files.
- If you have the GitHub CLI (`gh`) you can run `gh repo create YOUR_USERNAME/nexa-ai-app --public --source=. --remote=origin --push` to automate creation & push.

---

## 2. Mandatory files for Render (already present)

- `requirements.txt` — lists all Python dependencies (including `gunicorn`)
- `Procfile` — `web: gunicorn app:app`
- `runtime.txt` — Python version (e.g., `python-3.11.8`)

Render uses the `Start Command` to launch your app. For this repo the recommended start command is:

```
gunicorn app:app
```

If `app.py` lives in a package or a different module, change the import accordingly (e.g., `gunicorn mypackage.app:app`).

---

## 3. Create a Render Web Service

1. Sign in to https://render.com (choose GitHub sign-in for convenience)
2. From Render dashboard click **New** → **Web Service**
3. Choose your GitHub repo `nexa-ai-app`
4. Configure the service:
   - **Name:** `nexa-ai` (or any name)
   - **Environment:** `Python 3`
   - **Region:** Choose the closest region to your users
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Under **Environment** add variables:
   - `SECRET_KEY` = `a-long-random-string` (required for sessions)
   - Optionally: `PORT` (Render sets it automatically; not required)
6. Click **Create Web Service**

Render will queue a build and show live logs. When the build finishes, the service will be reachable at a Render-generated URL like `https://nexa-ai-xxxxx.onrender.com`.

---

## 4. Verify the deployment

After Render completes the build, verify with these steps:

- Visit the Render URL in your browser.
- Check Render logs for errors: Dashboard → Service → Logs.
- Use `curl` to confirm a 200 response:

```bash
curl -I https://your-render-url.onrender.com
```

Expected response header includes `200 OK` for the home page.

---

## 5. Environment & persistence notes

- Render's filesystem is ephemeral for web services: files written to the container (like `nexa-ai-student-data.json`) may be lost on restarts or instance changes. For production data persistence, use a managed database (Postgres), S3 for files, or Render's managed Postgres add-on.
- For simple deployments and demos, the local JSON file is fine, but don't rely on it for long-term storage.

---

## 6. Common issues & solutions

**Build error `ModuleNotFoundError`:**
- Ensure every imported package in `app.py` is listed in `requirements.txt`, then commit and push.

**App crashes on startup:**
- Check logs for stack trace. Common causes: missing `SECRET_KEY`, wrong `Start Command`, port bind errors.

**App works locally but fails on Render:**
- Compare Python versions (`python --version` locally vs `runtime.txt`).
- Check dependencies and ensure native packages (if any) are supported in the Render environment.

---

## 7. Updating the app (redeploy)

Make your code changes locally, then:

```powershell
git add .
git commit -m "Describe changes"
git push
```

Render will automatically start a new deployment for the pushed commit.

---

## 8. (Optional) Custom domain

1. Buy domain from any registrar (Namecheap, GoDaddy, Cloudflare, etc.)
2. On Render → Service → Settings → Custom Domains → Add Domain
3. Follow Render's DNS instructions (usually add a CNAME or A record)

---

## 9. Rollback

If a deployment introduces an error, go to Render → Deploys → choose an earlier successful deploy → click **Redeploy** to rollback.

---

## 10. Useful commands (local)

Start the Flask app locally for testing:

```powershell
"C:/Users/Administrator/Documents/nexa_ai app/.venv/Scripts/python.exe" app.py
```

Run the test suite (if present):

```powershell
python test_app.py
python test_flask.py
```

---

## 11. GitHub setup (if you haven't done it yet)

### Option A: Use GitHub CLI (fastest if installed)

```powershell
cd "C:\Users\Administrator\Documents\nexa_ai app"
gh repo create nexa-ai-app --public --source=. --remote=origin --push
```

### Option B: Manual GitHub setup

1. Go to https://github.com/new
2. Name it `nexa-ai-app`, choose "Public"
3. Click "Create repository"
4. Copy the HTTPS URL (e.g., `https://github.com/YOUR_USERNAME/nexa-ai-app.git`)
5. In PowerShell:

```powershell
cd "C:\Users\Administrator\Documents\nexa_ai app"
git remote add origin https://github.com/YOUR_USERNAME/nexa-ai-app.git
git branch -M main
git push -u origin main
```

### Option C: Upload via GitHub web UI (no git required)

1. Go to your new repo on GitHub
2. Click "Add file" → "Upload files"
3. Drag & drop all files from your project folder
4. Click "Commit changes"

---

## Need help?

I can:

- **Walk you through step-by-step** — I'll give you exact commands to paste, one by one
- **Verify your Render deployment** — Share your Render URL and I'll check the logs
- **Debug any errors** — Share error messages and I'll help fix them
- **Set up GitHub via `gh` CLI** — If you have it installed

Let me know which step you're stuck on and I'll help! 🚀
