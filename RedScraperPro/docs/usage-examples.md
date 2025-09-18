# Usage Examples for RedScraperPro

## Quick Start

### Interactive Mode
```bash
python src/main.py
```

### Command Line Mode
```bash
# Scrape by keyword
python src/main.py --mode keyword --query "python programming" --limit 50

# Scrape subreddit
python src/main.py --mode subreddit --target "programming" --limit 25

# Scrape user posts
python src/main.py --mode user --target "spez" --limit 10

# Scrape specific post
python src/main.py --mode post --post-id "5gn8ru" --include-comments
```

## Detailed Examples

### 1. Keyword-Based Scraping

#### Basic Keyword Search
```bash
python src/main.py --mode keyword --query "artificial intelligence" --limit 100
```

#### Advanced Keyword Search with Comments
```bash
python src/main.py --mode keyword \
    --query "machine learning" \
    --limit 50 \
    --include-comments \
    --depth 2 \
    --sentiment \
    --export xlsx \
    --output "ml_discussion"
```

#### Multiple Keywords
```bash
# Search for posts containing multiple terms
python src/main.py --mode keyword --query "python OR javascript OR rust" --limit 75
```

### 2. Subreddit Scraping

#### Popular Subreddits
```bash
# Technology discussions
python src/main.py --mode subreddit --target "technology" --limit 100

# Programming community
python src/main.py --mode subreddit --target "programming" --limit 50

# Ask Reddit questions
python src/main.py --mode subreddit --target "AskReddit" --limit 25
```

#### Subreddit with Comments
```bash
python src/main.py --mode subreddit \
    --target "MachineLearning" \
    --limit 30 \
    --include-comments \
    --depth 3 \
    --export json \
    --output "ml_subreddit_deep"
```

### 3. User Profile Scraping

#### Public User Profiles
```bash
# Reddit CEO
python src/main.py --mode user --target "spez" --limit 20

# Famous users (replace with actual usernames)
python src/main.py --mode user --target "GallowBoob" --limit 15
```

#### User with Comments
```bash
python src/main.py --mode user \
    --target "username" \
    --limit 50 \
    --include-comments \
    --export csv \
    --output "user_analysis"
```

### 4. Specific Post Analysis

#### Famous Reddit Posts
```bash
# "What tastes better than it smells?" - Famous AskReddit post
python src/main.py --mode post --post-id "5gn8ru" --include-comments --depth 2

# Reddit's most upvoted post
python src/main.py --mode post --post-id "haucpf" --include-comments
```

#### Post with Deep Comment Analysis
```bash
python src/main.py --mode post \
    --post-id "your_post_id" \
    --include-comments \
    --depth 5 \
    --sentiment \
    --export xlsx \
    --output "deep_post_analysis"
```

## Export Format Examples

### CSV Export
```bash
python src/main.py --mode keyword --query "data science" --export csv --output "data_science_posts"
```

### Excel Export with Multiple Sheets
```bash
python src/main.py --mode subreddit --target "datascience" --export xlsx --output "datascience_analysis"
```

### JSON Export for API Integration
```bash
python src/main.py --mode keyword --query "API development" --export json --output "api_posts"
```

### Text Export for Reading
```bash
python src/main.py --mode subreddit --target "philosophy" --export txt --output "philosophy_discussions"
```

## Advanced Features

### Sentiment Analysis
```bash
# Enable sentiment analysis for emotional insights
python src/main.py --mode keyword \
    --query "climate change" \
    --sentiment \
    --limit 100 \
    --export json \
    --output "climate_sentiment"
```

### Duplicate Removal
```bash
# Remove duplicate posts/comments
python src/main.py --mode subreddit \
    --target "news" \
    --no-duplicates \
    --limit 200 \
    --export csv
```

### Resume Interrupted Scraping
```bash
# Resume from a saved session
python src/main.py --resume "session_20241215_143022.json"
```

## Batch Processing Examples

### Multiple Subreddits
Create a shell script to scrape multiple subreddits:

```bash
#!/bin/bash
# scrape_multiple.sh

subreddits=("programming" "MachineLearning" "datascience" "artificial" "technology")

for subreddit in "${subreddits[@]}"; do
    echo "Scraping r/$subreddit..."
    python src/main.py --mode subreddit \
        --target "$subreddit" \
        --limit 50 \
        --export csv \
        --output "${subreddit}_$(date +%Y%m%d)"
    
    echo "Waiting 30 seconds before next subreddit..."
    sleep 30
done
```

### Keyword Research
```bash
#!/bin/bash
# keyword_research.sh

keywords=("python programming" "javascript frameworks" "rust language" "go programming" "java development")

for keyword in "${keywords[@]}"; do
    echo "Researching: $keyword"
    python src/main.py --mode keyword \
        --query "$keyword" \
        --limit 25 \
        --include-comments \
        --sentiment \
        --export json \
        --output "research_$(echo $keyword | tr ' ' '_')"
    
    sleep 60  # Wait 1 minute between searches
done
```

## Configuration Examples

### Custom Configuration File
```bash
# Use custom configuration
python src/main.py --config config/research.yaml --mode keyword --query "research topic"
```

### Environment Variables
```bash
# Set environment variables for API credentials
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USER_AGENT="YourApp:v1.0.0 (by /u/yourusername)"

python src/main.py --mode keyword --query "environment test"
```

## Real-World Use Cases

### 1. Market Research
```bash
# Research product mentions
python src/main.py --mode keyword \
    --query "iPhone 15 review" \
    --limit 200 \
    --include-comments \
    --sentiment \
    --export xlsx \
    --output "iphone15_market_research"
```

### 2. Academic Research
```bash
# Collect data for academic study
python src/main.py --mode subreddit \
    --target "science" \
    --limit 500 \
    --include-comments \
    --depth 2 \
    --export json \
    --output "science_discourse_study"
```

### 3. Content Analysis
```bash
# Analyze community discussions
python src/main.py --mode keyword \
    --query "mental health support" \
    --limit 300 \
    --sentiment \
    --export csv \
    --output "mental_health_analysis"
```

### 4. Trend Analysis
```bash
# Track trending topics
python src/main.py --mode subreddit \
    --target "technology" \
    --limit 100 \
    --export json \
    --output "tech_trends_$(date +%Y%m%d)"
```

## Data Processing Pipeline

### 1. Collection
```bash
# Step 1: Collect raw data
python src/main.py --mode keyword \
    --query "artificial intelligence ethics" \
    --limit 500 \
    --include-comments \
    --export json \
    --output "ai_ethics_raw"
```

### 2. Analysis
```bash
# Step 2: Add sentiment analysis
python src/main.py --mode keyword \
    --query "artificial intelligence ethics" \
    --limit 500 \
    --include-comments \
    --sentiment \
    --export xlsx \
    --output "ai_ethics_analyzed"
```

### 3. Filtering
```bash
# Step 3: Filter high-quality content
python src/main.py --mode keyword \
    --query "artificial intelligence ethics" \
    --limit 1000 \
    --include-comments \
    --no-duplicates \
    --export csv \
    --output "ai_ethics_filtered"
```

## Performance Optimization

### Large Dataset Collection
```bash
# For large datasets, use smaller batches
python src/main.py --mode subreddit \
    --target "MachineLearning" \
    --limit 100 \
    --export json \
    --output "ml_batch_1"

# Wait and continue
sleep 300  # 5 minutes

python src/main.py --mode subreddit \
    --target "MachineLearning" \
    --limit 100 \
    --export json \
    --output "ml_batch_2"
```

### Memory-Efficient Processing
```bash
# Process without comments for memory efficiency
python src/main.py --mode subreddit \
    --target "news" \
    --limit 1000 \
    --export csv \
    --output "news_posts_only"
```

## Error Handling Examples

### Robust Scraping Script
```bash
#!/bin/bash
# robust_scraping.sh

MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo "Attempt $((RETRY_COUNT + 1)) of $MAX_RETRIES"
    
    if python src/main.py --mode keyword --query "test query" --limit 10; then
        echo "Scraping successful!"
        break
    else
        echo "Scraping failed, retrying in 60 seconds..."
        RETRY_COUNT=$((RETRY_COUNT + 1))
        sleep 60
    fi
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "Scraping failed after $MAX_RETRIES attempts"
    exit 1
fi
```

## Monitoring and Logging

### Verbose Logging
```bash
# Enable detailed logging
python src/main.py --verbose --mode keyword --query "debug test" --limit 5
```

### Quiet Mode
```bash
# Suppress non-essential output
python src/main.py --quiet --mode keyword --query "silent test" --limit 5
```

### Log Analysis
```bash
# Check recent logs
tail -f logs/redscraperpro_*.log

# Search for errors
grep -i "error" logs/redscraperpro_*.log

# Count successful operations
grep -c "success" logs/redscraperpro_*.log
```

## Integration Examples

### Python Script Integration
```python
#!/usr/bin/env python3
"""
Custom integration example
"""
import subprocess
import json
import pandas as pd

def scrape_and_analyze(query, limit=100):
    """Scrape data and perform custom analysis"""
    
    # Run RedScraperPro
    cmd = [
        "python", "src/main.py",
        "--mode", "keyword",
        "--query", query,
        "--limit", str(limit),
        "--sentiment",
        "--export", "json",
        "--output", f"analysis_{query.replace(' ', '_')}"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Scraping completed for: {query}")
        
        # Load and analyze data
        with open(f"exports/analysis_{query.replace(' ', '_')}.json", 'r') as f:
            data = json.load(f)
        
        # Custom analysis here
        posts = [item for item in data['data'] if item.get('type') == 'post']
        print(f"📊 Collected {len(posts)} posts")
        
        return data
    else:
        print(f"❌ Scraping failed for: {query}")
        print(result.stderr)
        return None

# Usage
if __name__ == "__main__":
    topics = ["machine learning", "data science", "artificial intelligence"]
    
    for topic in topics:
        scrape_and_analyze(topic, 50)
```

## Best Practices

### 1. Rate Limiting
```bash
# Always respect rate limits
python src/main.py --mode keyword --query "test" --limit 10
# Wait between large requests
sleep 60
python src/main.py --mode keyword --query "test2" --limit 10
```

### 2. Data Organization
```bash
# Organize by date
mkdir -p data/$(date +%Y/%m/%d)
python src/main.py --mode keyword --query "daily news" --output "data/$(date +%Y/%m/%d)/news"
```

### 3. Backup Important Data
```bash
# Backup configuration
cp config/config.yaml config/config_backup_$(date +%Y%m%d).yaml

# Backup exports
tar -czf exports_backup_$(date +%Y%m%d).tar.gz exports/
```

---

## Remember

- Always comply with Reddit's Terms of Service
- Use reasonable rate limits to avoid overwhelming Reddit's servers
- Respect user privacy and community guidelines
- Use the tool for educational and research purposes
- Monitor your API usage and stay within limits

For more examples and advanced usage, check the `examples/` directory in the repository.
