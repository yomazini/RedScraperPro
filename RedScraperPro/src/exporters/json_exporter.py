"""
JSON Exporter for RedScraperPro
🩸 Export scraped data to JSON format 🩸
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..utils.config import Config
from ..utils.logger import Logger


class JSONExporter:
    """Handles JSON export functionality"""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.output_dir = config.get_output_directory()
    
    def export(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data to JSON format"""
        if not data:
            raise ValueError("No data to export")
        
        # Ensure filename has .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.output_dir / filename
        
        try:
            # Prepare export data with metadata
            export_data = {
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "total_items": len(data),
                    "posts_count": len([item for item in data if item.get('type') == 'post']),
                    "comments_count": len([item for item in data if item.get('type') == 'comment']),
                    "scraper_version": "1.0.0",
                    "export_format": "json"
                },
                "data": data
            }
            
            # Write JSON file with proper formatting
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(
                    export_data, 
                    jsonfile, 
                    indent=2, 
                    ensure_ascii=False,
                    default=self._json_serializer
                )
            
            self.logger.export_complete(str(filepath), len(data))
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"JSON export failed: {str(e)}")
            raise
    
    def export_compact(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data to compact JSON format (no indentation)"""
        if not data:
            raise ValueError("No data to export")
        
        # Ensure filename has .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.output_dir / filename
        
        try:
            # Prepare export data
            export_data = {
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "total_items": len(data),
                    "scraper_version": "1.0.0"
                },
                "data": data
            }
            
            # Write compact JSON file
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(
                    export_data, 
                    jsonfile, 
                    separators=(',', ':'),
                    ensure_ascii=False,
                    default=self._json_serializer
                )
            
            self.logger.export_complete(str(filepath), len(data))
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Compact JSON export failed: {str(e)}")
            raise
    
    def export_posts_only(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export only posts to JSON format"""
        posts_data = [item for item in data if item.get('type') == 'post']
        
        if not filename.endswith('.json'):
            filename += '_posts.json'
        
        return self.export(posts_data, filename)
    
    def export_comments_only(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export only comments to JSON format"""
        comments_data = [item for item in data if item.get('type') == 'comment']
        
        if not filename.endswith('.json'):
            filename += '_comments.json'
        
        return self.export(comments_data, filename)
    
    def export_by_subreddit(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data organized by subreddit"""
        if not data:
            raise ValueError("No data to export")
        
        # Ensure filename has .json extension
        if not filename.endswith('.json'):
            filename += '_by_subreddit.json'
        
        filepath = self.output_dir / filename
        
        try:
            # Organize data by subreddit
            subreddit_data = {}
            
            for item in data:
                subreddit = item.get('subreddit', 'unknown')
                if subreddit not in subreddit_data:
                    subreddit_data[subreddit] = {
                        'posts': [],
                        'comments': [],
                        'statistics': {
                            'total_items': 0,
                            'posts_count': 0,
                            'comments_count': 0,
                            'total_score': 0,
                            'average_score': 0
                        }
                    }
                
                # Add item to appropriate category
                if item.get('type') == 'post':
                    subreddit_data[subreddit]['posts'].append(item)
                    subreddit_data[subreddit]['statistics']['posts_count'] += 1
                elif item.get('type') == 'comment':
                    subreddit_data[subreddit]['comments'].append(item)
                    subreddit_data[subreddit]['statistics']['comments_count'] += 1
                
                # Update statistics
                subreddit_data[subreddit]['statistics']['total_items'] += 1
                subreddit_data[subreddit]['statistics']['total_score'] += item.get('score', 0)
            
            # Calculate averages
            for subreddit, data_dict in subreddit_data.items():
                stats = data_dict['statistics']
                if stats['total_items'] > 0:
                    stats['average_score'] = stats['total_score'] / stats['total_items']
            
            # Prepare export data
            export_data = {
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "total_subreddits": len(subreddit_data),
                    "total_items": len(data),
                    "organization": "by_subreddit",
                    "scraper_version": "1.0.0"
                },
                "subreddits": subreddit_data
            }
            
            # Write JSON file
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(
                    export_data, 
                    jsonfile, 
                    indent=2, 
                    ensure_ascii=False,
                    default=self._json_serializer
                )
            
            self.logger.export_complete(str(filepath), len(data))
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Subreddit-organized JSON export failed: {str(e)}")
            raise
    
    def export_by_author(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data organized by author"""
        if not data:
            raise ValueError("No data to export")
        
        # Ensure filename has .json extension
        if not filename.endswith('.json'):
            filename += '_by_author.json'
        
        filepath = self.output_dir / filename
        
        try:
            # Organize data by author
            author_data = {}
            
            for item in data:
                author = item.get('author', 'unknown')
                if author not in author_data:
                    author_data[author] = {
                        'posts': [],
                        'comments': [],
                        'statistics': {
                            'total_items': 0,
                            'posts_count': 0,
                            'comments_count': 0,
                            'total_score': 0,
                            'average_score': 0,
                            'subreddits': set()
                        }
                    }
                
                # Add item to appropriate category
                if item.get('type') == 'post':
                    author_data[author]['posts'].append(item)
                    author_data[author]['statistics']['posts_count'] += 1
                elif item.get('type') == 'comment':
                    author_data[author]['comments'].append(item)
                    author_data[author]['statistics']['comments_count'] += 1
                
                # Update statistics
                author_data[author]['statistics']['total_items'] += 1
                author_data[author]['statistics']['total_score'] += item.get('score', 0)
                author_data[author]['statistics']['subreddits'].add(item.get('subreddit', 'unknown'))
            
            # Calculate averages and convert sets to lists
            for author, data_dict in author_data.items():
                stats = data_dict['statistics']
                if stats['total_items'] > 0:
                    stats['average_score'] = stats['total_score'] / stats['total_items']
                stats['unique_subreddits'] = len(stats['subreddits'])
                stats['subreddits'] = list(stats['subreddits'])  # Convert set to list for JSON serialization
            
            # Prepare export data
            export_data = {
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "total_authors": len(author_data),
                    "total_items": len(data),
                    "organization": "by_author",
                    "scraper_version": "1.0.0"
                },
                "authors": author_data
            }
            
            # Write JSON file
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(
                    export_data, 
                    jsonfile, 
                    indent=2, 
                    ensure_ascii=False,
                    default=self._json_serializer
                )
            
            self.logger.export_complete(str(filepath), len(data))
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Author-organized JSON export failed: {str(e)}")
            raise
    
    def export_statistics_only(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export only statistics and metadata"""
        if not data:
            raise ValueError("No data to export")
        
        # Ensure filename has .json extension
        if not filename.endswith('.json'):
            filename += '_stats.json'
        
        filepath = self.output_dir / filename
        
        try:
            # Calculate comprehensive statistics
            posts = [item for item in data if item.get('type') == 'post']
            comments = [item for item in data if item.get('type') == 'comment']
            
            # Subreddit statistics
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
            
            # Author statistics
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
            
            # Prepare statistics data
            statistics_data = {
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "scraper_version": "1.0.0",
                    "export_type": "statistics_only"
                },
                "overall_statistics": {
                    "total_items": len(data),
                    "posts_count": len(posts),
                    "comments_count": len(comments),
                    "total_score": sum(item.get('score', 0) for item in data),
                    "average_score": sum(item.get('score', 0) for item in data) / len(data) if data else 0,
                    "max_score": max(item.get('score', 0) for item in data) if data else 0,
                    "min_score": min(item.get('score', 0) for item in data) if data else 0,
                    "unique_subreddits": len(subreddit_stats),
                    "unique_authors": len(author_stats)
                },
                "subreddit_statistics": dict(sorted(subreddit_stats.items(), key=lambda x: x[1]['posts'] + x[1]['comments'], reverse=True)),
                "author_statistics": dict(sorted(author_stats.items(), key=lambda x: x[1]['posts'] + x[1]['comments'], reverse=True)),
                "posts_statistics": {
                    "count": len(posts),
                    "average_score": sum(item.get('score', 0) for item in posts) / len(posts) if posts else 0,
                    "average_comments": sum(item.get('num_comments', 0) for item in posts) / len(posts) if posts else 0,
                } if posts else {},
                "comments_statistics": {
                    "count": len(comments),
                    "average_score": sum(item.get('score', 0) for item in comments) / len(comments) if comments else 0,
                    "average_length": sum(len(item.get('body', '')) for item in comments) / len(comments) if comments else 0,
                } if comments else {}
            }
            
            # Write JSON file
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(
                    statistics_data, 
                    jsonfile, 
                    indent=2, 
                    ensure_ascii=False,
                    default=self._json_serializer
                )
            
            self.logger.export_complete(str(filepath), len(data))
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Statistics JSON export failed: {str(e)}")
            raise
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for non-serializable objects"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return str(obj)
