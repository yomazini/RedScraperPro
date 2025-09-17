# PRAW (Python Reddit API Wrapper) Setup Guide

## Overview

PRAW is the official Python wrapper for the Reddit API. RedScraperPro uses PRAW to interact with Reddit's servers safely and efficiently.

## Step-by-Step Setup

### Step 1: Create a Reddit Account

If you don't already have a Reddit account:
1. Go to https://www.reddit.com/register
2. Create your account with a valid email address
3. Verify your email address
4. Complete your profile setup

### Step 2: Access Reddit App Preferences

1. **Log into Reddit**
2. **Navigate to App Preferences**
   - Go to: https://www.reddit.com/prefs/apps
   - Or: User Menu → User Settings → Privacy & Security → App Authorization

### Step 3: Create a New Application

1. **Click "Create App" or "Create Another App"**

2. **Fill in the Application Form**:
   - **Name**: `RedScraperPro` (or any descriptive name)
   - **App type**: Select **"script"** (this is important!)
   - **Description**: `Educational Reddit scraping tool`
   - **About URL**: Leave blank or use your GitHub profile
   - **Redirect URI**: `http://localhost:8080`
     - This is required but won't be used by RedScraperPro
     - Don't change this unless you know what you're doing

3. **Click "Create app"**

### Step 4: Collect Your Credentials

After creating the app, you'll see your application details:

```
RedScraperPro
personal use script by yourusername
[Edit] [Delete]

Client ID: abc123def456ghi789  ← This is your Client ID
Client Secret: xyz789abc123def456ghi789jkl012  ← This is your Client Secret
```

**Important Notes**:
- **Client ID**: The string of characters under your app name
- **Client Secret**: The longer string labeled "secret"
- **Keep these credentials private and secure**

### Step 5: Prepare Your User Agent

Create a descriptive User Agent string:
```
Format: AppName:Version (by /u/YourRedditUsername)
Example: RedScraperPro:v1.0.0 (by /u/yomazini)
```
or can get it from here https://51degrees.com/developers/user-agent-tester

### Step 6: Configure RedScraperPro

#### Option 1: Using the Configuration Wizard
```bash
python src/main.py --setup
```

Follow the prompts and enter:
- **Client ID**: Your app's client ID
- **Client Secret**: Your app's client secret  
- **User Agent**: Your formatted user agent string
- **Username**: Your Reddit username (optional)
- **Password**: Your Reddit password (optional)

#### Option 2: Manual Configuration
Edit `config/config.yaml`:
```yaml
reddit:
  client_id: "your_client_id_here"
  client_secret: "your_client_secret_here"
  user_agent: "RedScraperPro:v1.0.0 (by /u/yourusername)"
  username: "your_reddit_username"  # Optional
  password: "your_reddit_password"  # Optional
```

## Authentication Types

### Read-Only Access (Recommended for Scraping)
- Uses only Client ID, Client Secret, and User Agent
- Can read public posts and comments
- Cannot vote, comment, or post
- **Best for data collection and analysis**

### Authenticated Access (Optional)
- Requires username and password in addition to app credentials
- Can access private subreddits you're subscribed to
- Can perform actions like voting (not recommended for scraping)
- **Use only if you need access to private content**

## Testing Your Setup

### Test 1: Basic Connection
```bash
python src/main.py --mode keyword --query "test" --limit 1
```

### Test 2: Interactive Test
```bash
python src/main.py
# Select option 1 (Keyword Scraping)
# Enter "test" as keyword
# Set limit to 5
```

### Expected Results
- No authentication errors
- Successfully retrieves Reddit data
- Exports data to your chosen format

## Common Issues and Solutions

### Issue 1: "Invalid Client ID"
**Symptoms**: `prawcore.exceptions.ResponseException: received 401 HTTP response`

**Solutions**:
- Double-check your Client ID (it's under the app name, not the secret)
- Ensure no extra spaces or characters
- Make sure you selected "script" as app type

### Issue 2: "Invalid Client Secret"
**Symptoms**: Authentication fails with 401 error

**Solutions**:
- Verify the Client Secret is correct
- Regenerate the secret if needed (Edit app → Generate new secret)
- Check for copy-paste errors

### Issue 3: "Too Many Requests"
**Symptoms**: `prawcore.exceptions.TooManyRequests`

**Solutions**:
- Increase rate limiting delay in configuration
- Wait before retrying
- Check if you're making too many requests too quickly

### Issue 4: "User Agent Required"
**Symptoms**: `prawcore.exceptions.ResponseException: received 429 HTTP response`

**Solutions**:
- Ensure User Agent is descriptive and unique
- Follow the format: `AppName:Version (by /u/username)`
- Don't use generic user agents

## Rate Limiting Best Practices

### Reddit API Limits
- **60 requests per minute** for most endpoints
- **600 requests per 10 minutes** burst limit
- Limits reset on a rolling window

### RedScraperPro Rate Limiting
```yaml
scraping:
  rate_limit_delay: 1.0  # Seconds between requests
  max_retries: 3         # Retry failed requests
  timeout: 30           # Request timeout in seconds
```

### Recommendations
- Start with 1-2 second delays between requests
- Monitor for rate limit warnings
- Respect Reddit's servers and other users
- Use reasonable limits for data collection

## Security Best Practices

### Credential Security
- **Never share your Client Secret**
- **Don't commit credentials to version control**
- **Use environment variables for sensitive data**
- **Regenerate credentials if compromised**

### Account Security
- **Use a dedicated Reddit account for scraping**
- **Enable two-factor authentication**
- **Use strong, unique passwords**
- **Monitor account activity regularly**

## Advanced Configuration

### Environment Variables
```bash
# Set environment variables (optional)
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USER_AGENT="RedScraperPro:v1.0.0 (by /u/yourusername)"
```

### Multiple Configurations
Create different config files for different purposes:
```bash
# Research configuration
python src/main.py --config config/research.yaml

# Testing configuration  
python src/main.py --config config/testing.yaml
```

## Troubleshooting Checklist

Before seeking help, verify:

- [ ] Reddit account is created and verified
- [ ] App is created with type "script"
- [ ] Client ID and Secret are correct
- [ ] User Agent follows proper format
- [ ] No extra spaces in credentials
- [ ] Rate limiting is configured appropriately
- [ ] Internet connection is stable
- [ ] Reddit is not experiencing outages

## Getting Help

### Official Resources
- **PRAW Documentation**: https://praw.readthedocs.io/
- **Reddit API Documentation**: https://www.reddit.com/dev/api/
- **Reddit API Rules**: https://github.com/reddit-archive/reddit/wiki/API

### RedScraperPro Support
- **GitHub Issues**: https://github.com/yomazini/RedScraperPro/issues
- **Documentation**: https://github.com/yomazini/RedScraperPro/blob/master/fullRedscrapperprohowtouse.pdf
- **LinkedIn**: https://linkedin.com/in/yomazini

### Community Resources
- **r/redditdev**: Reddit's developer community
- **PRAW GitHub**: https://github.com/praw-dev/praw
- **Stack Overflow**: Tag questions with `praw` and `reddit-api`

---

**Remember**: Always comply with Reddit's Terms of Service and API guidelines. Use RedScraperPro responsibly for educational and research purposes.
