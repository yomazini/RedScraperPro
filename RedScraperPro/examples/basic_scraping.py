"""
Basic Reddit Scraping Examples for RedScraperPro
🩸 Simple usage examples to get you started 🩸
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.config import Config
from utils.logger import Logger
from utils.progress import ProgressTracker
from scraper.reddit_scraper import RedditScraper


def example_keyword_scraping():
    """Example: Scrape posts by keyword"""
    print("🔍 Example: Keyword Scraping")
    print("-" * 40)
    
    # Initialize components
    config = Config()
    logger = Logger(verbose=True)
    progress_tracker = ProgressTracker()
    
    # Create scraper
    scraper = RedditScraper(config, logger, progress_tracker)
    
    # Scrape by keyword
    results = scraper.scrape_by_keyword(
        query="python programming",
        limit=10,
        include_comments=True,
        comment_depth=1
    )
    
    # Export results
    if results:
        exported_file = scraper.export_data(results, "csv", "keyword_example")
        print(f"✅ Data exported to: {exported_file}")
    else:
        print("❌ No data scraped")


def example_subreddit_scraping():
    """Example: Scrape posts from a subreddit"""
    print("🏘️  Example: Subreddit Scraping")
    print("-" * 40)
    
    # Initialize components
    config = Config()
    logger = Logger(verbose=True)
    progress_tracker = ProgressTracker()
    
    # Create scraper
    scraper = RedditScraper(config, logger, progress_tracker)
    
    # Scrape subreddit
    results = scraper.scrape_subreddit(
        subreddit_name="programming",
        limit=15,
        include_comments=False,
        sort_method="hot"
    )
    
    # Export results
    if results:
        exported_file = scraper.export_data(results, "json", "subreddit_example")
        print(f"✅ Data exported to: {exported_file}")
    else:
        print("❌ No data scraped")


def example_user_scraping():
    """Example: Scrape user's posts and comments"""
    print("👤 Example: User Scraping")
    print("-" * 40)
    
    # Initialize components
    config = Config()
    logger = Logger(verbose=True)
    progress_tracker = ProgressTracker()
    
    # Create scraper
    scraper = RedditScraper(config, logger, progress_tracker)
    
    # Scrape user (replace with actual username)
    username = "spez"  # Reddit CEO - public profile
    
    results = scraper.scrape_user(
        username=username,
        limit=10,
        include_comments=True,
        content_type="both"
    )
    
    # Export results
    if results:
        exported_file = scraper.export_data(results, "xlsx", f"user_{username}_example")
        print(f"✅ Data exported to: {exported_file}")
    else:
        print("❌ No data scraped")


def example_post_scraping():
    """Example: Scrape a specific post and its comments"""
    print("📝 Example: Specific Post Scraping")
    print("-" * 40)
    
    # Initialize components
    config = Config()
    logger = Logger(verbose=True)
    progress_tracker = ProgressTracker()
    
    # Create scraper
    scraper = RedditScraper(config, logger, progress_tracker)
    
    # Example post ID (this is a famous Reddit post)
    post_id = "5gn8ru"  # "What tastes better than it smells?" post
    
    results = scraper.scrape_post(
        post_id=post_id,
        include_comments=True,
        comment_depth=2
    )
    
    # Export results
    if results:
        exported_file = scraper.export_data(results, "txt", f"post_{post_id}_example")
        print(f"✅ Data exported to: {exported_file}")
    else:
        print("❌ No data scraped")


def example_with_sentiment_analysis():
    """Example: Scraping with sentiment analysis"""
    print("🧠 Example: Scraping with Sentiment Analysis")
    print("-" * 40)
    
    # Initialize components
    config = Config()
    logger = Logger(verbose=True)
    progress_tracker = ProgressTracker()
    
    # Create scraper
    scraper = RedditScraper(config, logger, progress_tracker)
    
    # Scrape data
    results = scraper.scrape_by_keyword(
        query="artificial intelligence",
        limit=20,
        include_comments=False
    )
    
    # Add sentiment analysis
    if results:
        results_with_sentiment = scraper.add_sentiment_analysis(results)
        
        # Export results
        exported_file = scraper.export_data(results_with_sentiment, "json", "sentiment_example")
        print(f"✅ Data with sentiment analysis exported to: {exported_file}")
    else:
        print("❌ No data scraped")


def example_multiple_formats():
    """Example: Export the same data in multiple formats"""
    print("📊 Example: Multiple Export Formats")
    print("-" * 40)
    
    # Initialize components
    config = Config()
    logger = Logger(verbose=True)
    progress_tracker = ProgressTracker()
    
    # Create scraper
    scraper = RedditScraper(config, logger, progress_tracker)
    
    # Scrape data
    results = scraper.scrape_subreddit(
        subreddit_name="technology",
        limit=25,
        include_comments=True,
        comment_depth=1
    )
    
    if results:
        # Export in multiple formats
        formats = ["csv", "json", "xlsx", "txt"]
        
        for format_type in formats:
            try:
                exported_file = scraper.export_data(results, format_type, f"multi_format_example")
                print(f"✅ {format_type.upper()} exported to: {exported_file}")
            except Exception as e:
                print(f"❌ Failed to export {format_type.upper()}: {str(e)}")
    else:
        print("❌ No data scraped")


def main():
    """Run all examples"""
    print("🩸 RedScraperPro Basic Examples 🩸")
    print("=" * 50)
    print("\"In the darkness of data, we find the light of knowledge\"")
    print("=" * 50)
    print()
    
    examples = [
        ("Keyword Scraping", example_keyword_scraping),
        ("Subreddit Scraping", example_subreddit_scraping),
        ("User Scraping", example_user_scraping),
        ("Post Scraping", example_post_scraping),
        ("Sentiment Analysis", example_with_sentiment_analysis),
        ("Multiple Formats", example_multiple_formats),
    ]
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n[{i}/{len(examples)}] Running: {name}")
        print("=" * 50)
        
        try:
            func()
        except Exception as e:
            print(f"❌ Example failed: {str(e)}")
            print("💡 Make sure you have configured your Reddit API credentials!")
            print("   Run: python src/main.py --setup")
        
        print("\n" + "~" * 50)
        
        # Ask user if they want to continue
        if i < len(examples):
            try:
                input("\nPress Enter to continue to the next example (Ctrl+C to exit)...")
            except KeyboardInterrupt:
                print("\n\n🩸 Examples interrupted by user. Goodbye!")
                break
    
    print("\n🎯 All examples completed!")
    print("💭 \"Those who cannot acknowledge themselves will eventually fail.\" - Itachi Uchiha")


if __name__ == "__main__":
    main()
