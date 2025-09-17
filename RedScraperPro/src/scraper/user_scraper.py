"""
User Scraper for RedScraperPro
🩸 Specialized Reddit user profile scraping functionality 🩸
"""

import praw
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..utils.logger import Logger
from ..utils.progress import ProgressTracker


class UserScraper:
    """Handles Reddit user profile scraping"""
    
    def __init__(self, reddit: praw.Reddit, logger: Logger, progress_tracker: ProgressTracker):
        self.reddit = reddit
        self.logger = logger
        self.progress_tracker = progress_tracker
    
    def scrape_user_profile(self, username: str) -> Dict[str, Any]:
        """Scrape comprehensive user profile information"""
        try:
            user = self.reddit.redditor(username)
            
            # Basic user information
            user_data = {
                'type': 'user_profile',
                'username': user.name,
                'id': user.id,
                'created_utc': user.created_utc,
                'created_datetime': datetime.fromtimestamp(user.created_utc).isoformat(),
                'comment_karma': user.comment_karma,
                'link_karma': user.link_karma,
                'total_karma': user.comment_karma + user.link_karma,
                'is_gold': user.is_gold,
                'is_mod': user.is_mod,
                'has_verified_email': user.has_verified_email,
                'icon_img': getattr(user, 'icon_img', ''),
                'profile_url': f"https://reddit.com/u/{user.name}",
            }
            
            # Account age
            account_age_days = (datetime.now().timestamp() - user.created_utc) / (24 * 3600)
            user_data['account_age_days'] = int(account_age_days)
            user_data['account_age_years'] = round(account_age_days / 365.25, 2)
            
            # Additional profile information (if available)
            try:
                user_data['is_employee'] = getattr(user, 'is_employee', False)
                user_data['is_friend'] = getattr(user, 'is_friend', False)
                user_data['is_blocked'] = getattr(user, 'is_blocked', False)
                user_data['has_subscribed'] = getattr(user, 'has_subscribed', False)
                user_data['hide_from_robots'] = getattr(user, 'hide_from_robots', False)
                user_data['verified'] = getattr(user, 'verified', False)
                user_data['is_suspended'] = getattr(user, 'is_suspended', False)
            except Exception as e:
                self.logger.debug(f"Could not get extended profile info for {username}: {str(e)}")
            
            # Profile description/bio (if available)
            try:
                if hasattr(user, 'subreddit') and user.subreddit:
                    user_data['profile_description'] = user.subreddit.public_description
                    user_data['profile_title'] = user.subreddit.title
                else:
                    user_data['profile_description'] = ''
                    user_data['profile_title'] = ''
            except Exception:
                user_data['profile_description'] = ''
                user_data['profile_title'] = ''
            
            # Karma ratios and statistics
            if user_data['total_karma'] > 0:
                user_data['comment_karma_ratio'] = user.comment_karma / user_data['total_karma']
                user_data['link_karma_ratio'] = user.link_karma / user_data['total_karma']
            else:
                user_data['comment_karma_ratio'] = 0
                user_data['link_karma_ratio'] = 0
            
            # Average karma per day
            if account_age_days > 0:
                user_data['avg_karma_per_day'] = user_data['total_karma'] / account_age_days
            else:
                user_data['avg_karma_per_day'] = 0
            
            # Scraping metadata
            user_data['scraped_at'] = datetime.now().isoformat()
            user_data['scraper_version'] = '1.0.0'
            
            return user_data
            
        except Exception as e:
            self.logger.error(f"Error scraping user profile {username}: {str(e)}")
            return {
                'type': 'user_profile',
                'username': username,
                'error': str(e),
                'scraped_at': datetime.now().isoformat()
            }
    
    def scrape_user_submissions(self, username: str, limit: int = 100, 
                               sort: str = 'new') -> List[Dict[str, Any]]:
        """Scrape user's submissions (posts)"""
        try:
            user = self.reddit.redditor(username)
            submissions = []
            
            # Get submissions based on sort method
            if sort == 'new':
                user_submissions = user.submissions.new(limit=limit)
            elif sort == 'hot':
                user_submissions = user.submissions.hot(limit=limit)
            elif sort == 'top':
                user_submissions = user.submissions.top(limit=limit, time_filter='all')
            else:
                user_submissions = user.submissions.new(limit=limit)
            
            for submission in user_submissions:
                try:
                    # Import here to avoid circular imports
                    from .post_scraper import PostScraper
                    post_scraper = PostScraper(self.reddit, self.logger, self.progress_tracker)
                    
                    submission_data = post_scraper.scrape_post(submission)
                    submission_data['scraped_from_user'] = username
                    submissions.append(submission_data)
                    
                except Exception as e:
                    self.logger.error(f"Error scraping submission {submission.id} from user {username}: {str(e)}")
                    continue
            
            return submissions
            
        except Exception as e:
            self.logger.error(f"Error scraping submissions for user {username}: {str(e)}")
            return []
    
    def scrape_user_comments(self, username: str, limit: int = 100, 
                           sort: str = 'new') -> List[Dict[str, Any]]:
        """Scrape user's comments"""
        try:
            user = self.reddit.redditor(username)
            comments = []
            
            # Get comments based on sort method
            if sort == 'new':
                user_comments = user.comments.new(limit=limit)
            elif sort == 'hot':
                user_comments = user.comments.hot(limit=limit)
            elif sort == 'top':
                user_comments = user.comments.top(limit=limit, time_filter='all')
            else:
                user_comments = user.comments.new(limit=limit)
            
            for comment in user_comments:
                try:
                    # Import here to avoid circular imports
                    from .comment_scraper import CommentScraper
                    comment_scraper = CommentScraper(self.reddit, self.logger, self.progress_tracker)
                    
                    comment_data = comment_scraper.scrape_comment(comment)
                    if comment_data:
                        comment_data['scraped_from_user'] = username
                        comments.append(comment_data)
                    
                except Exception as e:
                    self.logger.error(f"Error scraping comment {comment.id} from user {username}: {str(e)}")
                    continue
            
            return comments
            
        except Exception as e:
            self.logger.error(f"Error scraping comments for user {username}: {str(e)}")
            return []
    
    def get_user_activity_summary(self, username: str, days: int = 30) -> Dict[str, Any]:
        """Get user activity summary for the last N days"""
        try:
            user = self.reddit.redditor(username)
            
            # Get recent submissions and comments
            recent_submissions = list(user.submissions.new(limit=100))
            recent_comments = list(user.comments.new(limit=100))
            
            # Filter by date
            cutoff_timestamp = datetime.now().timestamp() - (days * 24 * 3600)
            
            recent_submissions = [s for s in recent_submissions if s.created_utc >= cutoff_timestamp]
            recent_comments = [c for c in recent_comments if c.created_utc >= cutoff_timestamp]
            
            # Calculate statistics
            total_submission_score = sum(s.score for s in recent_submissions)
            total_comment_score = sum(c.score for c in recent_comments)
            
            # Get subreddit activity
            submission_subreddits = {}
            comment_subreddits = {}
            
            for submission in recent_submissions:
                subreddit_name = str(submission.subreddit)
                submission_subreddits[subreddit_name] = submission_subreddits.get(subreddit_name, 0) + 1
            
            for comment in recent_comments:
                subreddit_name = str(comment.subreddit)
                comment_subreddits[subreddit_name] = comment_subreddits.get(subreddit_name, 0) + 1
            
            return {
                'username': username,
                'period_days': days,
                'submissions_count': len(recent_submissions),
                'comments_count': len(recent_comments),
                'total_posts': len(recent_submissions) + len(recent_comments),
                'submission_karma': total_submission_score,
                'comment_karma': total_comment_score,
                'total_karma_earned': total_submission_score + total_comment_score,
                'avg_submission_score': total_submission_score / len(recent_submissions) if recent_submissions else 0,
                'avg_comment_score': total_comment_score / len(recent_comments) if recent_comments else 0,
                'posts_per_day': (len(recent_submissions) + len(recent_comments)) / days,
                'most_active_subreddits_submissions': dict(sorted(submission_subreddits.items(), key=lambda x: x[1], reverse=True)[:10]),
                'most_active_subreddits_comments': dict(sorted(comment_subreddits.items(), key=lambda x: x[1], reverse=True)[:10]),
                'unique_subreddits': len(set(list(submission_subreddits.keys()) + list(comment_subreddits.keys()))),
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting activity summary for user {username}: {str(e)}")
            return {
                'username': username,
                'error': str(e),
                'scraped_at': datetime.now().isoformat()
            }
    
    def get_user_subreddit_activity(self, username: str, limit: int = 1000) -> Dict[str, Any]:
        """Analyze user's activity across different subreddits"""
        try:
            user = self.reddit.redditor(username)
            
            # Get user's submissions and comments
            submissions = list(user.submissions.new(limit=limit))
            comments = list(user.comments.new(limit=limit))
            
            subreddit_stats = {}
            
            # Analyze submissions
            for submission in submissions:
                subreddit_name = str(submission.subreddit)
                if subreddit_name not in subreddit_stats:
                    subreddit_stats[subreddit_name] = {
                        'submissions': 0,
                        'comments': 0,
                        'submission_karma': 0,
                        'comment_karma': 0,
                        'total_posts': 0,
                        'avg_submission_score': 0,
                        'avg_comment_score': 0
                    }
                
                subreddit_stats[subreddit_name]['submissions'] += 1
                subreddit_stats[subreddit_name]['submission_karma'] += submission.score
                subreddit_stats[subreddit_name]['total_posts'] += 1
            
            # Analyze comments
            for comment in comments:
                subreddit_name = str(comment.subreddit)
                if subreddit_name not in subreddit_stats:
                    subreddit_stats[subreddit_name] = {
                        'submissions': 0,
                        'comments': 0,
                        'submission_karma': 0,
                        'comment_karma': 0,
                        'total_posts': 0,
                        'avg_submission_score': 0,
                        'avg_comment_score': 0
                    }
                
                subreddit_stats[subreddit_name]['comments'] += 1
                subreddit_stats[subreddit_name]['comment_karma'] += comment.score
                subreddit_stats[subreddit_name]['total_posts'] += 1
            
            # Calculate averages
            for subreddit_name, stats in subreddit_stats.items():
                if stats['submissions'] > 0:
                    stats['avg_submission_score'] = stats['submission_karma'] / stats['submissions']
                if stats['comments'] > 0:
                    stats['avg_comment_score'] = stats['comment_karma'] / stats['comments']
                
                stats['total_karma'] = stats['submission_karma'] + stats['comment_karma']
                stats['avg_score'] = stats['total_karma'] / stats['total_posts'] if stats['total_posts'] > 0 else 0
            
            # Sort by total activity
            sorted_subreddits = dict(sorted(subreddit_stats.items(), key=lambda x: x[1]['total_posts'], reverse=True))
            
            return {
                'username': username,
                'total_subreddits': len(subreddit_stats),
                'subreddit_activity': sorted_subreddits,
                'most_active_subreddit': max(subreddit_stats.keys(), key=lambda x: subreddit_stats[x]['total_posts']) if subreddit_stats else None,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing subreddit activity for user {username}: {str(e)}")
            return {
                'username': username,
                'error': str(e),
                'scraped_at': datetime.now().isoformat()
            }
    
    def is_user_accessible(self, username: str) -> bool:
        """Check if user profile is accessible"""
        try:
            user = self.reddit.redditor(username)
            # Try to access basic properties
            _ = user.created_utc
            _ = user.comment_karma
            return True
        except Exception:
            return False
    
    def get_user_karma_breakdown(self, username: str) -> Dict[str, Any]:
        """Get detailed karma breakdown for a user"""
        try:
            user_profile = self.scrape_user_profile(username)
            
            if 'error' in user_profile:
                return user_profile
            
            # Get recent activity for karma analysis
            activity_summary = self.get_user_activity_summary(username, days=365)  # Last year
            
            return {
                'username': username,
                'total_karma': user_profile['total_karma'],
                'comment_karma': user_profile['comment_karma'],
                'link_karma': user_profile['link_karma'],
                'comment_karma_ratio': user_profile['comment_karma_ratio'],
                'link_karma_ratio': user_profile['link_karma_ratio'],
                'avg_karma_per_day': user_profile['avg_karma_per_day'],
                'account_age_days': user_profile['account_age_days'],
                'recent_karma_earned': activity_summary.get('total_karma_earned', 0),
                'recent_avg_submission_score': activity_summary.get('avg_submission_score', 0),
                'recent_avg_comment_score': activity_summary.get('avg_comment_score', 0),
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting karma breakdown for user {username}: {str(e)}")
            return {
                'username': username,
                'error': str(e),
                'scraped_at': datetime.now().isoformat()
            }
