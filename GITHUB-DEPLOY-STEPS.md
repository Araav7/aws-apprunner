# 🚀 Quick GitHub to App Runner Deployment

## Step 1: Push to GitHub

```bash
# Initialize git in your project folder
cd /Users/araavind.senthil/hello-world-aws
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Python app with Datadog APM"

# Create repo on GitHub (via web) then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 2: Connect App Runner to GitHub

1. **AWS Console** → **App Runner** → **Create service**
2. Choose **"Source code repository"**
3. Click **"Add New"** to connect GitHub
4. **Install GitHub app** on your repository
5. Select your repo and branch (`main`)

## Step 3: Configure Service

App Runner will auto-detect `apprunner.yaml`, so just:

1. **Service name:** `simple-trace-app`
2. **Instance:** 0.25 vCPU, 0.5 GB RAM
3. **Deployment:** Choose "Automatic" for push-to-deploy
4. Click **"Create & deploy"**

## Step 4: Wait & Test

After ~5 minutes, get your URL from App Runner console:

```bash
# Test it
curl https://YOUR-APP-URL.ap-southeast-1.awsapprunner.com/health
curl https://YOUR-APP-URL.ap-southeast-1.awsapprunner.com/
```

## Step 5: Check Datadog

Go to **Datadog APM** → Look for `simple-trace-app` service

---

### Files You Need:
✅ `app.py` - Your Flask app  
✅ `requirements.txt` - Dependencies  
✅ `apprunner.yaml` - Configuration (already set up!)  

### To Update:
```bash
git add . && git commit -m "Update" && git push
# App Runner auto-deploys in ~2 minutes
```

That's it! 🎉
