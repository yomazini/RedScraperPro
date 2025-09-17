# 🔴 RedScraperPro

```
██████╗ ███████╗██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ ██████╗ ██████╗  ██████╗ 
██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔═══██╗
██████╔╝█████╗  ██║  ██║███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝██████╔╝██████╔╝██║   ██║
██╔══██╗██╔══╝  ██║  ██║╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗██╔═══╝ ██╔══██╗██║   ██║
██║  ██║███████╗██████╔╝███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║██║     ██║  ██║╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
                                                                                                           
    🩸 The Ultimate Reddit Scraping CLI Tool 🩸
    "In the darkness of data, we find the light of knowledge"
```

> **⚠️ EDUCATIONAL PURPOSE ONLY**  
> This tool is designed for educational purposes, research, and legitimate data analysis only. Please ensure you comply with Reddit's Terms of Service, API guidelines, and respect rate limits. Always use this tool responsibly and ethically.

---

## 🎯 Features

### Core Scraping Capabilities
- ✅ **Posts & Comments Scraping** - Extract both posts and their comments
- ✅ **Multiple Scraping Modes**:
  - 🔍 Keyword-based scraping
  - 🏘️ Subreddit scraping
  - 👤 User profile scraping
  - 📝 Individual post scraping
- ✅ **Real-time Scraping** - Live data extraction as it happens
- ✅ **Resume Interrupted Scraping** - Continue where you left off
- ✅ **Configurable Depth Limits** - Control how deep to scrape

### Export & Data Management
- 📊 **Multiple Export Formats**: CSV, XLSX, JSON, TXT
- 🧹 **Duplicate Detection & Removal** - Clean your data automatically
- 📈 **Optional Sentiment Analysis** - Lightweight sentiment scoring
- 📋 **Comprehensive Data Fields** - Title, author, score, timestamp, awards, and more

### User Experience
- 🎨 **Beautiful ASCII Art** - Horror/Itachi Uchiha themed interface
- 📊 **Real-time Progress Tracking** - See your scraping progress live
- 🔧 **Configuration Wizard** - Easy first-time setup
- 📱 **Cross-platform** - Works on Windows, macOS, and Linux
- 🆘 **Comprehensive Help System** - Built-in documentation and examples
- 💭 **Inspirational Quotes** - Stoic, Kafka, Dostoevsky, and Itachi-themed quotes

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Reddit API credentials (PRAW)

### Installation

#### Option 1: Quick Install (Recommended)
```bash
# Clone the repository
git clone https://github.com/yomazini/RedScraperPro.git
cd RedScraperPro

# Run the installation script
chmod +x install.sh
./install.sh
```

#### Option 2: Manual Install
```bash
# Clone and setup
git clone https://github.com/yomazini/RedScraperPro.git
cd RedScraperPro

# Install dependencies
pip install -r requirements.txt

# Run the tool
python src/main.py
```

### Getting Reddit API Credentials
📖 **Detailed Guide**: [How to Get PRAW API Credentials](https://github.com/yomazini/RedScraperPro/blob/master/fullRedscrapperprohowtouse.pdf)

Quick steps:
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Note down your `client_id`, `client_secret`, and set your `user_agent`

---

## 🎮 Usage

### Interactive Mode
```bash
python src/main.py
```

### Command Line Mode
```bash
# Scrape by keyword
python src/main.py --mode keyword --query "python programming" --limit 100

# Scrape subreddit
python src/main.py --mode subreddit --target "programming" --limit 50

# Scrape user posts
python src/main.py --mode user --target "username" --limit 25

# Export to different formats
python src/main.py --mode keyword --query "AI" --export xlsx --output "ai_posts"
```

### Configuration
First run will launch the configuration wizard to set up:
- Reddit API credentials
- Default export settings
- Scraping preferences
- Output directories

---

## 📁 Project Structure

```
RedScraperPro/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── NOTICE                    # Legal notices
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── install.sh               # Installation script
├── src/
│   ├── __init__.py
│   ├── main.py              # Main CLI entry point
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── reddit_scraper.py    # Core scraping logic
│   │   ├── post_scraper.py      # Post-specific scraping
│   │   ├── comment_scraper.py   # Comment-specific scraping
│   │   └── user_scraper.py      # User-specific scraping
│   ├── exporters/
│   │   ├── __init__.py
│   │   ├── csv_exporter.py      # CSV export functionality
│   │   ├── xlsx_exporter.py     # Excel export functionality
│   │   ├── json_exporter.py     # JSON export functionality
│   │   └── txt_exporter.py      # Text export functionality
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   ├── logger.py            # Logging system
│   │   ├── ascii_art.py         # ASCII art and themes
│   │   ├── quotes.py            # Inspirational quotes system
│   │   ├── progress.py          # Progress tracking
│   │   └── sentiment.py         # Sentiment analysis
│   └── cli/
│       ├── __init__.py
│       ├── interface.py         # CLI interface
│       ├── commands.py          # CLI commands
│       └── wizard.py            # Configuration wizard
├── docs/
│   ├── installation.md         # Detailed installation guide
│   ├── praw-setup.md           # PRAW API setup guide
│   ├── usage-examples.md       # Usage examples
│   └── troubleshooting.md      # Common issues and solutions
├── tests/
│   ├── __init__.py
│   ├── test_scraper.py         # Scraper tests
│   ├── test_exporters.py       # Exporter tests
│   └── test_utils.py           # Utility tests
├── assets/
│   ├── ascii_art.txt           # ASCII art templates
│   └── quotes.json             # Inspirational quotes database
├── examples/
│   ├── basic_scraping.py       # Basic usage examples
│   ├── advanced_scraping.py    # Advanced usage examples
│   └── batch_processing.py     # Batch processing examples
└── logs/                       # Log files directory
```

---

## 🎨 Themes & Aesthetics

RedScraperPro features a unique **Horror/Itachi Uchiha** aesthetic with:
- 🔴 Red color scheme throughout the interface
- 🩸 Dark, mysterious ASCII art
- 💭 Philosophical quotes from Stoic philosophers, Kafka, Dostoevsky
- ⚡ Itachi Uchiha-inspired themes and quotes
- 🌙 Dark terminal-friendly design

---

## 📊 Data Fields Extracted

### Posts
- Title, Author, Score (upvotes/downvotes)
- Creation timestamp, URL, Flair
- Number of comments, Awards
- Subreddit, Post ID, Permalink
- Content/Selftext, Media URLs
- Optional: Sentiment score

### Comments
- Comment body, Author, Score
- Creation timestamp, Comment ID
- Parent comment ID, Depth level
- Awards, Controversiality
- Optional: Sentiment score

---

## 🔧 Configuration Options

- **API Credentials**: Reddit API setup
- **Export Settings**: Default formats and locations
- **Scraping Limits**: Posts/comments per session
- **Sentiment Analysis**: Enable/disable sentiment scoring
- **Logging Level**: Control verbosity
- **Theme Settings**: ASCII art and color preferences
- **Resume Settings**: Auto-save progress for resuming

---

## 🚨 Rate Limiting & Best Practices

- **Respect Reddit's API limits** - Tool provides warnings but doesn't enforce limits
- **Use reasonable delays** between requests
- **Monitor your API usage** through Reddit's developer dashboard
- **Be respectful** of communities and users
- **Follow Reddit's ToS** and community guidelines

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/yomazini/RedScraperPro.git
cd RedScraperPro
pip install -r requirements-dev.txt
python -m pytest tests/
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Reddit API (PRAW)** - For providing excellent API access
- **Stoic Philosophers** - For timeless wisdom
- **Franz Kafka** - For existential insights
- **Fyodor Dostoevsky** - For psychological depth
- **Itachi Uchiha** - For the aesthetic inspiration

---

## 📞 Support & Contact

- 🐛 **Issues**: [GitHub Issues](https://github.com/yomazini/RedScraperPro/issues)
- 📖 **Documentation**: [Full Guide](https://github.com/yomazini/RedScraperPro/blob/master/fullRedscrapperprohowtouse.pdf)
- 💼 **LinkedIn**: [Connect with the developer](https://linkedin.com/in/yomazini)
- 🐙 **GitHub**: [@yomazini](https://github.com/yomazini)

---

*"The truth is not always beautiful, nor beautiful words the truth." - Laozi*

*"In the world of data, we are all just shadows seeking light." - RedScraperPro Philosophy*
