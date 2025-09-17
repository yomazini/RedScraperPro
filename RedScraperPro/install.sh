#!/bin/bash

# RedScraperPro Installation Script
# Horror/Itachi Theme Installation

# Colors for output
RED='\033[0;31m'
DARK_RED='\033[1;31m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# ASCII Art Header
echo -e "${DARK_RED}"
cat << "EOF"
██████╗ ███████╗██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ ██████╗ ██████╗  ██████╗ 
██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔═══██╗
██████╔╝█████╗  ██║  ██║███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝██████╔╝██████╔╝██║   ██║
██╔══██╗██╔══╝  ██║  ██║╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗██╔═══╝ ██╔══██╗██║   ██║
██║  ██║███████╗██████╔╝███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║██║     ██║  ██║╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
EOF
echo -e "${NC}"

echo -e "${WHITE}🩸 The Ultimate Reddit Scraping CLI Tool 🩸${NC}"
echo -e "${GRAY}\"In the darkness of data, we find the light of knowledge\"${NC}"
echo ""

# Detect OS
echo -e "${RED}🔍 Detecting your system...${NC}"
OS="Unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS="Windows"
fi

echo -e "${WHITE}📱 Platform detected: ${OS}${NC}"
echo ""

# Check Python version
echo -e "${RED}🐍 Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
else
    echo -e "${DARK_RED}❌ Python not found! Please install Python 3.8 or higher.${NC}"
    exit 1
fi

echo -e "${WHITE}✅ Python found: ${PYTHON_VERSION}${NC}"

# Check Python version compatibility
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${DARK_RED}❌ Python 3.8 or higher is required. Found: ${PYTHON_VERSION}${NC}"
    exit 1
fi

echo -e "${WHITE}✅ Python version compatible${NC}"
echo ""

# Check pip
echo -e "${RED}📦 Checking pip installation...${NC}"
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo -e "${DARK_RED}❌ pip not found! Please install pip.${NC}"
    exit 1
fi

echo -e "${WHITE}✅ pip found${NC}"
echo ""

# Create virtual environment (optional but recommended)
echo -e "${RED}🏗️  Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${GRAY}Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv venv
    
    if [ $? -eq 0 ]; then
        echo -e "${WHITE}✅ Virtual environment created${NC}"
    else
        echo -e "${DARK_RED}❌ Failed to create virtual environment${NC}"
        echo -e "${GRAY}Continuing with system Python...${NC}"
    fi
else
    echo -e "${WHITE}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo -e "${GRAY}Activating virtual environment...${NC}"
    if [[ "$OS" == "Windows" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    echo -e "${WHITE}✅ Virtual environment activated${NC}"
fi

echo ""

# Install dependencies
echo -e "${RED}📚 Installing dependencies...${NC}"
echo -e "${GRAY}This may take a few minutes...${NC}"

$PIP_CMD install --upgrade pip
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${WHITE}✅ All dependencies installed successfully${NC}"
else
    echo -e "${DARK_RED}❌ Failed to install some dependencies${NC}"
    echo -e "${GRAY}Please check the error messages above${NC}"
    exit 1
fi

echo ""

# Create necessary directories
echo -e "${RED}📁 Creating project directories...${NC}"
mkdir -p logs
mkdir -p exports
mkdir -p config

echo -e "${WHITE}✅ Project directories created${NC}"
echo ""

# Installation complete
echo -e "${DARK_RED}"
cat << "EOF"
🩸 INSTALLATION COMPLETE 🩸
EOF
echo -e "${NC}"

echo -e "${WHITE}🎯 Next Steps:${NC}"
echo -e "${GRAY}1. Get your Reddit API credentials:${NC}"
echo -e "${GRAY}   https://github.com/yomazini/RedScraperPro/blob/master/fullRedscrapperprohowtouse.pdf${NC}"
echo ""
echo -e "${GRAY}2. Run the configuration wizard:${NC}"
echo -e "${WHITE}   $PYTHON_CMD src/main.py --setup${NC}"
echo ""
echo -e "${GRAY}3. Start scraping:${NC}"
echo -e "${WHITE}   $PYTHON_CMD src/main.py${NC}"
echo ""

# Display a random quote
echo -e "${RED}💭 Wisdom for your journey:${NC}"
QUOTES=(
    "\"The only true wisdom is in knowing you know nothing.\" - Socrates"
    "\"In the midst of winter, I found there was, within me, an invincible summer.\" - Albert Camus"
    "\"Someone has to die in order that the rest of us should value life more.\" - Virginia Woolf"
    "\"The truth will set you free, but first it will piss you off.\" - Gloria Steinem"
    "\"Those who can make you believe absurdities can make you commit atrocities.\" - Voltaire"
)

RANDOM_QUOTE=${QUOTES[$RANDOM % ${#QUOTES[@]}]}
echo -e "${GRAY}${RANDOM_QUOTE}${NC}"
echo ""

echo -e "${WHITE}Happy scraping! 🕷️${NC}"
