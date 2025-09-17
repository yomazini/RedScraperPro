#!/usr/bin/env python3
"""
RedScraperPro - Main Entry Point
🩸 The Ultimate Reddit Scraping CLI Tool 🩸

"Those who cannot remember the past are condemned to repeat it." - George Santayana
"""

import sys
import os
import signal
import argparse
from pathlib import Path

from redscraperpro.cli.interface import CLIInterface
from redscraperpro.cli.wizard import ConfigWizard
from redscraperpro.utils.ascii_art import ASCIIArt
from redscraperpro.utils.config import Config
from redscraperpro.utils.logger import Logger
from redscraperpro.utils.quotes import Quotes


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🩸 Interrupted by user. Saving progress...")
    print("💭 \"The only way to deal with an unfree world is to become so absolutely free that your very existence is an act of rebellion.\" - Albert Camus")
    sys.exit(0)


def main():
    """Main entry point for RedScraperPro"""
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize ASCII art and display header
    ascii_art = ASCIIArt()
    ascii_art.display_header()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="🩸 RedScraperPro - The Ultimate Reddit Scraping CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Interactive mode
  python main.py --setup                           # Run configuration wizard
  python main.py --mode keyword --query "python"   # Scrape by keyword
  python main.py --mode subreddit --target "programming" --limit 50
  python main.py --mode user --target "username" --export xlsx
  
🩸 "In the world of data, we are all just shadows seeking light." 🩸
        """
    )
    
    # Configuration arguments
    parser.add_argument("--setup", action="store_true", 
                       help="Run the configuration wizard")
    parser.add_argument("--config", type=str, 
                       help="Path to custom configuration file")
    
    # Scraping mode arguments
    parser.add_argument("--mode", choices=["keyword", "subreddit", "user", "post"], 
                       help="Scraping mode")
    parser.add_argument("--query", type=str, 
                       help="Search query (for keyword mode)")
    parser.add_argument("--target", type=str, 
                       help="Target subreddit or username")
    parser.add_argument("--post-id", type=str, 
                       help="Specific post ID to scrape")
    
    # Scraping options
    parser.add_argument("--limit", type=int, default=100, 
                       help="Maximum number of items to scrape (default: 100)")
    parser.add_argument("--depth", type=int, default=1, 
                       help="Comment depth level (default: 1)")
    parser.add_argument("--include-comments", action="store_true", 
                       help="Include comments in scraping")
    parser.add_argument("--sentiment", action="store_true", 
                       help="Enable sentiment analysis")
    
    # Export options
    parser.add_argument("--export", choices=["csv", "xlsx", "json", "txt"], 
                       default="csv", help="Export format (default: csv)")
    parser.add_argument("--output", type=str, 
                       help="Output filename (without extension)")
    parser.add_argument("--no-duplicates", action="store_true", 
                       help="Remove duplicate entries")
    
    # Utility options
    parser.add_argument("--version", action="version", version="RedScraperPro 1.0.0")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Enable verbose logging")
    parser.add_argument("--quiet", "-q", action="store_true", 
                       help="Suppress non-essential output")
    parser.add_argument("--resume", type=str, 
                       help="Resume from saved session file")
    
    args = parser.parse_args()
    
    # Initialize configuration
    config = Config(args.config)
    
    # Initialize logger
    logger = Logger(verbose=args.verbose, quiet=args.quiet)
    
    # Display a random quote
    quotes = Quotes()
    if not args.quiet:
        quotes.display_random_quote()
    
    try:
        # Run configuration wizard if requested or if first run
        if args.setup or not config.is_configured():
            wizard = ConfigWizard(config)
            wizard.run()
            return
        
        # Initialize CLI interface
        cli = CLIInterface(config, logger)
        
        # Run in command line mode if arguments provided
        if args.mode:
            cli.run_command_mode(args)
        else:
            # Run in interactive mode
            cli.run_interactive_mode()
            
    except KeyboardInterrupt:
        signal_handler(None, None)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
