"""
Configuration Management for RedScraperPro
🩸 Handles all configuration settings and user preferences 🩸
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from rich.console import Console


@dataclass
class RedditConfig:
    """Reddit API configuration"""
    client_id: str = ""
    client_secret: str = ""
    user_agent: str = "RedScraperPro:v1.0.0 (by /u/yourusername)"
    username: str = ""
    password: str = ""


@dataclass
class ScrapingConfig:
    """Scraping configuration"""
    default_limit: int = 100
    default_depth: int = 1
    include_comments: bool = True
    enable_sentiment: bool = False
    remove_duplicates: bool = True
    rate_limit_delay: float = 1.0
    max_retries: int = 3
    timeout: int = 30


@dataclass
class ExportConfig:
    """Export configuration"""
    default_format: str = "csv"
    output_directory: str = "exports"
    include_timestamp: bool = True
    custom_filename: str = ""
    compress_output: bool = False


@dataclass
class UIConfig:
    """User interface configuration"""
    theme: str = "horror"  # horror, itachi, minimal
    show_quotes: bool = True
    show_progress: bool = True
    verbose_logging: bool = False
    quiet_mode: bool = False


class Config:
    """Main configuration manager"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.console = Console()
        
        # Set config file path
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = Path("config") / "config.yaml"
        
        # Initialize configuration objects
        self.reddit = RedditConfig()
        self.scraping = ScrapingConfig()
        self.export = ExportConfig()
        self.ui = UIConfig()
        
        # Ensure config directory exists
        self.config_path.parent.mkdir(exist_ok=True)
        
        # Load existing configuration
        self.load()
    
    def load(self) -> bool:
        """Load configuration from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    if self.config_path.suffix.lower() == '.json':
                        config_data = json.load(f)
                    else:
                        config_data = yaml.safe_load(f)
                
                # Load Reddit config
                if 'reddit' in config_data:
                    reddit_data = config_data['reddit']
                    self.reddit = RedditConfig(**reddit_data)
                
                # Load Scraping config
                if 'scraping' in config_data:
                    scraping_data = config_data['scraping']
                    self.scraping = ScrapingConfig(**scraping_data)
                
                # Load Export config
                if 'export' in config_data:
                    export_data = config_data['export']
                    self.export = ExportConfig(**export_data)
                
                # Load UI config
                if 'ui' in config_data:
                    ui_data = config_data['ui']
                    self.ui = UIConfig(**ui_data)
                
                return True
        except Exception as e:
            self.console.print(f"[red]Error loading config: {str(e)}[/red]")
        
        return False
    
    def save(self) -> bool:
        """Save configuration to file"""
        try:
            config_data = {
                'reddit': asdict(self.reddit),
                'scraping': asdict(self.scraping),
                'export': asdict(self.export),
                'ui': asdict(self.ui)
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                if self.config_path.suffix.lower() == '.json':
                    json.dump(config_data, f, indent=2)
                else:
                    yaml.dump(config_data, f, default_flow_style=False, indent=2)
            
            return True
        except Exception as e:
            self.console.print(f"[red]Error saving config: {str(e)}[/red]")
            return False
    
    def is_configured(self) -> bool:
        """Check if basic configuration is complete"""
        return (
            bool(self.reddit.client_id) and 
            bool(self.reddit.client_secret) and
            bool(self.reddit.user_agent)
        )
    
    def validate_reddit_config(self) -> bool:
        """Validate Reddit API configuration"""
        required_fields = ['client_id', 'client_secret', 'user_agent']
        
        for field in required_fields:
            if not getattr(self.reddit, field):
                self.console.print(f"[red]Missing required Reddit config: {field}[/red]")
                return False
        
        return True
    
    def get_reddit_config_dict(self) -> Dict[str, str]:
        """Get Reddit configuration as dictionary for PRAW"""
        return {
            'client_id': self.reddit.client_id,
            'client_secret': self.reddit.client_secret,
            'user_agent': self.reddit.user_agent,
            'username': self.reddit.username,
            'password': self.reddit.password
        }
    
    def update_reddit_config(self, **kwargs):
        """Update Reddit configuration"""
        for key, value in kwargs.items():
            if hasattr(self.reddit, key):
                setattr(self.reddit, key, value)
    
    def update_scraping_config(self, **kwargs):
        """Update scraping configuration"""
        for key, value in kwargs.items():
            if hasattr(self.scraping, key):
                setattr(self.scraping, key, value)
    
    def update_export_config(self, **kwargs):
        """Update export configuration"""
        for key, value in kwargs.items():
            if hasattr(self.export, key):
                setattr(self.export, key, value)
    
    def update_ui_config(self, **kwargs):
        """Update UI configuration"""
        for key, value in kwargs.items():
            if hasattr(self.ui, key):
                setattr(self.ui, key, value)
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.reddit = RedditConfig()
        self.scraping = ScrapingConfig()
        self.export = ExportConfig()
        self.ui = UIConfig()
    
    def export_config(self, filepath: str) -> bool:
        """Export configuration to a specific file"""
        try:
            config_data = {
                'reddit': asdict(self.reddit),
                'scraping': asdict(self.scraping),
                'export': asdict(self.export),
                'ui': asdict(self.ui)
            }
            
            export_path = Path(filepath)
            export_path.parent.mkdir(exist_ok=True)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                if export_path.suffix.lower() == '.json':
                    json.dump(config_data, f, indent=2)
                else:
                    yaml.dump(config_data, f, default_flow_style=False, indent=2)
            
            return True
        except Exception as e:
            self.console.print(f"[red]Error exporting config: {str(e)}[/red]")
            return False
    
    def import_config(self, filepath: str) -> bool:
        """Import configuration from a specific file"""
        try:
            import_path = Path(filepath)
            if not import_path.exists():
                self.console.print(f"[red]Config file not found: {filepath}[/red]")
                return False
            
            with open(import_path, 'r', encoding='utf-8') as f:
                if import_path.suffix.lower() == '.json':
                    config_data = json.load(f)
                else:
                    config_data = yaml.safe_load(f)
            
            # Update configurations
            if 'reddit' in config_data:
                self.reddit = RedditConfig(**config_data['reddit'])
            if 'scraping' in config_data:
                self.scraping = ScrapingConfig(**config_data['scraping'])
            if 'export' in config_data:
                self.export = ExportConfig(**config_data['export'])
            if 'ui' in config_data:
                self.ui = UIConfig(**config_data['ui'])
            
            return True
        except Exception as e:
            self.console.print(f"[red]Error importing config: {str(e)}[/red]")
            return False
    
    def get_output_directory(self) -> Path:
        """Get the output directory path"""
        output_dir = Path(self.export.output_directory)
        output_dir.mkdir(exist_ok=True)
        return output_dir
    
    def get_logs_directory(self) -> Path:
        """Get the logs directory path"""
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        return logs_dir
    
    def display_current_config(self):
        """Display current configuration"""
        from rich.table import Table
        from rich.panel import Panel
        
        # Reddit Config Table
        reddit_table = Table(title="Reddit API Configuration", show_header=True, header_style="bold red")
        reddit_table.add_column("Setting", style="cyan")
        reddit_table.add_column("Value", style="white")
        
        reddit_table.add_row("Client ID", self.reddit.client_id[:10] + "..." if self.reddit.client_id else "Not Set")
        reddit_table.add_row("Client Secret", "***" if self.reddit.client_secret else "Not Set")
        reddit_table.add_row("User Agent", self.reddit.user_agent)
        reddit_table.add_row("Username", self.reddit.username or "Not Set")
        
        # Scraping Config Table
        scraping_table = Table(title="Scraping Configuration", show_header=True, header_style="bold red")
        scraping_table.add_column("Setting", style="cyan")
        scraping_table.add_column("Value", style="white")
        
        scraping_table.add_row("Default Limit", str(self.scraping.default_limit))
        scraping_table.add_row("Default Depth", str(self.scraping.default_depth))
        scraping_table.add_row("Include Comments", str(self.scraping.include_comments))
        scraping_table.add_row("Enable Sentiment", str(self.scraping.enable_sentiment))
        scraping_table.add_row("Remove Duplicates", str(self.scraping.remove_duplicates))
        
        # Export Config Table
        export_table = Table(title="Export Configuration", show_header=True, header_style="bold red")
        export_table.add_column("Setting", style="cyan")
        export_table.add_column("Value", style="white")
        
        export_table.add_row("Default Format", self.export.default_format.upper())
        export_table.add_row("Output Directory", self.export.output_directory)
        export_table.add_row("Include Timestamp", str(self.export.include_timestamp))
        export_table.add_row("Compress Output", str(self.export.compress_output))
        
        # Display tables
        self.console.print(reddit_table)
        self.console.print()
        self.console.print(scraping_table)
        self.console.print()
        self.console.print(export_table)
