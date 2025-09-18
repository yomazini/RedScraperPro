# Troubleshooting Guide for RedScraperPro

## Common Issues and Solutions

### Installation Issues

#### Issue: Python Not Found
```
Error: 'python' is not recognized as an internal or external command
```

**Solutions:**
1. **Install Python 3.8+**
   - Download from: https://python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Use python3 instead of python**
   ```bash
   python3 src/main.py
   ```

3. **Manually add Python to PATH**
   - Windows: Add Python installation directory to System PATH
   - Linux/macOS: Add to ~/.bashrc or ~/.zshrc

#### Issue: Permission Denied (Linux/macOS)
```
bash: ./install.sh: Permission denied
```

**Solution:**
```bash
chmod +x install.sh
./install.sh
```

#### Issue: Module Import Errors
```
ModuleNotFoundError: No module named 'praw'
```

**Solutions:**
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Use virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. **Upgrade pip**
   ```bash
   pip install --upgrade pip
   ```

### Reddit API Issues

#### Issue: Invalid Client ID
```
prawcore.exceptions.ResponseException: received 401 HTTP response
```

**Solutions:**
1. **Verify Client ID**
   - Go to https://www.reddit.com/prefs/apps
   - Client ID is the string under your app name (not the secret)
   - Copy exactly without extra spaces

2. **Check App Type**
   - Ensure you selected "script" when creating the app
   - Personal use scripts require "script" type

3. **Recreate App**
   - Delete and recreate your Reddit app if needed

#### Issue: Rate Limiting
```
prawcore.exceptions.TooManyRequests: received 429 HTTP response
```

**Solutions:**
1. **Increase delay between requests**
   ```bash
   # Edit config/config.yaml
   scraping:
     rate_limit_delay: 2.0  # Increase from 1.0 to 2.0 seconds
   ```

2. **Reduce request frequency**
   - Use smaller limits per session
   - Wait longer between scraping sessions

3. **Check API usage**
   - Reddit allows 60 requests per minute
   - Monitor your usage patterns

#### Issue: Invalid User Agent
```
prawcore.exceptions.ResponseException: received 429 HTTP response
```

**Solutions:**
1. **Use descriptive User Agent**
   ```
   Format: AppName:Version (by /u/YourUsername)
   Example: RedScraperPro:v1.0.0 (by /u/yomazini)
   ```

2. **Avoid generic User Agents**
   - Don't use browser user agents
   - Don't use generic strings like "bot" or "scraper"

3. **Update User Agent**
   ```bash
   python src/main.py --setup
   # Enter new User Agent when prompted
   ```

### Configuration Issues

#### Issue: Configuration Not Found
```
Error loading config: [Errno 2] No such file or directory: 'config/config.yaml'
```

**Solutions:**
1. **Run setup wizard**
   ```bash
   python src/main.py --setup
   ```

2. **Create config directory**
   ```bash
   mkdir -p config
   python src/main.py --setup
   ```

3. **Check file permissions**
   ```bash
   ls -la config/
   chmod 644 config/config.yaml
   ```

#### Issue: Invalid Configuration Format
```
Error loading config: while parsing a block mapping
```

**Solutions:**
1. **Check YAML syntax**
   - Ensure proper indentation (spaces, not tabs)
   - Check for missing colons or quotes

2. **Reset configuration**
   ```bash
   rm config/config.yaml
   python src/main.py --setup
   ```

3. **Use configuration template**
   ```yaml
   reddit:
     client_id: "your_client_id"
     client_secret: "your_client_secret"
     user_agent: "RedScraperPro:v1.0.0 (by /u/yourusername)"
   ```

### Scraping Issues

#### Issue: No Data Scraped
```
❌ No data was scraped.
```

**Solutions:**
1. **Check search terms**
   - Use more common keywords
   - Try different subreddit names
   - Verify user/post IDs exist

2. **Increase limits**
   ```bash
   python src/main.py --mode keyword --query "test" --limit 100
   ```

3. **Check subreddit accessibility**
   - Some subreddits may be private
   - Some users may have deleted accounts

4. **Verify API credentials**
   ```bash
   python src/main.py --mode keyword --query "reddit" --limit 5
   ```

#### Issue: Incomplete Data
```
Some posts/comments missing expected fields
```

**Solutions:**
1. **Check Reddit API changes**
   - Reddit occasionally updates their API
   - Some fields may be deprecated

2. **Handle deleted content**
   - Deleted posts/comments return limited data
   - This is normal behavior

3. **Update PRAW version**
   ```bash
   pip install --upgrade praw
   ```

### Export Issues

#### Issue: Export Failed
```
❌ Export failed: [Errno 13] Permission denied
```

**Solutions:**
1. **Check directory permissions**
   ```bash
   mkdir -p exports
   chmod 755 exports
   ```

2. **Close open files**
   - Close Excel/CSV files if they're open
   - Some programs lock files during editing

3. **Check disk space**
   ```bash
   df -h  # Linux/macOS
   # Check available disk space
   ```

#### Issue: Corrupted Export Files
```
File appears corrupted or unreadable
```

**Solutions:**
1. **Try different export format**
   ```bash
   python src/main.py --mode keyword --query "test" --export json
   ```

2. **Check file size**
   - Very large datasets may cause issues
   - Try smaller limits or split data

3. **Verify data integrity**
   ```bash
   python -c "import json; json.load(open('exports/file.json'))"
   ```

### Performance Issues

#### Issue: Slow Scraping
```
Scraping takes very long time
```

**Solutions:**
1. **Reduce comment depth**
   ```bash
   python src/main.py --mode post --post-id "abc123" --depth 1
   ```

2. **Skip comments for large datasets**
   ```bash
   python src/main.py --mode subreddit --target "news" --limit 1000
   # Don't use --include-comments for large datasets
   ```

3. **Use smaller batches**
   ```bash
   # Instead of --limit 1000, use multiple smaller requests
   python src/main.py --mode keyword --query "test" --limit 100
   ```

#### Issue: High Memory Usage
```
System runs out of memory during scraping
```

**Solutions:**
1. **Reduce batch size**
   ```bash
   python src/main.py --mode subreddit --target "programming" --limit 50
   ```

2. **Disable sentiment analysis for large datasets**
   ```bash
   # Remove --sentiment flag for memory efficiency
   python src/main.py --mode keyword --query "test" --limit 500
   ```

3. **Export frequently**
   - Process data in smaller chunks
   - Export and clear memory between batches

### Network Issues

#### Issue: Connection Timeout
```
requests.exceptions.ConnectTimeout: HTTPSConnectionPool
```

**Solutions:**
1. **Check internet connection**
   ```bash
   ping reddit.com
   ```

2. **Increase timeout**
   ```yaml
   # In config/config.yaml
   scraping:
     timeout: 60  # Increase from 30 to 60 seconds
   ```

3. **Retry failed requests**
   ```yaml
   scraping:
     max_retries: 5  # Increase retry attempts
   ```

#### Issue: SSL Certificate Errors
```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**Solutions:**
1. **Update certificates**
   ```bash
   pip install --upgrade certifi
   ```

2. **Update Python**
   - Use Python 3.8+ for better SSL support

3. **Check system time**
   - Ensure system clock is accurate

### Platform-Specific Issues

#### Windows Issues

**Issue: Script won't run**
```
'python' is not recognized
```

**Solutions:**
1. **Use full path**
   ```cmd
   C:\Python39\python.exe src/main.py
   ```

2. **Use Python Launcher**
   ```cmd
   py src/main.py
   ```

3. **Install from Microsoft Store**
   - Search "Python" in Microsoft Store
   - Install Python 3.9+

**Issue: Path issues**
```
FileNotFoundError: [Errno 2] No such file or directory
```

**Solutions:**
1. **Use forward slashes**
   ```bash
   python src/main.py  # Not src\main.py
   ```

2. **Use Git Bash or WSL**
   - Better compatibility with Unix-style paths

#### macOS Issues

**Issue: Command Line Tools missing**
```
xcrun: error: invalid active developer path
```

**Solutions:**
1. **Install Xcode Command Line Tools**
   ```bash
   xcode-select --install
   ```

2. **Use Homebrew for Python**
   ```bash
   brew install python
   ```

#### Linux Issues

**Issue: Missing development headers**
```
error: Microsoft Visual C++ 14.0 is required
```

**Solutions:**
1. **Install build tools**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-dev build-essential
   
   # CentOS/RHEL
   sudo yum install python3-devel gcc
   ```

2. **Install specific packages**
   ```bash
   sudo apt-get install libffi-dev libssl-dev
   ```

## Debugging Steps

### 1. Enable Verbose Logging
```bash
python src/main.py --verbose --mode keyword --query "debug" --limit 5
```

### 2. Check Log Files
```bash
# View recent logs
tail -f logs/redscraperpro_*.log

# Search for errors
grep -i "error" logs/redscraperpro_*.log

# Check configuration loading
grep -i "config" logs/redscraperpro_*.log
```

### 3. Test Basic Functionality
```bash
# Test configuration
python src/main.py --setup

# Test simple scraping
python src/main.py --mode keyword --query "test" --limit 1

# Test export
python src/main.py --mode keyword --query "test" --limit 1 --export json
```

### 4. Verify Dependencies
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(praw|rich|pandas|requests)"

# Test imports
python -c "import praw, rich, pandas; print('All imports successful')"
```

### 5. Test Reddit API Connection
```python
# test_connection.py
import praw

reddit = praw.Reddit(
    client_id="your_client_id",
    client_secret="your_client_secret",
    user_agent="test_script"
)

try:
    # Test read-only access
    subreddit = reddit.subreddit("test")
    for post in subreddit.hot(limit=1):
        print(f"✅ Connection successful: {post.title}")
        break
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

## Getting Help

### Before Seeking Help

1. **Check this troubleshooting guide**
2. **Review error messages carefully**
3. **Check log files for details**
4. **Try basic debugging steps**
5. **Search existing GitHub issues**

### When Reporting Issues

Include the following information:

1. **System Information**
   ```bash
   python --version
   pip --version
   uname -a  # Linux/macOS
   # or
   systeminfo  # Windows
   ```

2. **Error Messages**
   - Full error traceback
   - Relevant log entries
   - Command that caused the error

3. **Configuration**
   - Sanitized config file (remove credentials)
   - Command line arguments used
   - Environment variables (if any)

4. **Steps to Reproduce**
   - Exact commands run
   - Expected vs actual behavior
   - Any workarounds attempted

### Support Channels

1. **GitHub Issues**: https://github.com/yomazini/RedScraperPro/issues
2. **Documentation**: https://github.com/yomazini/RedScraperPro/blob/master/RedScraperPro/DOCUMENTATION.md
3. **LinkedIn**: https://linkedin.com/in/youssef-mazini

### Community Resources

1. **r/redditdev**: Reddit's developer community
2. **PRAW Documentation**: https://praw.readthedocs.io/
3. **Stack Overflow**: Tag questions with `praw` and `reddit-api`

---

**Remember**: Most issues are related to configuration or API credentials. Double-check your Reddit API setup before diving into complex troubleshooting.
