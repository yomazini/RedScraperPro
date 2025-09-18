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
# Verify with any of the aliases
rsp --version
redscraperpro --version
python -m RedScraperPro.src.redscraperpro.main --version
```

---

## Configuration

### Initial Setup
Run the configuration wizard:
```bash
# Run with any of the aliases
rsp --setup
redscraperpro --setup
```

### Reddit API Setup
1. **Create Reddit App**:
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" → Select "script"
   - Note your Client ID and Client Secret

2. **Configure Credentials**:
   - Client ID: String under app name
   - Client Secret: The "secret" field
   - User Agent: A descriptive user agent, e.g., `RedScraperPro:v1.0.0 (by /u/yourusername)`. You can find your browser's user agent at [What is my User Agent?](https://51degrees.com/developers/user-agent-tester).

### Configuration File
Location: `RedScraperPro/config/config.yaml`
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
# Run with any of the aliases
rsp
redscraperpro
```
Displays a beautiful ASCII art menu with numbered options.

### Command Line Mode

#### Keyword Scraping
```bash
rsp --mode keyword --query "python programming" --limit 100
```

#### Subreddit Scraping
```bash
redscraperpro --mode subreddit --target "programming" --limit 50
```

#### User Scraping
```bash
rsp --mode user --target "username" --limit 25
```

#### Post Scraping
```bash
redscraperpro --mode post --post-id "abc123" --include-comments --depth 2
```

### Advanced Options
```bash
# With sentiment analysis
rsp --mode keyword --query "AI" --sentiment --export json

# Custom output filename
redscraperpro --mode subreddit --target "technology" --output "tech_posts"

# Resume interrupted session
rsp --resume "session_file.json"

# Verbose logging
redscraperpro --verbose --mode keyword --query "debug"
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
Optional lightweight sentiment analysis using TextBlob and VADER. For more details, see the [Sentiment Analysis Guide](./docs/sentiment_analysis.md).

```bash
# Enable sentiment analysis
rsp --mode keyword --query "climate change" --sentiment
```

**Output includes:**
- Polarity score (-1 to 1)
- Subjectivity score (0 to 1)
- VADER compound score (-1 to 1)

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
rsp --mode subreddit --target "news" --limit 1000

# If interrupted, resume with:
rsp --resume "logs/session_20240115_103000.json"
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
# Try using python3 instead of python
python3 -m RedScraperPro.src.redscraperpro.main

# Permission denied (Linux/macOS)
chmod +x install.sh

# Module import errors
pip install -r requirements.txt
```

#### API Issues
```bash
# Invalid credentials
rsp --setup  # Reconfigure

# Rate limiting
# Increase delay in RedScraperPro/config/config.yaml:
scraping:
  rate_limit_delay: 2.0  # Increase from 1.0
```

#### Export Problems
```bash
# Permission denied
mkdir -p exports
chmod 755 exports

# Corrupted files
# Try a different format:
rsp --mode keyword --query "test" --export json
```

### Debug Mode
```bash
# Enable verbose logging
rsp --verbose --mode keyword --query "debug" --limit 5

# Check log files
tail -f RedScraperPro/logs/redscraperpro_*.log
```

### Getting Help
1. Check log files in the `RedScraperPro/logs/` directory.
2. Review your configuration in `RedScraperPro/config/config.yaml`.
3. Test with small limits first (e.g., `--limit 5`).
4. Verify your Reddit API credentials are correct and have not expired.

---

## Best Practices

### Ethical Usage
- **Educational Purpose**: This tool is intended for educational and research purposes only. The author is not responsible for any misuse.
- **Respect Rate Limits**: Do not overwhelm Reddit's servers.
- **Follow ToS**: Comply with Reddit's Terms of Service.
- **Privacy**: Respect user privacy and community guidelines.

### Performance Optimization
- **Reasonable Limits**: Start with small limits (10-50 items) to test your queries.
- **Rate Limiting**: Use appropriate delays between requests to avoid being blocked.
- **Batch Processing**: For very large scraping tasks, consider running them in smaller batches.
- **Memory Management**: Export data frequently for large datasets to avoid high memory usage.

### Data Management
- **Organize Output**: Use descriptive filenames and directories for your exports.
- **Backup Configuration**: Save a backup of your `config.yaml` file.
- **Version Control**: If you modify the scripts, use version control (like Git), but be sure to exclude your credentials.
- **Data Validation**: Always check the integrity of your exported data.

### Security
- **Protect Credentials**: Never commit your API keys or secrets to version control (e.g., a public GitHub repository).
- **Use Environment Variables**: For advanced security, consider loading credentials from environment variables.
- **Regular Updates**: Keep the tool and its dependencies updated.
- **Monitor Usage**: Keep an eye on your Reddit API usage through the Reddit Apps dashboard.

---

## Contributing

### Development Setup
```bash
git clone https://github.com/yomazini/RedScraperPro.git
cd RedScraperPro
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development dependencies
```

### Running Tests
```bash
python -m pytest RedScraperPro/tests/
```

### Code Style
- Follow PEP 8 guidelines.
- Use type hints where appropriate.
- Add clear docstrings to all functions and classes.
- Maintain the Horror/Itachi aesthetic theme in user-facing elements.

### Submitting Issues
When submitting an issue, please include:
- Your operating system and Python version.
- The full error message and traceback.
- The steps required to reproduce the issue.
- Your (sanitized) configuration details.

### Feature Requests
- Clearly describe the use case and how it benefits the tool.
- Explain how the feature fits the educational purpose and theme.
- Provide implementation suggestions if possible.

---

## License and Legal

### MIT License
This project is licensed under the MIT License. See the `LICENSE` file for details.

### Educational Purpose Only
This tool is designed for educational purposes, research, and legitimate data analysis only. The author is not responsible for any misuse or any actions taken by the user that may violate Reddit's Terms of Service or any other laws.

### Disclaimer
Users are responsible for ensuring their use of RedScraperPro complies with:
- Reddit's Terms of Service
- All applicable local laws and regulations
- Data protection and privacy requirements
- Ethical research guidelines

### Third-Party Licenses
This software uses several third-party libraries, each with its own license. Key libraries include:
- PRAW (BSD 2-Clause)
- Rich (MIT)
- Pandas (BSD 3-Clause)
- See `requirements.txt` for a full list.

---

## Support

### Documentation
- **Sentiment Analysis Guide**: `docs/sentiment_analysis.md`
- **Installation Guide**: `docs/installation.md`
- **PRAW Setup**: `docs/praw-setup.md`
- **Usage Examples**: `docs/usage-examples.md`
- **Troubleshooting**: `docs/troubleshooting.md`

### Community & Contact
- **GitHub Issues**: [https://github.com/yomazini/RedScraperPro/issues](https://github.com/yomazini/RedScraperPro/issues)
- **YouTube Tutorial**: [Watch the tutorial](https://youtu.be/96-3VUxfNKc?si=yHE0wq3PGS10dpbp) (Coming Soon)
- **Author on LinkedIn**: [Youssef Mazini](https://www.linkedin.com/in/youssef-mazini/)
- **Reddit Community**: r/redditdev for general Reddit API questions

### Resources
- **PRAW Documentation**: [https://praw.readthedocs.io/](https://praw.readthedocs.io/)
- **Reddit API Wiki**: [https://www.reddit.com/dev/api/](https://www.reddit.com/dev/api/)
- **Python Documentation**: [https://docs.python.org/](https://docs.python.org/)

---

**🩸 "Those who cannot acknowledge themselves will eventually fail." - Itachi Uchiha 🩸**

*RedScraperPro acknowledges itself as the ultimate Reddit scraping tool, and therefore, it will never fail.* How?, With Your *Support*.
