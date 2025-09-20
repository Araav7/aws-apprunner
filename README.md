# Simple Python App with Datadog APM

A minimal Python Flask app that automatically sends traces to Datadog APM using `ddtrace-run`.

## Quick Deploy to AWS App Runner

### 1. Build and Push to ECR

```bash
# Set your AWS account ID and region
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=ap-southeast-1

# Create ECR repository (if needed)
aws ecr create-repository --repository-name simple-trace-app --region $AWS_REGION 2>/dev/null || true

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build and push
docker build -t simple-trace-app .
docker tag simple-trace-app:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/simple-trace-app:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/simple-trace-app:latest
```

### 2. Create App Runner Service

In AWS Console:
1. Go to **App Runner** → **Create service**
2. Select **Container registry** → **Amazon ECR**
3. Choose your image: `simple-trace-app:latest`
4. Set Port: `8080`

### 3. Set Environment Variables

In App Runner configuration, add:

```
DD_TRACE_AGENT_URL = http://8htnpdqdkp.ap-southeast-1.awsapprunner.com:8126
DD_SERVICE = simple-trace-app
DD_ENV = production
DD_TRACE_ENABLED = true
```

### 4. Deploy

Click **Create & deploy** and wait for "Running" status.

## Testing

```bash
# Test health check
curl https://YOUR-APP-URL.ap-southeast-1.awsapprunner.com/health

# Test main endpoint (creates trace)
curl https://YOUR-APP-URL.ap-southeast-1.awsapprunner.com/
```

## View Traces

Go to Datadog → APM → Services → Look for `simple-trace-app`

## Files

- `app.py` - Simple Flask app (26 lines)
- `requirements.txt` - Dependencies
- `Dockerfile` - Uses ddtrace-run with Gunicorn

## Troubleshooting

If health checks fail:
1. Check CloudWatch logs for errors
2. Verify PORT is set to 8080
3. Ensure Docker image was pushed correctly
4. Redeploy the service in App Runner# aws-apprunner
