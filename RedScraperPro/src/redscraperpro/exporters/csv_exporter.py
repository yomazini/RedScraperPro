"""
CSV Exporter for RedScraperPro
🩸 Export scraped data to CSV format 🩸
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from redscraperpro.utils.config import Config
from redscraperpro.utils.logger import Logger


class CSVExporter:
    """Handles CSV export functionality"""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.output_dir = config.get_output_directory()
    
    def export(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export data to CSV format"""
        if not data:
            raise ValueError("No data to export")
        
        # Ensure filename has .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = self.output_dir / filename
        
        try:
            # Flatten nested data and prepare for CSV
            flattened_data = self._flatten_data(data)
            
            # Get all unique fieldnames
            fieldnames = self._get_fieldnames(flattened_data)
            
            # Write CSV file
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for row in flattened_data:
                    # Ensure all fields are present
                    complete_row = {field: row.get(field, '') for field in fieldnames}
                    writer.writerow(complete_row)
            
            self.logger.export_complete(str(filepath), len(data))
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"CSV export failed: {str(e)}")
            raise
    
    def _flatten_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flatten nested dictionaries and lists for CSV export"""
        flattened = []
        
        for item in data:
            flat_item = {}
            self._flatten_dict(item, flat_item)
            flattened.append(flat_item)
        
        return flattened
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """Recursively flatten a nested dictionary"""
        items = []
        
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Handle lists by converting to JSON string or flattening if list of dicts
                if v and isinstance(v[0], dict):
                    # List of dictionaries - convert to JSON string
                    items.append((new_key, json.dumps(v, ensure_ascii=False)))
                else:
                    # Simple list - join as string
                    items.append((new_key, ', '.join(map(str, v)) if v else ''))
            elif v is None:
                items.append((new_key, ''))
            elif isinstance(v, bool):
                items.append((new_key, str(v)))
            else:
                items.append((new_key, str(v)))
        
        return dict(items)
    
    def _get_fieldnames(self, data: List[Dict[str, Any]]) -> List[str]:
        """Get all unique fieldnames from the data"""
        fieldnames = set()
        
        for item in data:
            fieldnames.update(item.keys())
        
        # Sort fieldnames for consistent column order
        sorted_fieldnames = sorted(fieldnames)
        
        # Move common fields to the front
        priority_fields = [
            'type', 'id', 'title', 'author', 'subreddit', 'created_datetime', 
            'score', 'body', 'content', 'url', 'permalink'
        ]
        
        ordered_fieldnames = []
        
        # Add priority fields first (if they exist)
        for field in priority_fields:
            if field in sorted_fieldnames:
                ordered_fieldnames.append(field)
                sorted_fieldnames.remove(field)
        
        # Add remaining fields
        ordered_fieldnames.extend(sorted_fieldnames)
        
        return ordered_fieldnames
    
    def export_with_custom_fields(self, data: List[Dict[str, Any]], filename: str, 
                                 fields: List[str]) -> str:
        """Export data with only specified fields"""
        if not data:
            raise ValueError("No data to export")
        
        # Ensure filename has .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = self.output_dir / filename
        
        try:
            # Flatten data first
            flattened_data = self._flatten_data(data)
            
            # Write CSV file with only specified fields
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields, extrasaction='ignore')
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for row in flattened_data:
                    # Only include specified fields
                    filtered_row = {field: row.get(field, '') for field in fields}
                    writer.writerow(filtered_row)
            
            self.logger.export_complete(str(filepath), len(data))
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Custom CSV export failed: {str(e)}")
            raise
    
    def export_posts_only(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export only posts (filter out comments)"""
        posts_data = [item for item in data if item.get('type') == 'post']
        return self.export(posts_data, filename)
    
    def export_comments_only(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export only comments (filter out posts)"""
        comments_data = [item for item in data if item.get('type') == 'comment']
        return self.export(comments_data, filename)
    
    def export_summary_stats(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Export summary statistics as CSV"""
        if not data:
            raise ValueError("No data to export")
        
        # Calculate statistics
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
        
        # Prepare summary data
        summary_data = []
        
        # Overall statistics
        summary_data.append({
            'metric': 'Total Items',
            'value': len(data),
            'category': 'Overall'
        })
        summary_data.append({
            'metric': 'Total Posts',
            'value': len(posts),
            'category': 'Overall'
        })
        summary_data.append({
            'metric': 'Total Comments',
            'value': len(comments),
            'category': 'Overall'
        })
        summary_data.append({
            'metric': 'Total Score',
            'value': sum(item.get('score', 0) for item in data),
            'category': 'Overall'
        })
        summary_data.append({
            'metric': 'Average Score',
            'value': sum(item.get('score', 0) for item in data) / len(data) if data else 0,
            'category': 'Overall'
        })
        
        # Top subreddits
        top_subreddits = sorted(subreddit_stats.items(), key=lambda x: x[1]['posts'] + x[1]['comments'], reverse=True)[:10]
        for subreddit, stats in top_subreddits:
            summary_data.append({
                'metric': f'Subreddit: {subreddit}',
                'value': f"Posts: {stats['posts']}, Comments: {stats['comments']}, Score: {stats['total_score']}",
                'category': 'Top Subreddits'
            })
        
        # Top authors
        top_authors = sorted(author_stats.items(), key=lambda x: x[1]['posts'] + x[1]['comments'], reverse=True)[:10]
        for author, stats in top_authors:
            summary_data.append({
                'metric': f'Author: {author}',
                'value': f"Posts: {stats['posts']}, Comments: {stats['comments']}, Score: {stats['total_score']}",
                'category': 'Top Authors'
            })
        
        # Export summary
        if not filename.endswith('.csv'):
            filename += '_summary.csv'
        
        return self.export(summary_data, filename)
