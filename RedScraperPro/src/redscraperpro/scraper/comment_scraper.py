"""
Comment Scraper for RedScraperPro
🩸 Specialized Reddit comment scraping functionality 🩸
"""

import praw
from datetime import datetime
from typing import Dict, Any, List, Optional
from redscraperpro.utils.logger import Logger
from redscraperpro.utils.progress import ProgressTracker


class CommentScraper:
    """Handles Reddit comment scraping"""
    
    def __init__(self, reddit: praw.Reddit, logger: Logger, progress_tracker: ProgressTracker):
        self.reddit = reddit
        self.logger = logger
        self.progress_tracker = progress_tracker
    
    def scrape_post_comments(self, post: praw.models.Submission, depth: int = 1, 
                           limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Scrape all comments from a post"""
        try:
            comments = []
            
            # Expand all comments
            post.comments.replace_more(limit=0)
            
            # Get all comments
            all_comments = post.comments.list()
            
            if limit:
                all_comments = all_comments[:limit]
            
            for comment in all_comments:
                if isinstance(comment, praw.models.MoreComments):
                    continue
                
                # Check depth limit
                comment_depth = self._get_comment_depth(comment)
                if comment_depth <= depth:
                    comment_data = self.scrape_comment(comment, post.id)
                    if comment_data:
                        comments.append(comment_data)
                        self.progress_tracker.increment_comments()
            
            return comments
            
        except Exception as e:
            self.logger.error(f"Error scraping comments from post {post.id}: {str(e)}")
            return []
    
    def scrape_comment(self, comment: praw.models.Comment, post_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Scrape data from a single comment"""
        try:
            # Basic comment information
            comment_data = {
                'type': 'comment',
                'id': comment.id,
                'post_id': post_id or (comment.submission.id if hasattr(comment, 'submission') else ''),
                'parent_id': comment.parent_id,
                'author': str(comment.author) if comment.author else '[deleted]',
                'body': comment.body,
                'content': comment.body,  # Alias for consistency
                'created_utc': comment.created_utc,
                'created_datetime': datetime.fromtimestamp(comment.created_utc).isoformat(),
                'score': comment.score,
                'ups': getattr(comment, 'ups', None),
                'downs': getattr(comment, 'downs', None),
                'gilded': comment.gilded,
                'total_awards_received': comment.total_awards_received,
                'edited': comment.edited if comment.edited else False,
                'distinguished': comment.distinguished,
                'stickied': comment.stickied,
                'is_submitter': comment.is_submitter,
                'controversiality': comment.controversiality,
                'depth': self._get_comment_depth(comment),
                'permalink': f"https://reddit.com{comment.permalink}" if hasattr(comment, 'permalink') else '',
            }
            
            # Subreddit information
            if hasattr(comment, 'subreddit'):
                comment_data['subreddit'] = str(comment.subreddit)
            else:
                comment_data['subreddit'] = ''
            
            # Author flair
            comment_data['author_flair_text'] = comment.author_flair_text
            comment_data['author_flair_css_class'] = comment.author_flair_css_class
            
            # Awards information
            if hasattr(comment, 'all_awardings') and comment.all_awardings:
                comment_data['awards'] = [
                    {
                        'name': award.get('name', ''),
                        'count': award.get('count', 0),
                        'coin_price': award.get('coin_price', 0)
                    }
                    for award in comment.all_awardings
                ]
            else:
                comment_data['awards'] = []
            
            # Parent comment information
            if comment.parent_id.startswith('t1_'):  # It's a reply to another comment
                comment_data['is_reply'] = True
                comment_data['parent_comment_id'] = comment.parent_id[3:]  # Remove 't1_' prefix
            else:  # It's a top-level comment
                comment_data['is_reply'] = False
                comment_data['parent_comment_id'] = None
            
            # Comment thread information
            comment_data['is_root'] = comment.is_root
            comment_data['link_id'] = comment.link_id
            
            # Additional metadata
            comment_data['can_mod_post'] = getattr(comment, 'can_mod_post', False)
            comment_data['send_replies'] = getattr(comment, 'send_replies', True)
            comment_data['saved'] = getattr(comment, 'saved', False)
            comment_data['archived'] = getattr(comment, 'archived', False)
            comment_data['locked'] = getattr(comment, 'locked', False)
            comment_data['collapsed'] = getattr(comment, 'collapsed', False)
            comment_data['collapsed_reason'] = getattr(comment, 'collapsed_reason', None)
            comment_data['associated_award'] = getattr(comment, 'associated_award', None)
            comment_data['score_hidden'] = getattr(comment, 'score_hidden', False)
            
            # Reply count (number of direct replies)
            if hasattr(comment, 'replies') and comment.replies:
                try:
                    comment_data['reply_count'] = len(comment.replies)
                except:
                    comment_data['reply_count'] = 0
            else:
                comment_data['reply_count'] = 0
            
            # Comment length statistics
            comment_data['body_length'] = len(comment.body)
            comment_data['word_count'] = len(comment.body.split())
            comment_data['line_count'] = comment.body.count('\n') + 1
            
            # Scraping metadata
            comment_data['scraped_at'] = datetime.now().isoformat()
            comment_data['scraper_version'] = '1.0.0'
            
            return comment_data
            
        except Exception as e:
            self.logger.error(f"Error scraping comment {getattr(comment, 'id', 'unknown')}: {str(e)}")
            # Return minimal data structure on error
            return {
                'type': 'comment',
                'id': getattr(comment, 'id', 'unknown'),
                'body': getattr(comment, 'body', 'Error loading comment'),
                'author': str(getattr(comment, 'author', '[error]')),
                'error': str(e),
                'scraped_at': datetime.now().isoformat()
            }
    
    def _get_comment_depth(self, comment: praw.models.Comment) -> int:
        """Calculate the depth of a comment in the thread"""
        try:
            depth = 0
            current = comment
            
            while hasattr(current, 'parent') and current.parent_id.startswith('t1_'):
                depth += 1
                try:
                    current = current.parent()
                    if depth > 20:  # Prevent infinite loops
                        break
                except:
                    break
            
            return depth
            
        except Exception:
            return 0
    
    def scrape_comment_thread(self, comment: praw.models.Comment, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Scrape a comment and all its replies up to max_depth"""
        try:
            comments = []
            
            # Scrape the main comment
            comment_data = self.scrape_comment(comment)
            if comment_data:
                comments.append(comment_data)
            
            # Scrape replies if within depth limit
            if max_depth > 0 and hasattr(comment, 'replies'):
                try:
                    comment.replies.replace_more(limit=0)
                    for reply in comment.replies:
                        if isinstance(reply, praw.models.Comment):
                            reply_comments = self.scrape_comment_thread(reply, max_depth - 1)
                            comments.extend(reply_comments)
                except Exception as e:
                    self.logger.error(f"Error scraping replies for comment {comment.id}: {str(e)}")
            
            return comments
            
        except Exception as e:
            self.logger.error(f"Error scraping comment thread: {str(e)}")
            return []
    
    def get_comment_statistics(self, comment: praw.models.Comment) -> Dict[str, Any]:
        """Get detailed statistics for a comment"""
        try:
            return {
                'id': comment.id,
                'score': comment.score,
                'controversiality': comment.controversiality,
                'total_awards_received': comment.total_awards_received,
                'gilded': comment.gilded,
                'body_length': len(comment.body),
                'word_count': len(comment.body.split()),
                'reply_count': len(comment.replies) if hasattr(comment, 'replies') else 0,
                'depth': self._get_comment_depth(comment),
                'created_utc': comment.created_utc,
                'age_hours': (datetime.now().timestamp() - comment.created_utc) / 3600,
                'is_reply': comment.parent_id.startswith('t1_'),
                'is_submitter': comment.is_submitter
            }
        except Exception as e:
            self.logger.error(f"Error getting comment statistics: {str(e)}")
            return {}
    
    def is_comment_accessible(self, comment: praw.models.Comment) -> bool:
        """Check if comment is accessible (not deleted/removed)"""
        try:
            # Check if comment is deleted or removed
            if comment.author is None and comment.body in ['[deleted]', '[removed]']:
                return False
            
            # Check if we can access basic properties
            _ = comment.body
            _ = comment.score
            
            return True
            
        except Exception:
            return False
    
    def filter_comments_by_score(self, comments: List[Dict[str, Any]], min_score: int = 1) -> List[Dict[str, Any]]:
        """Filter comments by minimum score"""
        return [comment for comment in comments if comment.get('score', 0) >= min_score]
    
    def filter_comments_by_length(self, comments: List[Dict[str, Any]], min_length: int = 10) -> List[Dict[str, Any]]:
        """Filter comments by minimum body length"""
        return [comment for comment in comments if comment.get('body_length', 0) >= min_length]
    
    def sort_comments_by_score(self, comments: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
        """Sort comments by score"""
        return sorted(comments, key=lambda x: x.get('score', 0), reverse=reverse)
    
    def get_top_level_comments(self, comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get only top-level comments (direct replies to post)"""
        return [comment for comment in comments if not comment.get('is_reply', False)]
    
    def get_comment_replies(self, comments: List[Dict[str, Any]], parent_id: str) -> List[Dict[str, Any]]:
        """Get all replies to a specific comment"""
        return [comment for comment in comments if comment.get('parent_comment_id') == parent_id]
