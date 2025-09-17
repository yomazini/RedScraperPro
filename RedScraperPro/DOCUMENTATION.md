# 🩸 RedScraperPro Documentation 🩸

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [API Reference](#api-reference)
6. [Export Formats](#export-formats)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [Contributing](#contributing)

---

## Overview

RedScraperPro is the ultimate Reddit scraping CLI tool featuring a unique Horror/Itachi Uchiha aesthetic. Built with Python and designed for educational purposes, it provides comprehensive Reddit data extraction with multiple output formats.

### Key Features
- **Multiple Scraping Modes**: Keyword, Subreddit, User, Post
- **Beautiful Interface**: Horror/Itachi themed ASCII art and quotes
- **Export Formats**: CSV, XLSX, JSON, TXT
- **Sentiment Analysis**: Optional lightweight analysis
- **Cross-Platform**: Windows, macOS, Linux support
- **Resume Functionality**: Continue interrupted operations

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection
- Reddit account for API access

### Quick Install
```bash
git clone https://github.com/yomazini/RedScraperPro.git
cd RedScraperPro
chmod +x install.sh
./install.sh
```

### Manual Install
```bash
git clone https://github.com/yomazini/RedScraperPro.git
cd RedScraperPro
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Verify Installation
```bash
python src/main.py --version
```

---

## Configuration

### Initial Setup
Run the configuration wizard:
```bash
python src/main.py --setup
```

### Reddit API Setup
1. **Create Reddit App**:
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" → Select "script"
   - Note your Client ID and Client Secret

2. **Configure Credentials**:
   - Client ID: String under app name
   - Client Secret: The "secret" field
   - User Agent: `RedScraperPro:v1.0.0 (by /u/yourusername)`

### Configuration File
Location: `config/config.yaml`
```yaml
reddit:
  client_id: "your_client_id"
  client_secret: "your_client_secret"
  user_agent: "RedScraperPro:v1.0.0 (by /u/yourusername)"
scraping:
  default_limit: 100
  default_depth: 1
  include_comments: true
export:
  default_format: "csv"
  output_directory: "exports"
```

---

## Usage

### Interactive Mode
```bash
python src/main.py
```
Displays beautiful ASCII art menu with numbered options (1, 2, 3...).

### Command Line Mode

#### Keyword Scraping
```bash
python src/main.py --mode keyword --query "python programming" --limit 100
```

#### Subreddit Scraping
```bash
python src/main.py --mode subreddit --target "programming" --limit 50
```

#### User Scraping
```bash
python src/main.py --mode user --target "username" --limit 25
```

#### Post Scraping
```bash
python src/main.py --mode post --post-id "abc123" --include-comments --depth 2
```

### Advanced Options
```bash
# With sentiment analysis
python src/main.py --mode keyword --query "AI" --sentiment --export json

# Custom output filename
python src/main.py --mode subreddit --target "technology" --output "tech_posts"

# Resume interrupted session
python src/main.py --resume "session_file.json"

# Verbose logging
python src/main.py --verbose --mode keyword --query "debug"
```

---

## API Reference

### Core Classes

#### RedditScraper
Main scraping class with methods for different scraping modes.

```python
from scraper.reddit_scraper import RedditScraper

scraper = RedditScraper(config, logger, progress_tracker)

# Scrape by keyword
results = scraper.scrape_by_keyword(
    query="python programming",
    limit=100,
    include_comments=True,
    comment_depth=2
)

# Scrape subreddit
results = scraper.scrape_subreddit(
    subreddit_name="programming",
    limit=50,
    sort_method="hot"
)

# Scrape user
results = scraper.scrape_user(
    username="spez",
    limit=25,
    content_type="both"
)

# Scrape specific post
results = scraper.scrape_post(
    post_id="abc123",
    include_comments=True,
    comment_depth=3
)
```

#### Exporters
Export data to various formats.

```python
from exporters import CSVExporter, XLSXExporter, JSONExporter, TXTExporter

# CSV Export
csv_exporter = CSVExporter(config, logger)
csv_file = csv_exporter.export(data, "output_file")

# Excel Export with multiple sheets
xlsx_exporter = XLSXExporter(config, logger)
xlsx_file = xlsx_exporter.export(data, "output_file")

# JSON Export with metadata
json_exporter = JSONExporter(config, logger)
json_file = json_exporter.export(data, "output_file")

# Text Export for reading
txt_exporter = TXTExporter(config, logger)
txt_file = txt_exporter.export(data, "output_file")
```

### Configuration Management

```python
from utils.config import Config

config = Config()

# Update Reddit settings
config.update_reddit_config(
    client_id="new_id",
    client_secret="new_secret"
)

# Update scraping preferences
config.update_scraping_config(
    default_limit=200,
    enable_sentiment=True
)

# Save configuration
config.save()
```

---

## Export Formats

### CSV Format
- Flattened data structure
- All fields as columns
- Nested data converted to strings
- Perfect for spreadsheet analysis

**Example Output:**
```csv
type,id,title,author,subreddit,score,created_datetime
post,abc123,Example Post,user123,programming,150,2024-01-15T10:30:00
```

### XLSX Format
- Multiple sheets: Posts, Comments, Summary, Statistics
- Professional formatting with colors
- Auto-adjusted column widths
- Charts and statistics

**Sheets:**
- **Posts**: All post data
- **Comments**: All comment data  
- **Summary**: Overview statistics
- **Statistics**: Detailed analytics

### JSON Format
- Structured data with metadata
- Nested objects preserved
- API-ready format
- Multiple organization options

**Example Structure:**
```json
{
  "metadata": {
    "export_timestamp": "2024-01-15T10:30:00",
    "total_items": 150,
    "scraper_version": "1.0.0"
  },
  "data": [...]
}
```

### TXT Format
- Human-readable format
- Summary statistics
- Formatted posts and comments
- Perfect for reading and analysis

---

## Advanced Features

### Sentiment Analysis
Optional lightweight sentiment analysis using TextBlob and VADER.

```bash
# Enable sentiment analysis
python src/main.py --mode keyword --query "climate change" --sentiment
```

**Output includes:**
- Polarity score (-1 to 1)
- Subjectivity score (0 to 1)
- Emotion scores (positive, negative, neutral)
- Combined classification with confidence

### Progress Tracking
Real-time progress display with themed elements:
- 🩸 Blood drops for progress indicators
- 📊 Statistics and ETA calculations
- 🌙 Moon symbols for completion
- Session resumption capability

### Resume Functionality
Continue interrupted scraping sessions:

```bash
# Scraping automatically saves progress
python src/main.py --mode subreddit --target "news" --limit 1000

# If interrupted, resume with:
python src/main.py --resume "logs/session_20240115_103000.json"
```

### Duplicate Removal
Automatic duplicate detection and removal:
- Based on post/comment IDs
- Configurable in settings
- Statistics tracking

### Rate Limiting
Respects Reddit's API limits:
- Configurable delays between requests
- Automatic retry on rate limit errors
- Warning notifications

---

## Troubleshooting

### Common Issues

#### Installation Problems
```bash
# Python not found
python3 src/main.py  # Use python3 instead of python

# Permission denied (Linux/macOS)
chmod +x install.sh

# Module import errors
pip install -r requirements.txt
```

#### API Issues
```bash
# Invalid credentials
python src/main.py --setup  # Reconfigure

# Rate limiting
# Increase delay in config/config.yaml:
scraping:
  rate_limit_delay: 2.0  # Increase from 1.0
```

#### Export Problems
```bash
# Permission denied
mkdir -p exports
chmod 755 exports

# Corrupted files
# Try different format:
python src/main.py --mode keyword --query "test" --export json
```

### Debug Mode
```bash
# Enable verbose logging
python src/main.py --verbose --mode keyword --query "debug" --limit 5

# Check log files
tail -f logs/redscraperpro_*.log
```

### Getting Help
1. Check log files in `logs/` directory
2. Review configuration in `config/config.yaml`
3. Test with small limits first
4. Verify Reddit API credentials

---

## Best Practices

### Ethical Usage
- **Educational Purpose**: Use for learning and research only
- **Respect Rate Limits**: Don't overwhelm Reddit's servers
- **Follow ToS**: Comply with Reddit's Terms of Service
- **Privacy**: Respect user privacy and community guidelines

### Performance Optimization
- **Reasonable Limits**: Start with small limits (10-50 items)
- **Rate Limiting**: Use appropriate delays between requests
- **Batch Processing**: Process large datasets in smaller chunks
- **Memory Management**: Export frequently for large datasets

### Data Management
- **Organize Output**: Use descriptive filenames and directories
- **Backup Configuration**: Save your config files
- **Version Control**: Track your scraping scripts (not credentials)
- **Data Validation**: Verify exported data integrity

### Security
- **Protect Credentials**: Never commit API keys to version control
- **Use Environment Variables**: For sensitive configuration
- **Regular Updates**: Keep dependencies updated
- **Monitor Usage**: Track your API usage patterns

---

## Contributing

### Development Setup
```bash
git clone https://github.com/yomazini/RedScraperPro.git
cd RedScraperPro
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

### Running Tests
```bash
python tests/test_basic.py
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Maintain the Horror/Itachi aesthetic theme

### Submitting Issues
Include:
- System information (OS, Python version)
- Full error messages and tracebacks
- Steps to reproduce the issue
- Configuration details (sanitized)

### Feature Requests
- Describe the use case clearly
- Explain how it fits the educational purpose
- Consider the Horror/Itachi theme integration
- Provide implementation suggestions if possible

---

## License and Legal

### MIT License
This project is licensed under the MIT License. See `LICENSE` file for details.

### Educational Purpose
This tool is designed for educational purposes, research, and legitimate data analysis only.

### Disclaimer
Users are responsible for ensuring their use complies with:
- Reddit's Terms of Service
- Local laws and regulations
- Data protection requirements
- Ethical guidelines

### Third-Party Licenses
This software uses several third-party libraries with their own licenses:
- PRAW (BSD 2-Clause)
- Rich (MIT)
- Pandas (BSD 3-Clause)
- And others (see requirements.txt)

---

## Support

### Documentation
- **Installation Guide**: `docs/installation.md`
- **PRAW Setup**: `docs/praw-setup.md`
- **Youtube Video Tutorial**: `link soon`
- **Usage Examples**: `docs/usage-examples.md`
- **Troubleshooting**: `docs/troubleshooting.md`

### Community
- **GitHub Issues**: https://github.com/yomazini/RedScraperPro/issues
- **LinkedIn**: https://linkedin.com/in/yomazini
- **Reddit**: r/redditdev for general Reddit API questions

### Resources
- **PRAW Documentation**: https://praw.readthedocs.io/
- **Reddit API**: https://www.reddit.com/dev/api/
- **Python Documentation**: https://docs.python.org/

---

**🩸 "Those who cannot acknowledge themselves will eventually fail." - Itachi Uchiha 🩸**

*RedScraperPro acknowledges itself as the ultimate Reddit scraping tool, and therefore, it will never fail.*
