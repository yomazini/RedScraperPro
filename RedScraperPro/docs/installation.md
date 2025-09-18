# Installation Guide for RedScraperPro

## Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Memory**: At least 4GB RAM recommended
- **Storage**: 500MB free space for installation and data

### Required Software
1. **Python 3.8+**
   - Download from: https://python.org/downloads/
   - Ensure `pip` is included in the installation
   - Add Python to your system PATH

2. **Git** (Optional but recommended)
   - Download from: https://git-scm.com/downloads
   - Required for cloning the repository

## Installation Methods

### Method 1: Quick Install (Recommended)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yomazini/RedScraperPro.git
   cd RedScraperPro
   ```

2. **Run Installation Script**
   ```bash
   # On Linux/macOS
   chmod +x install.sh
   ./install.sh
   
   # On Windows (use Git Bash or WSL)
   bash install.sh
   ```

3. **Follow the Installation Wizard**
   - The script will automatically detect your system
   - Install Python dependencies
   - Create necessary directories
   - Guide you through initial setup

### Method 2: Manual Installation

1. **Clone or Download**
   ```bash
   git clone https://github.com/yomazini/RedScraperPro.git
   cd RedScraperPro
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Linux/macOS:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Create Directories**
   ```bash
   mkdir -p logs exports config
   ```

5. **Run Configuration**
   ```bash
   python src/main.py --setup
   ```

### Method 3: Development Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/yomazini/RedScraperPro.git
   cd RedScraperPro
   ```

2. **Install in Development Mode**
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt  # If available
   ```

3. **Run Tests** (Optional)
   ```bash
   python -m pytest tests/
   ```

## Reddit API Setup

### Getting Reddit API Credentials

1. **Create Reddit Account**
   - Go to https://reddit.com and create an account if you don't have one

2. **Create Reddit App**
   - Visit: https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Fill in the form:
     - **Name**: RedScraperPro (or any name you prefer)
     - **App type**: Select "script"
     - **Description**: Reddit scraping tool for educational purposes
     - **About URL**: Leave blank
     - **Redirect URI**: http://localhost:8080 (required but not used)

3. **Note Your Credentials**
   - **Client ID**: Found under the app name (looks like: `abc123def456`)
   - **Client Secret**: The "secret" field value
   - **User Agent**: Use format: `RedScraperPro:v1.0.0 (by /u/yourusername)`

### Configuration

1. **Run Configuration Wizard**
   ```bash
   python src/main.py --setup
   ```

2. **Enter Your Credentials**
   - Follow the prompts to enter your Reddit API credentials
   - Configure scraping preferences
   - Set export options

3. **Test Connection** (Optional)
   - The wizard will offer to test your API connection
   - This ensures your credentials are working correctly

## Verification

### Test Installation
```bash
# Check if RedScraperPro runs
python src/main.py --version

# Run a quick test
python src/main.py --mode keyword --query "test" --limit 5
```

### Expected Output
- ASCII art header should display
- No import errors
- Configuration wizard should run smoothly
- Test scraping should work (if API is configured)

## Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Error: 'python' is not recognized
# Solution: Use python3 or add Python to PATH
python3 src/main.py
```

#### Permission Denied (Linux/macOS)
```bash
# Error: Permission denied
# Solution: Make script executable
chmod +x install.sh
```

#### Module Import Errors
```bash
# Error: ModuleNotFoundError
# Solution: Install dependencies
pip install -r requirements.txt
```

#### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove and recreate
rm -rf venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Platform-Specific Issues

#### Windows
- Use Git Bash or Windows Subsystem for Linux (WSL) for best compatibility
- Ensure Python is added to PATH during installation
- Use `python` instead of `python3` in commands

#### macOS
- Install Xcode Command Line Tools: `xcode-select --install`
- Use Homebrew for Python installation: `brew install python`
- May need to use `python3` and `pip3` explicitly

#### Linux
- Install Python development headers: `sudo apt-get install python3-dev`
- Install pip if not available: `sudo apt-get install python3-pip`
- Ensure you have build tools: `sudo apt-get install build-essential`

## Next Steps

After successful installation:

1. **Read the Documentation**
   - Check `docs/usage-examples.md` for usage examples
   - Review `docs/praw-setup.md` for detailed API setup

2. **Start Scraping**
   ```bash
   # Interactive mode
   python src/main.py
   
   # Command line mode
   python src/main.py --mode keyword --query "python programming"
   ```

3. **Explore Features**
   - Try different scraping modes
   - Experiment with export formats
   - Configure advanced settings

## Support

If you encounter issues:

1. **Check the logs**: Look in the `logs/` directory for error details
2. **Review configuration**: Run `python src/main.py --setup` to reconfigure
3. **Update dependencies**: Run `pip install --upgrade -r requirements.txt`
4. **Seek help**: 
   - GitHub Issues: https://github.com/yomazini/RedScraperPro/issues
   - Documentation: https://github.com/yomazini/RedScraperPro/blob/master/RedScraperPro/DOCUMENTATION.md

---

**Remember**: Always use RedScraperPro responsibly and in compliance with Reddit's Terms of Service and API guidelines.
