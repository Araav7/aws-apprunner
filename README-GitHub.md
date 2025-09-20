# Deploy to AWS App Runner from GitHub

Complete guide for deploying this Python app to AWS App Runner using GitHub as source.

## Prerequisites

- GitHub account
- AWS account with App Runner access
- Datadog agent already running (at `http://8htnpdqdkp.ap-southeast-1.awsapprunner.com:8126`)

## Step 1: Push Code to GitHub

### Option A: Create New Repository

1. **Create a new GitHub repository:**
   - Go to [GitHub](https://github.com/new)
   - Name it: `simple-trace-app` (or any name you prefer)
   - Keep it Public or Private (both work)
   - Don't initialize with README (you already have one)

2. **Push your code:**
   ```bash
   cd /Users/araavind.senthil/hello-world-aws
   
   # Initialize git (if not already)
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Simple Python app with Datadog APM"
   
   # Add your GitHub repo as remote (replace with your repo URL)
   git remote add origin https://github.com/YOUR_USERNAME/simple-trace-app.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

### Option B: Fork/Use Existing Repository

If you already have the code in a repo, skip to Step 2.

## Step 2: Create App Runner Service from GitHub

1. **Go to AWS App Runner Console:**
   - Navigate to [AWS App Runner](https://console.aws.amazon.com/apprunner)
   - Click **"Create service"**

2. **Choose Source:**
   - Select **"Source code repository"**
   - Click **"Add New"** to connect GitHub

3. **Connect GitHub Account:**
   - Click **"Install another"**
   - You'll be redirected to GitHub
   - Select your repository or "All repositories"
   - Click **"Install"**
   - Return to AWS Console

4. **Configure Source:**
   - **Connection name:** `github-connection` (or any name)
   - **Repository:** Select your repo from dropdown
   - **Branch:** `main` (or your default branch)
   - **Source directory:** `/` (root)
   - Click **"Next"**

5. **Configure Deployment:**
   - **Deployment trigger:** Choose one:
     - **Automatic** - Redeploys on every push (recommended)
     - **Manual** - Deploy only when you trigger

## Step 3: Configure Build Settings

Since we have `apprunner.yaml`, App Runner will use it automatically.

1. **Configuration source:**
   - Select **"Use a configuration file"**
   - App Runner will detect `apprunner.yaml`

2. Click **"Next"**

## Step 4: Configure Service

1. **Service settings:**
   - **Service name:** `simple-trace-app-github`
   - **CPU:** `0.25 vCPU`
   - **Memory:** `0.5 GB`
   - **Environment variables:** (Optional - already in apprunner.yaml)
     - You can override here if needed:
     ```
     DD_TRACE_AGENT_URL = http://8htnpdqdkp.ap-southeast-1.awsapprunner.com:8126
     DD_SERVICE = simple-trace-app
     DD_ENV = production
     ```

2. **Auto scaling:**
   - Leave defaults (Min: 1, Max: 25)

3. **Health check:**
   - **Path:** `/health`
   - **Protocol:** `HTTP`
   - **Interval:** `10 seconds`
   - **Timeout:** `5 seconds`
   - **Threshold:** `1 unhealthy, 5 healthy`

4. **Security:**
   - Leave defaults (public access)

5. **Tags:** (Optional)
   - Add any tags for organization

6. Click **"Next"**

## Step 5: Review and Create

1. Review all settings
2. Click **"Create & deploy"**
3. Wait for deployment (5-10 minutes for first deployment)

## Step 6: Monitor Deployment

1. **Check Status:**
   - Status should progress: `Operation in progress` → `Running`
   - If it fails, check "Activity" tab for errors

2. **View Logs:**
   - Click on "Logs" tab
   - Select "Application logs" to see your app output

3. **Get Your App URL:**
   - Once running, you'll see the **Default domain**
   - Example: `https://xxxxxxxxxx.ap-southeast-1.awsapprunner.com`

## Step 7: Test Your Application

```bash
# Replace with your actual App Runner URL
APP_URL="https://xxxxxxxxxx.ap-southeast-1.awsapprunner.com"

# Test health endpoint
curl $APP_URL/health

# Expected output:
# {"status":"healthy","timestamp":"2024-..."}

# Test main endpoint (creates trace)
curl $APP_URL/

# Expected output:
# {"message":"Hello from AWS App Runner!","service":"simple-trace-app","timestamp":"2024-..."}
```

## Step 8: View Traces in Datadog

1. Go to [Datadog APM](https://app.datadoghq.com/apm/services)
2. Look for service: `simple-trace-app`
3. Click to see traces, latency, and metrics

## Updating Your App

### With Automatic Deployment:
```bash
# Make changes to your code
git add .
git commit -m "Update message"
git push

# App Runner automatically redeploys!
```

### With Manual Deployment:
1. Push changes to GitHub
2. Go to App Runner console
3. Click **"Deploy"** button

## File Structure Required

Your GitHub repository must have:
```
simple-trace-app/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── apprunner.yaml      # App Runner configuration
└── README.md          # Documentation
```

## Troubleshooting

### Build Fails
- Check `apprunner.yaml` syntax
- Verify `requirements.txt` has all dependencies
- Check CloudWatch logs for Python errors

### Health Check Fails
- Ensure `/health` endpoint returns 200 status
- Check PORT is 8080
- Verify Gunicorn is starting correctly

### No Traces in Datadog
- Verify `DD_TRACE_AGENT_URL` is correct
- Check Datadog agent is running and accessible
- Ensure `DD_TRACE_ENABLED=true`

### Connection to GitHub Fails
- Revoke and reconnect GitHub app
- Check repository permissions
- Ensure branch name is correct

## Cost Optimization

- **Minimum instances:** Set to 0 for dev environments
- **Maximum instances:** Limit based on expected traffic
- **Instance size:** Start with 0.25 vCPU for simple apps

## Advantages of GitHub Deployment

✅ **No Docker needed** - App Runner builds for you  
✅ **Automatic deployments** - Push to deploy  
✅ **Version control** - Full Git history  
✅ **Rollback capability** - Easy to revert  
✅ **Simpler workflow** - No ECR management  

## Next Steps

1. **Set up branch protection** for production
2. **Add GitHub Actions** for testing
3. **Configure custom domain** in App Runner
4. **Set up Datadog monitors** for alerts

---

That's it! Your app is now deployed from GitHub to AWS App Runner with automatic Datadog APM tracing.
