"""
Post Scraper for RedScraperPro
🩸 Specialized Reddit post scraping functionality 🩸
"""

import praw
from datetime import datetime
from typing import Dict, Any, Optional
from redscraperpro.utils.logger import Logger
from redscraperpro.utils.progress import ProgressTracker


class PostScraper:
    """Handles Reddit post scraping"""
    
    def __init__(self, reddit: praw.Reddit, logger: Logger, progress_tracker: ProgressTracker):
        self.reddit = reddit
        self.logger = logger
        self.progress_tracker = progress_tracker
    
    def scrape_post(self, post: praw.models.Submission) -> Dict[str, Any]:
        """Scrape data from a Reddit post"""
        try:
            # Basic post information
            post_data = {
                'type': 'post',
                'id': post.id,
                'title': post.title,
                'author': str(post.author) if post.author else '[deleted]',
                'subreddit': str(post.subreddit),
                'created_utc': post.created_utc,
                'created_datetime': datetime.fromtimestamp(post.created_utc).isoformat(),
                'score': post.score,
                'upvote_ratio': post.upvote_ratio,
                'num_comments': post.num_comments,
                'url': post.url,
                'permalink': f"https://reddit.com{post.permalink}",
                'is_self': post.is_self,
                'selftext': post.selftext,
                'content': post.selftext if post.is_self else '',
                'domain': post.domain,
                'is_video': post.is_video,
                'over_18': post.over_18,
                'spoiler': post.spoiler,
                'locked': post.locked,
                'stickied': post.stickied,
                'distinguished': post.distinguished,
                'edited': post.edited if post.edited else False,
                'gilded': post.gilded,
                'total_awards_received': post.total_awards_received,
                'treatment_tags': getattr(post, 'treatment_tags', []),
            }
            
            # Post flair
            post_data['link_flair_text'] = post.link_flair_text
            post_data['link_flair_css_class'] = post.link_flair_css_class
            
            # Author flair
            post_data['author_flair_text'] = post.author_flair_text
            post_data['author_flair_css_class'] = post.author_flair_css_class
            
            # Media information
            if hasattr(post, 'media') and post.media:
                post_data['media_type'] = 'video' if post.is_video else 'other'
                post_data['media_url'] = self._extract_media_url(post)
            else:
                post_data['media_type'] = None
                post_data['media_url'] = None
            
            # Preview images
            if hasattr(post, 'preview') and post.preview:
                try:
                    preview_images = post.preview['images']
                    if preview_images:
                        post_data['preview_image'] = preview_images[0]['source']['url']
                    else:
                        post_data['preview_image'] = None
                except (KeyError, IndexError):
                    post_data['preview_image'] = None
            else:
                post_data['preview_image'] = None
            
            # Thumbnail
            post_data['thumbnail'] = post.thumbnail if hasattr(post, 'thumbnail') else None
            
            # Awards information
            if hasattr(post, 'all_awardings') and post.all_awardings:
                post_data['awards'] = [
                    {
                        'name': award.get('name', ''),
                        'count': award.get('count', 0),
                        'coin_price': award.get('coin_price', 0)
                    }
                    for award in post.all_awardings
                ]
            else:
                post_data['awards'] = []
            
            # Additional metadata
            post_data['is_original_content'] = getattr(post, 'is_original_content', False)
            post_data['is_reddit_media_domain'] = getattr(post, 'is_reddit_media_domain', False)
            post_data['is_meta'] = getattr(post, 'is_meta', False)
            post_data['pinned'] = getattr(post, 'pinned', False)
            post_data['archived'] = getattr(post, 'archived', False)
            post_data['can_mod_post'] = getattr(post, 'can_mod_post', False)
            post_data['contest_mode'] = getattr(post, 'contest_mode', False)
            post_data['hide_score'] = getattr(post, 'hide_score', False)
            
            # Crosspost information
            if hasattr(post, 'crosspost_parent_list') and post.crosspost_parent_list:
                crosspost_parent = post.crosspost_parent_list[0]
                post_data['is_crosspost'] = True
                post_data['crosspost_parent'] = {
                    'id': crosspost_parent.get('id', ''),
                    'subreddit': crosspost_parent.get('subreddit', ''),
                    'title': crosspost_parent.get('title', ''),
                    'author': crosspost_parent.get('author', '')
                }
            else:
                post_data['is_crosspost'] = False
                post_data['crosspost_parent'] = None
            
            # Poll data (if applicable)
            if hasattr(post, 'poll_data') and post.poll_data:
                post_data['poll_data'] = {
                    'total_vote_count': post.poll_data.total_vote_count,
                    'voting_end_timestamp': post.poll_data.voting_end_timestamp,
                    'options': [
                        {
                            'text': option.text,
                            'vote_count': option.vote_count
                        }
                        for option in post.poll_data.options
                    ]
                }
            else:
                post_data['poll_data'] = None
            
            # Gallery data (if applicable)
            if hasattr(post, 'is_gallery') and post.is_gallery:
                post_data['is_gallery'] = True
                if hasattr(post, 'media_metadata') and post.media_metadata:
                    post_data['gallery_images'] = [
                        {
                            'id': img_id,
                            'url': img_data.get('s', {}).get('u', '').replace('preview.redd.it', 'i.redd.it')
                        }
                        for img_id, img_data in post.media_metadata.items()
                        if 's' in img_data
                    ]
                else:
                    post_data['gallery_images'] = []
            else:
                post_data['is_gallery'] = False
                post_data['gallery_images'] = []
            
            # Scraping metadata
            post_data['scraped_at'] = datetime.now().isoformat()
            post_data['scraper_version'] = '1.0.0'
            
            return post_data
            
        except Exception as e:
            self.logger.error(f"Error scraping post {post.id}: {str(e)}")
            # Return minimal data structure on error
            return {
                'type': 'post',
                'id': getattr(post, 'id', 'unknown'),
                'title': getattr(post, 'title', 'Error loading post'),
                'author': str(getattr(post, 'author', '[error]')),
                'subreddit': str(getattr(post, 'subreddit', '[error]')),
                'error': str(e),
                'scraped_at': datetime.now().isoformat()
            }
    
    def _extract_media_url(self, post: praw.models.Submission) -> Optional[str]:
        """Extract media URL from post"""
        try:
            # Reddit video
            if hasattr(post, 'media') and post.media and 'reddit_video' in post.media:
                return post.media['reddit_video'].get('fallback_url', '')
            
            # YouTube video
            if hasattr(post, 'media') and post.media and 'oembed' in post.media:
                return post.media['oembed'].get('thumbnail_url', '')
            
            # Direct image/video URL
            if post.url and any(ext in post.url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm']):
                return post.url
            
            # Imgur links
            if 'imgur.com' in post.url and not post.url.endswith('.gifv'):
                if '/a/' not in post.url and '/gallery/' not in post.url:
                    # Single image
                    img_id = post.url.split('/')[-1]
                    return f"https://i.imgur.com/{img_id}.jpg"
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error extracting media URL: {str(e)}")
            return None
    
    def get_post_statistics(self, post: praw.models.Submission) -> Dict[str, Any]:
        """Get detailed statistics for a post"""
        try:
            return {
                'id': post.id,
                'score': post.score,
                'upvote_ratio': post.upvote_ratio,
                'num_comments': post.num_comments,
                'total_awards_received': post.total_awards_received,
                'gilded': post.gilded,
                'view_count': getattr(post, 'view_count', None),
                'engagement_ratio': post.num_comments / max(post.score, 1),
                'awards_per_score': post.total_awards_received / max(post.score, 1),
                'created_utc': post.created_utc,
                'age_hours': (datetime.now().timestamp() - post.created_utc) / 3600
            }
        except Exception as e:
            self.logger.error(f"Error getting post statistics: {str(e)}")
            return {}
    
    def is_post_accessible(self, post: praw.models.Submission) -> bool:
        """Check if post is accessible (not deleted/removed)"""
        try:
            # Check if post is deleted or removed
            if post.author is None and post.selftext == '[deleted]':
                return False
            
            if post.author is None and post.selftext == '[removed]':
                return False
            
            # Check if we can access basic properties
            _ = post.title
            _ = post.score
            
            return True
            
        except Exception:
            return False
