"""
TXT Exporter for RedScraperPro
🩸 Export scraped data to text format 🩸
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..utils.config import Config
from ..utils.logger import Logger


class TXTExporter:
    """Handles TXT export functionality"""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.output_dir = config.get_output_directory()
    
    def export(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data to formatted text file"""
        if not data:
            raise ValueError("No data to export")
        
        # Ensure filename has .txt extension
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as txtfile:
                # Write header
                self._write_header(txtfile, data)
                
                # Separate posts and comments
                posts = [item for item in data if item.get('type') == 'post']
                comments = [item for item in data if item.get('type') == 'comment']
                
                # Write posts section
                if posts:
                    self._write_posts_section(txtfile, posts)
                
                # Write comments section
                if comments:
                    self._write_comments_section(txtfile, comments)
                
                # Write footer with statistics
                self._write_footer(txtfile, data, posts, comments)
            
            self.logger.export_complete(str(filepath), len(data))
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"TXT export failed: {str(e)}")
            raise
    
    def export_readable(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data in human-readable format"""
        if not data:
            raise ValueError("No data to export")
        
        # Ensure filename has .txt extension
        if not filename.endswith('.txt'):
            filename += '_readable.txt'
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as txtfile:
                # Write title
                txtfile.write("🩸 REDSCRAPERPRO DATA EXPORT 🩸\n")
                txtfile.write("=" * 80 + "\n\n")
                
                # Write export info
                txtfile.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                txtfile.write(f"Total Items: {len(data)}\n")
                txtfile.write(f"Posts: {len([item for item in data if item.get('type') == 'post'])}\n")
                txtfile.write(f"Comments: {len([item for item in data if item.get('type') == 'comment'])}\n\n")
                
                # Write data in readable format
                for i, item in enumerate(data, 1):
                    txtfile.write(f"[{i}] ")
                    
                    if item.get('type') == 'post':
                        self._write_readable_post(txtfile, item)
                    elif item.get('type') == 'comment':
                        self._write_readable_comment(txtfile, item)
                    
                    txtfile.write("\n" + "-" * 80 + "\n\n")
            
            self.logger.export_complete(str(filepath), len(data))
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Readable TXT export failed: {str(e)}")
            raise
    
    def export_posts_only(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export only posts to text format"""
        posts_data = [item for item in data if item.get('type') == 'post']
        
        if not filename.endswith('.txt'):
            filename += '_posts.txt'
        
        return self.export(posts_data, filename)
    
    def export_comments_only(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export only comments to text format"""
        comments_data = [item for item in data if item.get('type') == 'comment']
        
        if not filename.endswith('.txt'):
            filename += '_comments.txt'
        
        return self.export(comments_data, filename)
    
    def export_summary_only(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export only summary statistics to text format"""
        if not data:
            raise ValueError("No data to export")
        
        # Ensure filename has .txt extension
        if not filename.endswith('.txt'):
            filename += '_summary.txt'
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as txtfile:
                # Write header
                txtfile.write("🩸 REDSCRAPERPRO SUMMARY REPORT 🩸\n")
                txtfile.write("=" * 80 + "\n\n")
                
                # Write summary statistics
                self._write_summary_statistics(txtfile, data)
            
            self.logger.export_complete(str(filepath), len(data))
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Summary TXT export failed: {str(e)}")
            raise
    
    def _write_header(self, txtfile, data: List[Dict[str, Any]]):
        """Write file header"""
        txtfile.write("🩸 REDSCRAPERPRO DATA EXPORT 🩸\n")
        txtfile.write("=" * 80 + "\n")
        txtfile.write("\"In the darkness of data, we find the light of knowledge\"\n")
        txtfile.write("=" * 80 + "\n\n")
        
        # Export metadata
        txtfile.write("EXPORT INFORMATION:\n")
        txtfile.write("-" * 20 + "\n")
        txtfile.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        txtfile.write(f"Total Items: {len(data)}\n")
        txtfile.write(f"Posts: {len([item for item in data if item.get('type') == 'post'])}\n")
        txtfile.write(f"Comments: {len([item for item in data if item.get('type') == 'comment'])}\n")
        txtfile.write(f"Scraper Version: 1.0.0\n\n")
    
    def _write_posts_section(self, txtfile, posts: List[Dict[str, Any]]):
        """Write posts section"""
        txtfile.write("📝 POSTS SECTION\n")
        txtfile.write("=" * 80 + "\n\n")
        
        for i, post in enumerate(posts, 1):
            txtfile.write(f"POST #{i}\n")
            txtfile.write("-" * 10 + "\n")
            txtfile.write(f"ID: {post.get('id', 'N/A')}\n")
            txtfile.write(f"Title: {post.get('title', 'N/A')}\n")
            txtfile.write(f"Author: {post.get('author', 'N/A')}\n")
            txtfile.write(f"Subreddit: r/{post.get('subreddit', 'N/A')}\n")
            txtfile.write(f"Score: {post.get('score', 'N/A')}\n")
            txtfile.write(f"Comments: {post.get('num_comments', 'N/A')}\n")
            txtfile.write(f"Created: {post.get('created_datetime', 'N/A')}\n")
            txtfile.write(f"URL: {post.get('url', 'N/A')}\n")
            
            # Post content
            if post.get('selftext'):
                txtfile.write(f"Content:\n{post.get('selftext')}\n")
            
            txtfile.write(f"Permalink: {post.get('permalink', 'N/A')}\n")
            txtfile.write("\n" + "~" * 40 + "\n\n")
    
    def _write_comments_section(self, txtfile, comments: List[Dict[str, Any]]):
        """Write comments section"""
        txtfile.write("💬 COMMENTS SECTION\n")
        txtfile.write("=" * 80 + "\n\n")
        
        for i, comment in enumerate(comments, 1):
            txtfile.write(f"COMMENT #{i}\n")
            txtfile.write("-" * 12 + "\n")
            txtfile.write(f"ID: {comment.get('id', 'N/A')}\n")
            txtfile.write(f"Author: {comment.get('author', 'N/A')}\n")
            txtfile.write(f"Subreddit: r/{comment.get('subreddit', 'N/A')}\n")
            txtfile.write(f"Score: {comment.get('score', 'N/A')}\n")
            txtfile.write(f"Depth: {comment.get('depth', 'N/A')}\n")
            txtfile.write(f"Created: {comment.get('created_datetime', 'N/A')}\n")
            txtfile.write(f"Is Reply: {comment.get('is_reply', 'N/A')}\n")
            
            # Comment body
            if comment.get('body'):
                txtfile.write(f"Content:\n{comment.get('body')}\n")
            
            txtfile.write(f"Permalink: {comment.get('permalink', 'N/A')}\n")
            txtfile.write("\n" + "~" * 40 + "\n\n")
    
    def _write_footer(self, txtfile, data: List[Dict[str, Any]], posts: List[Dict[str, Any]], comments: List[Dict[str, Any]]):
        """Write file footer with statistics"""
        txtfile.write("📊 STATISTICS\n")
        txtfile.write("=" * 80 + "\n\n")
        
        # Overall statistics
        txtfile.write("OVERALL STATISTICS:\n")
        txtfile.write("-" * 20 + "\n")
        txtfile.write(f"Total Items: {len(data)}\n")
        txtfile.write(f"Total Posts: {len(posts)}\n")
        txtfile.write(f"Total Comments: {len(comments)}\n")
        txtfile.write(f"Total Score: {sum(item.get('score', 0) for item in data)}\n")
        txtfile.write(f"Average Score: {sum(item.get('score', 0) for item in data) / len(data):.2f}\n\n")
        
        # Subreddit breakdown
        subreddit_counts = {}
        for item in data:
            subreddit = item.get('subreddit', 'unknown')
            subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1
        
        if subreddit_counts:
            txtfile.write("TOP SUBREDDITS:\n")
            txtfile.write("-" * 15 + "\n")
            sorted_subreddits = sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for subreddit, count in sorted_subreddits:
                txtfile.write(f"r/{subreddit}: {count} items\n")
            txtfile.write("\n")
        
        # Author breakdown
        author_counts = {}
        for item in data:
            author = item.get('author', 'unknown')
            author_counts[author] = author_counts.get(author, 0) + 1
        
        if author_counts:
            txtfile.write("TOP AUTHORS:\n")
            txtfile.write("-" * 12 + "\n")
            sorted_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for author, count in sorted_authors:
                txtfile.write(f"u/{author}: {count} items\n")
            txtfile.write("\n")
        
        # Footer
        txtfile.write("=" * 80 + "\n")
        txtfile.write("Generated by RedScraperPro - The Ultimate Reddit Scraping Tool\n")
        txtfile.write("GitHub: https://github.com/yomazini/RedScraperPro\n")
        txtfile.write("\"Those who cannot acknowledge themselves will eventually fail.\" - Itachi Uchiha\n")
        txtfile.write("=" * 80 + "\n")
    
    def _write_readable_post(self, txtfile, post: Dict[str, Any]):
        """Write a post in readable format"""
        txtfile.write(f"📝 POST: {post.get('title', 'Untitled')}\n")
        txtfile.write(f"   Author: u/{post.get('author', 'unknown')} in r/{post.get('subreddit', 'unknown')}\n")
        txtfile.write(f"   Score: {post.get('score', 0)} | Comments: {post.get('num_comments', 0)}\n")
        txtfile.write(f"   Created: {post.get('created_datetime', 'unknown')}\n")
        
        if post.get('selftext'):
            txtfile.write(f"   Content: {post.get('selftext')[:200]}{'...' if len(post.get('selftext', '')) > 200 else ''}\n")
        
        txtfile.write(f"   URL: {post.get('url', 'N/A')}\n")
    
    def _write_readable_comment(self, txtfile, comment: Dict[str, Any]):
        """Write a comment in readable format"""
        txtfile.write(f"💬 COMMENT by u/{comment.get('author', 'unknown')} in r/{comment.get('subreddit', 'unknown')}\n")
        txtfile.write(f"   Score: {comment.get('score', 0)} | Depth: {comment.get('depth', 0)}\n")
        txtfile.write(f"   Created: {comment.get('created_datetime', 'unknown')}\n")
        
        if comment.get('body'):
            body = comment.get('body', '')
            txtfile.write(f"   Content: {body[:300]}{'...' if len(body) > 300 else ''}\n")
    
    def _write_summary_statistics(self, txtfile, data: List[Dict[str, Any]]):
        """Write comprehensive summary statistics"""
        posts = [item for item in data if item.get('type') == 'post']
        comments = [item for item in data if item.get('type') == 'comment']
        
        # Basic statistics
        txtfile.write("BASIC STATISTICS:\n")
        txtfile.write("-" * 17 + "\n")
        txtfile.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        txtfile.write(f"Total Items: {len(data)}\n")
        txtfile.write(f"Posts: {len(posts)}\n")
        txtfile.write(f"Comments: {len(comments)}\n\n")
        
        # Score statistics
        if data:
            scores = [item.get('score', 0) for item in data]
            txtfile.write("SCORE STATISTICS:\n")
            txtfile.write("-" * 17 + "\n")
            txtfile.write(f"Total Score: {sum(scores)}\n")
            txtfile.write(f"Average Score: {sum(scores) / len(scores):.2f}\n")
            txtfile.write(f"Highest Score: {max(scores)}\n")
            txtfile.write(f"Lowest Score: {min(scores)}\n\n")
        
        # Subreddit analysis
        subreddit_stats = {}
        for item in data:
            subreddit = item.get('subreddit', 'unknown')
            if subreddit not in subreddit_stats:
                subreddit_stats[subreddit] = {'posts': 0, 'comments': 0, 'total_score': 0}
            
            if item.get('type') == 'post':
                subreddit_stats[subreddit]['posts'] += 1
            elif item.get('type') == 'comment':
                subreddit_stats[subreddit]['comments'] += 1
            
            subreddit_stats[subreddit]['total_score'] += item.get('score', 0)
        
        txtfile.write("SUBREDDIT BREAKDOWN:\n")
        txtfile.write("-" * 20 + "\n")
        sorted_subreddits = sorted(subreddit_stats.items(), key=lambda x: x[1]['posts'] + x[1]['comments'], reverse=True)
        for subreddit, stats in sorted_subreddits[:15]:
            total_items = stats['posts'] + stats['comments']
            txtfile.write(f"r/{subreddit}: {total_items} items (Posts: {stats['posts']}, Comments: {stats['comments']}, Score: {stats['total_score']})\n")
        
        txtfile.write("\n")
        
        # Author analysis
        author_stats = {}
        for item in data:
            author = item.get('author', 'unknown')
            if author not in author_stats:
                author_stats[author] = {'posts': 0, 'comments': 0, 'total_score': 0}
            
            if item.get('type') == 'post':
                author_stats[author]['posts'] += 1
            elif item.get('type') == 'comment':
                author_stats[author]['comments'] += 1
            
            author_stats[author]['total_score'] += item.get('score', 0)
        
        txtfile.write("TOP AUTHORS:\n")
        txtfile.write("-" * 12 + "\n")
        sorted_authors = sorted(author_stats.items(), key=lambda x: x[1]['posts'] + x[1]['comments'], reverse=True)
        for author, stats in sorted_authors[:15]:
            total_items = stats['posts'] + stats['comments']
            txtfile.write(f"u/{author}: {total_items} items (Posts: {stats['posts']}, Comments: {stats['comments']}, Score: {stats['total_score']})\n")
        
        txtfile.write("\n")
        txtfile.write("=" * 80 + "\n")
        txtfile.write("End of Summary Report\n")
        txtfile.write("Generated by RedScraperPro v1.0.0\n")
        txtfile.write("=" * 80 + "\n")
