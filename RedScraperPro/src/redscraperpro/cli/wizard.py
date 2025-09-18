"""
Configuration Wizard for RedScraperPro
🩸 Interactive setup for first-time users 🩸
"""

import os
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from redscraperpro.utils.config import Config
from redscraperpro.utils.ascii_art import ASCIIArt
from redscraperpro.utils.quotes import Quotes


class ConfigWizard:
    """Interactive configuration wizard"""
    
    def __init__(self, config: Config):
        self.config = config
        self.console = Console()
        self.ascii_art = ASCIIArt()
        self.quotes = Quotes()
    
    def run(self):
        """Run the complete configuration wizard"""
        self.ascii_art.display_header()
        
        # Welcome message
        welcome_panel = Panel(
            "[bold red]🩸 WELCOME TO REDSCRAPERPRO CONFIGURATION 🩸[/bold red]\n\n"
            "This wizard will guide you through the initial setup process.\n"
            "You'll need to configure your Reddit API credentials and preferences.\n\n"
            "[yellow]⚠️  You'll need Reddit API credentials to continue.[/yellow]\n"
            "[dim]If you don't have them yet, visit: https://www.reddit.com/prefs/apps[/dim]",
            style="red",
            border_style="red"
        )
        self.console.print(welcome_panel)
        self.console.print()
        
        # Display a motivational quote
        self.quotes.display_random_quote(category="stoic", style="panel")
        self.console.print()
        
        try:
            # Step 1: Reddit API Configuration
            self._configure_reddit_api()
            
            # Step 2: Scraping Preferences
            self._configure_scraping_preferences()
            
            # Step 3: Export Settings
            self._configure_export_settings()
            
            # Step 4: UI Preferences
            self._configure_ui_preferences()
            
            # Step 5: Save Configuration
            self._save_configuration()
            
            # Step 6: Test Configuration (Optional)
            if Confirm.ask("\n🧪 Would you like to test your Reddit API configuration?"):
                self._test_reddit_connection()
            
            # Completion message
            self._display_completion_message()
            
        except KeyboardInterrupt:
            self.console.print("\n\n[red]Configuration cancelled by user.[/red]")
            sys.exit(0)
        except Exception as e:
            self.console.print(f"\n\n[red]Configuration error: {str(e)}[/red]")
            sys.exit(1)
    
    def _configure_reddit_api(self):
        """Configure Reddit API settings"""
        self.ascii_art.display_menu_header("Reddit API Configuration")
        
        # Display instructions
        instructions = Panel(
            "[bold yellow]📋 Reddit API Setup Instructions[/bold yellow]\n\n"
            "1. Go to: [link]https://www.reddit.com/prefs/apps[/link]\n"
            "2. Click 'Create App' or 'Create Another App'\n"
            "3. Choose 'script' as the application type\n"
            "4. Fill in the required information:\n"
            "   • Name: RedScraperPro (or any name you prefer)\n"
            "   • Description: Reddit scraping tool for educational purposes\n"
            "   • Redirect URI: http://localhost:8080 (required but not used)\n\n"
            "5. After creation, note down:\n"
            "   • Client ID (under the app name, looks like: abc123def456)\n"
            "   • Client Secret (the 'secret' field)\n\n"
            "[red]📖 Detailed Guide:[/red] [link]https://github.com/yomazini/RedScraperPro/blob/master/RedScraperPro/DOCUMENTATION.md[/link]",
            style="yellow",
            border_style="yellow"
        )
        self.console.print(instructions)
        self.console.print()
        
        # Get Reddit credentials
        client_id = Prompt.ask(
            "🔑 Enter your Reddit Client ID",
            default=self.config.reddit.client_id
        ).strip()
        
        client_secret = Prompt.ask(
            "🔐 Enter your Reddit Client Secret",
            password=True,
            default=self.config.reddit.client_secret
        ).strip()
        
        # Get user agent
        default_user_agent = f"RedScraperPro:v1.0.0 (by /u/{os.getenv('USER', 'user')})"
        user_agent = Prompt.ask(
            "🤖 Enter your User Agent",
            default=self.config.reddit.user_agent or default_user_agent
        ).strip()
        
        # Optional: Reddit username and password for authenticated requests
        use_auth = Confirm.ask("\n🔐 Do you want to use Reddit username/password for authenticated requests? (Optional)")
        
        username = ""
        password = ""
        if use_auth:
            username = Prompt.ask(
                "👤 Enter your Reddit username",
                default=self.config.reddit.username
            ).strip()
            
            password = Prompt.ask(
                "🔒 Enter your Reddit password",
                password=True,
                default=self.config.reddit.password
            ).strip()
        
        # Update configuration
        self.config.update_reddit_config(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )
        
        self.ascii_art.display_success("Reddit API configuration completed!")
        self.console.print()
    
    def _configure_scraping_preferences(self):
        """Configure scraping preferences"""
        self.ascii_art.display_menu_header("Scraping Preferences")
        
        # Default limits
        default_limit = IntPrompt.ask(
            "📊 Default number of items to scrape per session",
            default=self.config.scraping.default_limit,
            show_default=True
        )
        
        # Comment depth
        default_depth = IntPrompt.ask(
            "🔍 Default comment depth level (1=direct replies, 2=replies to replies, etc.)",
            default=self.config.scraping.default_depth,
            show_default=True
        )
        
        # Include comments by default
        include_comments = Confirm.ask(
            "💬 Include comments by default?",
            default=self.config.scraping.include_comments
        )
        
        # Sentiment analysis
        enable_sentiment = Confirm.ask(
            "🧠 Enable sentiment analysis by default? (Lightweight analysis)",
            default=self.config.scraping.enable_sentiment
        )
        
        # Duplicate removal
        remove_duplicates = Confirm.ask(
            "🧹 Remove duplicate entries by default?",
            default=self.config.scraping.remove_duplicates
        )
        
        # Rate limiting
        rate_limit_delay = float(Prompt.ask(
            "⏱️  Rate limit delay between requests (seconds)",
            default=str(self.config.scraping.rate_limit_delay),
            show_default=True
        ))
        
        # Update configuration
        self.config.update_scraping_config(
            default_limit=default_limit,
            default_depth=default_depth,
            include_comments=include_comments,
            enable_sentiment=enable_sentiment,
            remove_duplicates=remove_duplicates,
            rate_limit_delay=rate_limit_delay
        )
        
        self.ascii_art.display_success("Scraping preferences configured!")
        self.console.print()
    
    def _configure_export_settings(self):
        """Configure export settings"""
        self.ascii_art.display_menu_header("Export Settings")
        
        # Default export format
        format_choices = ["csv", "xlsx", "json", "txt"]
        default_format = Prompt.ask(
            "📁 Default export format",
            choices=format_choices,
            default=self.config.export.default_format,
            show_choices=True
        )
        
        # Output directory
        output_directory = Prompt.ask(
            "📂 Output directory for exported files",
            default=self.config.export.output_directory,
            show_default=True
        )
        
        # Include timestamp in filenames
        include_timestamp = Confirm.ask(
            "🕐 Include timestamp in filenames?",
            default=self.config.export.include_timestamp
        )
        
        # Compress output
        compress_output = Confirm.ask(
            "🗜️  Compress output files? (ZIP format)",
            default=self.config.export.compress_output
        )
        
        # Update configuration
        self.config.update_export_config(
            default_format=default_format,
            output_directory=output_directory,
            include_timestamp=include_timestamp,
            compress_output=compress_output
        )
        
        self.ascii_art.display_success("Export settings configured!")
        self.console.print()
    
    def _configure_ui_preferences(self):
        """Configure UI preferences"""
        self.ascii_art.display_menu_header("User Interface Preferences")
        
        # Theme selection
        theme_choices = ["horror", "itachi", "minimal"]
        theme = Prompt.ask(
            "🎨 Choose your preferred theme",
            choices=theme_choices,
            default=self.config.ui.theme,
            show_choices=True
        )
        
        # Show quotes
        show_quotes = Confirm.ask(
            "💭 Show inspirational quotes during operation?",
            default=self.config.ui.show_quotes
        )
        
        # Show progress
        show_progress = Confirm.ask(
            "📊 Show detailed progress information?",
            default=self.config.ui.show_progress
        )
        
        # Verbose logging
        verbose_logging = Confirm.ask(
            "🔍 Enable verbose logging by default?",
            default=self.config.ui.verbose_logging
        )
        
        # Update configuration
        self.config.update_ui_config(
            theme=theme,
            show_quotes=show_quotes,
            show_progress=show_progress,
            verbose_logging=verbose_logging
        )
        
        self.ascii_art.display_success("UI preferences configured!")
        self.console.print()
    
    def _save_configuration(self):
        """Save the configuration"""
        self.ascii_art.display_menu_header("Saving Configuration")
        
        if self.config.save():
            self.ascii_art.display_success(f"Configuration saved to: {self.config.config_path}")
        else:
            self.ascii_art.display_error("Failed to save configuration!")
            raise Exception("Configuration save failed")
        
        self.console.print()
    
    def _test_reddit_connection(self):
        """Test Reddit API connection"""
        self.ascii_art.display_menu_header("Testing Reddit Connection")
        
        try:
            import praw
            
            # Create Reddit instance
            reddit_config = self.config.get_reddit_config_dict()
            reddit = praw.Reddit(**reddit_config)
            
            # Test connection by getting user info
            self.console.print("🧪 Testing Reddit API connection...")
            
            # Try to access Reddit
            user = reddit.user.me()
            if user:
                self.ascii_art.display_success(f"Connected as: {user.name}")
            else:
                # Try read-only access
                subreddit = reddit.subreddit("test")
                post_count = len(list(subreddit.hot(limit=1)))
                if post_count >= 0:
                    self.ascii_art.display_success("Read-only connection successful!")
                else:
                    raise Exception("Unable to access Reddit")
            
        except ImportError:
            self.ascii_art.display_warning("PRAW not installed. Install with: pip install praw")
        except Exception as e:
            self.ascii_art.display_error(f"Connection test failed: {str(e)}")
            self.console.print("\n[yellow]Don't worry! You can test the connection later.[/yellow]")
        
        self.console.print()
    
    def _display_completion_message(self):
        """Display completion message"""
        completion_panel = Panel(
            "[bold green]🎯 CONFIGURATION COMPLETED SUCCESSFULLY! 🎯[/bold green]\n\n"
            "Your RedScraperPro is now configured and ready to use!\n\n"
            "[white]Next steps:[/white]\n"
            "1. Run: [cyan]rsp[/cyan] or [cyan]redscraperpro[/cyan] to start scraping\n"
            "2. Use: [cyan]rsp --help[/cyan] for command options\n"
            "3. Check: [cyan]config/config.yaml[/cyan] to modify settings (or import a previous config in the main menu)\n\n"
            "[yellow]📖 Documentation:[/yellow] [link]https://github.com/yomazini/RedScraperPro[/link]\n"
            "[yellow]🆘 Support:[/yellow] [link]https://github.com/yomazini/RedScraperPro/issues[/link]",
            style="green",
            border_style="green"
        )
        self.console.print(completion_panel)
        
        # Display final quote
        self.quotes.display_completion_quote()
        
        # Display current configuration summary
        self.console.print("\n" + "="*80)
        self.console.print("[bold red]📋 Configuration Summary[/bold red]")
        self.config.display_current_config()
    
    def quick_setup(self):
        """Quick setup with minimal questions"""
        self.ascii_art.display_header()
        
        quick_panel = Panel(
            "[bold red]⚡ QUICK SETUP MODE ⚡[/bold red]\n\n"
            "This will set up RedScraperPro with minimal configuration.\n"
            "You can always run the full wizard later with: [cyan]rsp --setup[/cyan]",
            style="red",
            border_style="red"
        )
        self.console.print(quick_panel)
        self.console.print()
        
        # Only ask for essential Reddit API credentials
        client_id = Prompt.ask("🔑 Reddit Client ID").strip()
        client_secret = Prompt.ask("🔐 Reddit Client Secret", password=True).strip()
        
        # Use defaults for everything else
        default_user_agent = f"RedScraperPro:v1.0.0 (by /u/{os.getenv('USER', 'user')})"
        
        self.config.update_reddit_config(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=default_user_agent
        )
        
        if self.config.save():
            self.ascii_art.display_success("Quick setup completed!")
            self.console.print("\n[green]You're ready to start scraping![/green]")
            self.console.print("[dim]Run: rsp[/dim]")
        else:
            self.ascii_art.display_error("Setup failed!")
            sys.exit(1)
