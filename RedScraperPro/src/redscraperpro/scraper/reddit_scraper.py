"""
Main Reddit Scraper for RedScraperPro
🩸 Core scraping functionality with PRAW integration 🩸
"""

import time
import praw
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from pathlib import Path

from redscraperpro.utils.config import Config
from redscraperpro.utils.logger import Logger
from redscraperpro.utils.progress import ProgressTracker
from redscraperpro.exporters.csv_exporter import CSVExporter
from redscraperpro.exporters.json_exporter import JSONExporter
from redscraperpro.exporters.txt_exporter import TXTExporter
from redscraperpro.exporters.xlsx_exporter import XLSXExporter
from redscraperpro.scraper.post_scraper import PostScraper
from redscraperpro.scraper.comment_scraper import CommentScraper
from redscraperpro.scraper.user_scraper import UserScraper


class RedditScraper:
    """Main Reddit scraping class"""
    
    def __init__(self, config: Config, logger: Logger, progress_tracker: ProgressTracker):
        self.config = config
        self.logger = logger
        self.progress_tracker = progress_tracker
        
        # Initialize Reddit instance
        self.reddit = self._initialize_reddit()
        
        # Initialize specialized scrapers
        self.post_scraper = PostScraper(self.reddit, logger, progress_tracker)
        self.comment_scraper = CommentScraper(self.reddit, logger, progress_tracker)
        self.user_scraper = UserScraper(self.reddit, logger, progress_tracker)
        
        # Initialize exporters
        self.exporters = {
            'csv': CSVExporter(config, logger),
            'xlsx': XLSXExporter(config, logger),
            'json': JSONExporter(config, logger),
            'txt': TXTExporter(config, logger)
        }
    
    def _initialize_reddit(self) -> praw.Reddit:
        """Initialize Reddit instance with configuration"""
        try:
            reddit_config = self.config.get_reddit_config_dict()
            reddit = praw.Reddit(**reddit_config)
            
            # Test the connection
            reddit.user.me()  # This will raise an exception if credentials are invalid
            
            self.logger.success("Reddit API connection established")
            return reddit
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Reddit connection: {str(e)}")
            raise Exception(f"Reddit API initialization failed: {str(e)}")
    
    def scrape_by_keyword(self, query: str, limit: int = 100, include_comments: bool = True, 
                         comment_depth: int = 1, sentiment_analysis: bool = False) -> List[Dict[str, Any]]:
        """Scrape Reddit posts by keyword search"""
        self.logger.scraping_start("keyword", query, limit)
        self.progress_tracker.start_session("keyword", query, limit)
        
        try:
            results = []
            
            # Search across all subreddits
            search_results = self.reddit.subreddit("all").search(
                query, 
                limit=limit,
                sort="relevance",
                time_filter="all"
            )
            
            for post in search_results:
                try:
                    # Scrape post data
                    post_data = self.post_scraper.scrape_post(post)
                    results.append(post_data)
                    
                    # Scrape comments if requested
                    if include_comments:
                        comments = self.comment_scraper.scrape_post_comments(
                            post, 
                            depth=comment_depth
                        )
                        results.extend(comments)
                    
                    # Update progress
                    self.progress_tracker.increment_posts()
                    
                    # Rate limiting
                    time.sleep(self.config.scraping.rate_limit_delay)
                    
                except Exception as e:
                    self.logger.error(f"Error scraping post {post.id}: {str(e)}")
                    self.progress_tracker.increment_errors()
                    continue
            
            self.progress_tracker.finish_session()
            self.logger.scraping_complete(self.progress_tracker.get_stats())
            
            return results
            
        except Exception as e:
            self.logger.error(f"Keyword scraping failed: {str(e)}")
            raise
    
    def scrape_subreddit(self, subreddit_name: str, limit: int = 100, include_comments: bool = True,
                        comment_depth: int = 1, sort_method: str = "hot") -> List[Dict[str, Any]]:
        """Scrape posts from a specific subreddit"""
        self.logger.scraping_start("subreddit", subreddit_name, limit)
        self.progress_tracker.start_session("subreddit", subreddit_name, limit)
        
        try:
            results = []
            
            # Get subreddit
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get posts based on sort method
            if sort_method == "hot":
                posts = subreddit.hot(limit=limit)
            elif sort_method == "new":
                posts = subreddit.new(limit=limit)
            elif sort_method == "top":
                posts = subreddit.top(limit=limit, time_filter="all")
            elif sort_method == "rising":
                posts = subreddit.rising(limit=limit)
            else:
                posts = subreddit.hot(limit=limit)
            
            for post in posts:
                try:
                    # Scrape post data
                    post_data = self.post_scraper.scrape_post(post)
                    results.append(post_data)
                    
                    # Scrape comments if requested
                    if include_comments:
                        comments = self.comment_scraper.scrape_post_comments(
                            post, 
                            depth=comment_depth
                        )
                        results.extend(comments)
                    
                    # Update progress
                    self.progress_tracker.increment_posts()
                    
                    # Rate limiting
                    time.sleep(self.config.scraping.rate_limit_delay)
                    
                except Exception as e:
                    self.logger.error(f"Error scraping post {post.id}: {str(e)}")
                    self.progress_tracker.increment_errors()
                    continue
            
            self.progress_tracker.finish_session()
            self.logger.scraping_complete(self.progress_tracker.get_stats())
            
            return results
            
        except Exception as e:
            self.logger.error(f"Subreddit scraping failed: {str(e)}")
            raise
    
    def scrape_user(self, username: str, limit: int = 100, include_comments: bool = True,
                   content_type: str = "submissions") -> List[Dict[str, Any]]:
        """Scrape posts/comments from a specific user"""
        self.logger.scraping_start("user", username, limit)
        self.progress_tracker.start_session("user", username, limit)
        
        try:
            results = []
            
            # Get user
            user = self.reddit.redditor(username)
            
            # Scrape user submissions
            if content_type in ["submissions", "both"]:
                submissions = user.submissions.new(limit=limit)
                for post in submissions:
                    try:
                        post_data = self.post_scraper.scrape_post(post)
                        results.append(post_data)
                        
                        # Update progress
                        self.progress_tracker.increment_posts()
                        
                        # Rate limiting
                        time.sleep(self.config.scraping.rate_limit_delay)
                        
                    except Exception as e:
                        self.logger.error(f"Error scraping user post {post.id}: {str(e)}")
                        self.progress_tracker.increment_errors()
                        continue
            
            # Scrape user comments
            if content_type in ["comments", "both"] or include_comments:
                comments = user.comments.new(limit=limit)
                for comment in comments:
                    try:
                        comment_data = self.comment_scraper.scrape_comment(comment)
                        results.append(comment_data)
                        
                        # Update progress
                        self.progress_tracker.increment_comments()
                        
                        # Rate limiting
                        time.sleep(self.config.scraping.rate_limit_delay)
                        
                    except Exception as e:
                        self.logger.error(f"Error scraping user comment {comment.id}: {str(e)}")
                        self.progress_tracker.increment_errors()
                        continue
            
            self.progress_tracker.finish_session()
            self.logger.scraping_complete(self.progress_tracker.get_stats())
            
            return results
            
        except Exception as e:
            self.logger.error(f"User scraping failed: {str(e)}")
            raise
    
    def scrape_post(self, post_id: str, include_comments: bool = True, 
                   comment_depth: int = 1) -> List[Dict[str, Any]]:
        """Scrape a specific post and its comments"""
        self.logger.scraping_start("post", post_id, 1)
        self.progress_tracker.start_session("post", post_id, 1)
        
        try:
            results = []
            
            # Get post
            post = self.reddit.submission(id=post_id)
            
            # Scrape post data
            post_data = self.post_scraper.scrape_post(post)
            results.append(post_data)
            self.progress_tracker.increment_posts()
            
            # Scrape comments if requested
            if include_comments:
                comments = self.comment_scraper.scrape_post_comments(
                    post, 
                    depth=comment_depth
                )
                results.extend(comments)
            
            self.progress_tracker.finish_session()
            self.logger.scraping_complete(self.progress_tracker.get_stats())
            
            return results
            
        except Exception as e:
            self.logger.error(f"Post scraping failed: {str(e)}")
            raise
    
    def add_sentiment_analysis(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add sentiment analysis to scraped data"""
        try:
            from textblob import TextBlob
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            
            analyzer = SentimentIntensityAnalyzer()
            
            self.logger.info("Starting sentiment analysis...")
            
            for i, item in enumerate(data):
                try:
                    # Get text content
                    text = item.get('content', '') or item.get('body', '') or item.get('title', '')
                    
                    if text and len(text.strip()) > 0:
                        # TextBlob analysis
                        blob = TextBlob(text)
                        textblob_polarity = blob.sentiment.polarity
                        textblob_subjectivity = blob.sentiment.subjectivity
                        
                        # VADER analysis
                        vader_scores = analyzer.polarity_scores(text)
                        
                        # Add sentiment data
                        item['sentiment'] = {
                            'textblob_polarity': textblob_polarity,
                            'textblob_subjectivity': textblob_subjectivity,
                            'vader_positive': vader_scores['pos'],
                            'vader_negative': vader_scores['neg'],
                            'vader_neutral': vader_scores['neu'],
                            'vader_compound': vader_scores['compound']
                        }
                    else:
                        item['sentiment'] = None
                    
                    # Log progress
                    if i % 10 == 0:
                        self.logger.sentiment_analysis(i + 1, len(data))
                        
                except Exception as e:
                    self.logger.error(f"Sentiment analysis error for item {i}: {str(e)}")
                    item['sentiment'] = None
                    continue
            
            self.logger.success(f"Sentiment analysis completed for {len(data)} items")
            return data
            
        except ImportError:
            self.logger.warning("Sentiment analysis libraries not available. Install textblob and vaderSentiment.")
            return data
        except Exception as e:
            self.logger.error(f"Sentiment analysis failed: {str(e)}")
            return data
    
    def remove_duplicates(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate entries from scraped data"""
        original_count = len(data)
        
        # Use post/comment ID as unique identifier
        seen_ids = set()
        unique_data = []
        
        for item in data:
            item_id = item.get('id', '') or item.get('post_id', '')
            if item_id and item_id not in seen_ids:
                seen_ids.add(item_id)
                unique_data.append(item)
        
        removed_count = original_count - len(unique_data)
        if removed_count > 0:
            self.logger.duplicate_removal(original_count, len(unique_data))
            self.progress_tracker.increment_duplicates(removed_count)
        
        return unique_data
    
    def export_data(self, data: List[Dict[str, Any]], format_type: str, filename: str) -> str:
        """Export scraped data to specified format"""
        if not data:
            raise ValueError("No data to export")
        
        if format_type not in self.exporters:
            raise ValueError(f"Unsupported export format: {format_type}")
        
        # Add timestamp to filename if configured
        if self.config.export.include_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}"
        
        # Export data
        exporter = self.exporters[format_type]
        exported_file = exporter.export(data, filename)
        
        self.logger.export_complete(exported_file, len(data))
        
        return exported_file
    
    def get_subreddit_info(self, subreddit_name: str) -> Dict[str, Any]:
        """Get information about a subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            return {
                'name': subreddit.display_name,
                'title': subreddit.title,
                'description': subreddit.description,
                'subscribers': subreddit.subscribers,
                'created_utc': subreddit.created_utc,
                'over18': subreddit.over18,
                'public_description': subreddit.public_description,
                'url': f"https://reddit.com/r/{subreddit.display_name}"
            }
        except Exception as e:
            self.logger.error(f"Error getting subreddit info: {str(e)}")
            return {}
    
    def get_user_info(self, username: str) -> Dict[str, Any]:
        """Get information about a user"""
        try:
            user = self.reddit.redditor(username)
            
            return {
                'name': user.name,
                'created_utc': user.created_utc,
                'comment_karma': user.comment_karma,
                'link_karma': user.link_karma,
                'is_gold': user.is_gold,
                'is_mod': user.is_mod,
                'has_verified_email': user.has_verified_email,
                'url': f"https://reddit.com/u/{user.name}"
            }
        except Exception as e:
            self.logger.error(f"Error getting user info: {str(e)}")
            return {}
    
    def test_connection(self) -> bool:
        """Test Reddit API connection"""
        try:
            # Try to access Reddit
            user = self.reddit.user.me()
            if user:
                self.logger.success(f"Connected as: {user.name}")
                return True
            else:
                # Try read-only access
                subreddit = self.reddit.subreddit("test")
                list(subreddit.hot(limit=1))
                self.logger.success("Read-only connection successful")
                return True
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False
