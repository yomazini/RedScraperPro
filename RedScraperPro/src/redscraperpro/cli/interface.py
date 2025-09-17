"""
CLI Interface for RedScraperPro
🩸 Interactive command-line interface with horror/Itachi theme 🩸
"""

import sys
import time
from typing import Optional, Dict, Any
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns

from redscraperpro.utils.config import Config
from redscraperpro.utils.logger import Logger
from redscraperpro.utils.ascii_art import ASCIIArt
from redscraperpro.utils.quotes import Quotes
from redscraperpro.utils.progress import ProgressTracker


class CLIInterface:
    """Main CLI interface for RedScraperPro"""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.console = Console()
        self.ascii_art = ASCIIArt()
        self.quotes = Quotes()
        self.progress_tracker = ProgressTracker(self.console)
        
        # Menu options
        self.main_menu_options = {
            "1": ("🔍 Scrape by Keyword", self._scrape_by_keyword),
            "2": ("🏘️  Scrape Subreddit", self._scrape_subreddit),
            "3": ("👤 Scrape User Profile", self._scrape_user),
            "4": ("📝 Scrape Specific Post", self._scrape_post),
            "5": ("📊 View Statistics", self._view_statistics),
            "6": ("⚙️  Configuration", self._configuration_menu),
            "7": ("📖 Help & Documentation", self._help_menu),
            "8": ("🚪 Exit", self._exit_application)
        }
    
    def run_interactive_mode(self):
        """Run the interactive CLI mode"""
        self.logger.session_start("interactive_mode")
        
        try:
            while True:
                self._display_main_menu()
                choice = self._get_menu_choice()
                
                if choice in self.main_menu_options:
                    option_name, option_func = self.main_menu_options[choice]
                    self.logger.info(f"User selected: {option_name}")
                    
                    try:
                        option_func()
                    except KeyboardInterrupt:
                        self.console.print("\n[yellow]Operation cancelled by user.[/yellow]")
                        continue
                    except Exception as e:
                        self.logger.error(f"Error in {option_name}: {str(e)}")
                        self.ascii_art.display_error(f"An error occurred: {str(e)}")
                        continue
                else:
                    self.ascii_art.display_warning("Invalid choice. Please try again.")
                
                # Pause before showing menu again
                if choice != "8":  # Don't pause before exit
                    self.console.print("\n[dim]Press Enter to continue...[/dim]", end="")
                    input()
        
        except KeyboardInterrupt:
            self._exit_application()
    
    def run_command_mode(self, args):
        self.logger.session_start(f"command_mode_{args.mode}")
        try:
            # Import scraper here to avoid circular imports
            from redscraperpro.scraper.reddit_scraper import RedditScraper
            
            # Create scraper instance
            scraper = RedditScraper(self.config, self.logger, self.progress_tracker)
            
            # Determine scraping parameters
            if args.mode == "keyword":
                if not args.query:
                    self.ascii_art.display_error("Keyword mode requires --query parameter")
                    sys.exit(1)
                results = scraper.scrape_by_keyword(
                    query=args.query,
                    limit=args.limit,
                    include_comments=args.include_comments,
                    comment_depth=args.depth
                )
            
            elif args.mode == "subreddit":
                if not args.target:
                    self.ascii_art.display_error("Subreddit mode requires --target parameter")
                    sys.exit(1)
                results = scraper.scrape_subreddit(
                    subreddit_name=args.target,
                    limit=args.limit,
                    include_comments=args.include_comments,
                    comment_depth=args.depth
                )
            
            elif args.mode == "user":
                if not args.target:
                    self.ascii_art.display_error("User mode requires --target parameter")
                    sys.exit(1)
                results = scraper.scrape_user(
                    username=args.target,
                    limit=args.limit,
                    include_comments=args.include_comments
                )
            
            elif args.mode == "post":
                if not args.post_id:
                    self.ascii_art.display_error("Post mode requires --post-id parameter")
                    sys.exit(1)
                results = scraper.scrape_post(
                    post_id=args.post_id,
                    include_comments=args.include_comments,
                    comment_depth=args.depth
                )
            
            # Process results
            if results:
                # Apply sentiment analysis if requested
                if args.sentiment:
                    results = scraper.add_sentiment_analysis(results)
                
                # Remove duplicates if requested
                if args.no_duplicates:
                    results = scraper.remove_duplicates(results)
                
                # Export results
                output_filename = args.output or f"{args.mode}_{args.target or args.query or args.post_id}"
                exported_file = scraper.export_data(results, args.export, output_filename)
                
                self.ascii_art.display_success(f"Data exported to: {exported_file}")
            else:
                self.ascii_art.display_warning("No data was scraped.")
        
        except Exception as e:
            self.logger.error(f"Command mode error: {str(e)}")
            self.ascii_art.display_error(f"Scraping failed: {str(e)}")
            sys.exit(1)
    
    def _display_main_menu(self):
        """Display the main menu"""
        self.console.clear()
        self.ascii_art.display_header()
        
        # Display random quote
        if self.config.ui.show_quotes:
            self.quotes.display_random_quote(style="simple")
            self.console.print()
        
        # Create menu table
        menu_table = Table(title="🩸 Main Menu 🩸", show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("Option", style="bold red", width=3)
        menu_table.add_column("Description", style="white")
        
        for key, (description, _) in self.main_menu_options.items():
            menu_table.add_row(key, description)
        
        menu_panel = Panel(
            menu_table,
            style="red",
            border_style="red",
            padding=(1, 2)
        )
        self.console.print(menu_panel)
        self.console.print()
    
    def _get_menu_choice(self) -> str:
        """Get user menu choice"""
        return Prompt.ask(
            self.ascii_art.get_themed_prompt("Select an option"),
            choices=list(self.main_menu_options.keys()),
            show_choices=False
        )
    
    def _scrape_by_keyword(self):
        """Handle keyword scraping"""
        self.ascii_art.display_menu_header("Keyword Scraping")
        
        # Get parameters
        query = Prompt.ask("🔍 Enter search keyword(s)")
        limit = IntPrompt.ask("📊 Number of posts to scrape", default=self.config.scraping.default_limit)
        include_comments = Confirm.ask("💬 Include comments?", default=self.config.scraping.include_comments)
        
        comment_depth = 1
        if include_comments:
            comment_depth = IntPrompt.ask("🔍 Comment depth level", default=self.config.scraping.default_depth)
        
        sentiment_analysis = Confirm.ask("🧠 Enable sentiment analysis?", default=self.config.scraping.enable_sentiment)
        
        # Start scraping
        self._execute_scraping("keyword", query, {
            "query": query,
            "limit": limit,
            "include_comments": include_comments,
            "comment_depth": comment_depth,
            "sentiment_analysis": sentiment_analysis
        })
    
    def _scrape_subreddit(self):
        """Handle subreddit scraping"""
        self.ascii_art.display_menu_header("Subreddit Scraping")
        
        # Get parameters
        subreddit = Prompt.ask("🏘️  Enter subreddit name (without r/)")
        limit = IntPrompt.ask("📊 Number of posts to scrape", default=self.config.scraping.default_limit)
        include_comments = Confirm.ask("💬 Include comments?", default=self.config.scraping.include_comments)
        
        comment_depth = 1
        if include_comments:
            comment_depth = IntPrompt.ask("🔍 Comment depth level", default=self.config.scraping.default_depth)
        
        sentiment_analysis = Confirm.ask("🧠 Enable sentiment analysis?", default=self.config.scraping.enable_sentiment)
        
        # Start scraping
        self._execute_scraping("subreddit", subreddit, {
            "subreddit_name": subreddit,
            "limit": limit,
            "include_comments": include_comments,
            "comment_depth": comment_depth,
            "sentiment_analysis": sentiment_analysis
        })
    
    def _scrape_user(self):
        """Handle user profile scraping"""
        self.ascii_art.display_menu_header("User Profile Scraping")
        
        # Get parameters
        username = Prompt.ask("👤 Enter username (without u/)")
        limit = IntPrompt.ask("📊 Number of posts to scrape", default=self.config.scraping.default_limit)
        include_comments = Confirm.ask("💬 Include comments?", default=self.config.scraping.include_comments)
        sentiment_analysis = Confirm.ask("🧠 Enable sentiment analysis?", default=self.config.scraping.enable_sentiment)
        
        # Start scraping
        self._execute_scraping("user", username, {
            "username": username,
            "limit": limit,
            "include_comments": include_comments,
            "sentiment_analysis": sentiment_analysis
        })
    
    def _scrape_post(self):
        """Handle specific post scraping"""
        self.ascii_art.display_menu_header("Specific Post Scraping")
        
        # Get parameters
        post_id = Prompt.ask("📝 Enter post ID or URL")
        
        # Extract post ID from URL if needed
        if "reddit.com" in post_id:
            # Extract post ID from Reddit URL
            import re
            match = re.search(r'/comments/([a-zA-Z0-9]+)/', post_id)
            if match:
                post_id = match.group(1)
            else:
                self.ascii_art.display_error("Could not extract post ID from URL")
                return
        
        include_comments = Confirm.ask("💬 Include comments?", default=True)
        comment_depth = IntPrompt.ask("🔍 Comment depth level", default=self.config.scraping.default_depth)
        sentiment_analysis = Confirm.ask("🧠 Enable sentiment analysis?", default=self.config.scraping.enable_sentiment)
        
        # Start scraping
        self._execute_scraping("post", post_id, {
            "post_id": post_id,
            "include_comments": include_comments,
            "comment_depth": comment_depth,
            "sentiment_analysis": sentiment_analysis
        })
    
    def _execute_scraping(self, mode: str, target: str, params: Dict[str, Any]):
        """Execute the scraping operation"""
        try:
            # Import scraper here to avoid circular imports
            from redscraperpro.scraper.reddit_scraper import RedditScraper
            
            # Create scraper instance
            scraper = RedditScraper(self.config, self.logger, self.progress_tracker)
            
            # Display scraping start
            self.ascii_art.display_progress_header(mode, target)
            
            # Execute scraping based on mode
            results = None
            if mode == "keyword":
                results = scraper.scrape_by_keyword(**params)
            elif mode == "subreddit":
                results = scraper.scrape_subreddit(**params)
            elif mode == "user":
                results = scraper.scrape_user(**params)
            elif mode == "post":
                results = scraper.scrape_post(**params)
            
            if results:
                # Apply sentiment analysis if requested
                if params.get("sentiment_analysis", False):
                    self.console.print("\n🧠 Performing sentiment analysis...")
                    results = scraper.add_sentiment_analysis(results)
                
                # Remove duplicates
                if self.config.scraping.remove_duplicates:
                    original_count = len(results)
                    results = scraper.remove_duplicates(results)
                    if len(results) < original_count:
                        self.logger.duplicate_removal(original_count, len(results))
                
                # Get export preferences
                self._handle_export(scraper, results, mode, target)
            else:
                self.ascii_art.display_warning("No data was scraped.")
        
        except Exception as e:
            self.logger.error(f"Scraping error: {str(e)}")
            self.ascii_art.display_error(f"Scraping failed: {str(e)}")
            self.quotes.display_error_quote()
    
    def _handle_export(self, scraper, results, mode: str, target: str):
        """Handle data export"""
        self.console.print("\n" + "="*60)
        self.console.print("[bold green]📤 Export Options[/bold green]")
        
        # Export format selection
        format_choices = ["csv", "xlsx", "json", "txt"]
        export_format = Prompt.ask(
            "📁 Choose export format",
            choices=format_choices,
            default=self.config.export.default_format,
            show_choices=True
        )
        
        # Filename
        default_filename = f"{mode}_{target}_{int(time.time())}"
        filename = Prompt.ask(
            "📝 Enter filename (without extension)",
            default=default_filename
        )
        
        # Export data
        try:
            exported_file = scraper.export_data(results, export_format, filename)
            
            # Display completion summary
            stats = self.progress_tracker.get_stats()
            stats['format'] = export_format.upper()
            stats['filename'] = exported_file
            
            self.ascii_art.display_completion_summary(stats)
            
            # Display final quote
            self.quotes.display_completion_quote()
            
        except Exception as e:
            self.logger.error(f"Export error: {str(e)}")
            self.ascii_art.display_error(f"Export failed: {str(e)}")
    
    def _view_statistics(self):
        """Display statistics and logs"""
        self.ascii_art.display_menu_header("Statistics & Logs")
        
        # Display current session stats
        stats = self.progress_tracker.get_stats()
        
        stats_table = Table(title="📊 Current Session Statistics", show_header=True, header_style="bold red")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="white")
        
        for key, value in stats.items():
            if key not in ['start_time', 'end_time']:  # Skip timestamp fields for display
                stats_table.add_row(key.replace('_', ' ').title(), str(value))
        
        self.console.print(stats_table)
        self.console.print()
        
        # Display log statistics
        self.logger.display_log_stats()
        
        # Options
        if Confirm.ask("\n🧹 Clean up old log files?"):
            removed = self.logger.cleanup_old_logs()
            if removed > 0:
                self.ascii_art.display_success(f"Removed {removed} old log files")
            else:
                self.ascii_art.display_info("No old log files to remove")
    
    def _configuration_menu(self):
        """Display configuration menu"""
        self.ascii_art.display_menu_header("Configuration")
        
        config_options = {
            "1": "View Current Configuration",
            "2": "Modify Reddit API Settings",
            "3": "Modify Scraping Preferences", 
            "4": "Modify Export Settings",
            "5": "Modify UI Preferences",
            "6": "Reset to Defaults",
            "7": "Export Configuration",
            "8": "Import Configuration",
            "9": "Back to Main Menu"
        }
        
        # Display options
        for key, description in config_options.items():
            self.console.print(f"[red]{key}[/red]. {description}")
        
        choice = Prompt.ask(
            self.ascii_art.get_themed_prompt("Select option"),
            choices=list(config_options.keys()),
            show_choices=False
        )
        
        if choice == "1":
            self.config.display_current_config()
        elif choice == "2":
            self._modify_reddit_config()
        elif choice == "3":
            self._modify_scraping_config()
        elif choice == "4":
            self._modify_export_config()
        elif choice == "5":
            self._modify_ui_config()
        elif choice == "6":
            if Confirm.ask("⚠️  Reset all settings to defaults?"):
                self.config.reset_to_defaults()
                self.config.save()
                self.ascii_art.display_success("Configuration reset to defaults")
        elif choice == "7":
            filepath = Prompt.ask("📤 Export path", default="config_backup.yaml")
            if self.config.export_config(filepath):
                self.ascii_art.display_success(f"Configuration exported to: {filepath}")
        elif choice == "8":
            filepath = Prompt.ask("📥 Import path")
            if self.config.import_config(filepath):
                self.ascii_art.display_success("Configuration imported successfully")
        # Choice 9 returns to main menu
    
    def _modify_reddit_config(self):
        """Modify Reddit API configuration"""
        self.console.print("[bold red]🔧 Reddit API Configuration[/bold red]")
        
        # Show current values and allow modification
        client_id = Prompt.ask("Client ID", default=self.config.reddit.client_id)
        client_secret = Prompt.ask("Client Secret", password=True, default=self.config.reddit.client_secret)
        user_agent = Prompt.ask("User Agent", default=self.config.reddit.user_agent)
        username = Prompt.ask("Username (optional)", default=self.config.reddit.username)
        password = Prompt.ask("Password (optional)", password=True, default=self.config.reddit.password)
        
        self.config.update_reddit_config(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )
        
        if self.config.save():
            self.ascii_art.display_success("Reddit configuration updated")
    
    def _modify_scraping_config(self):
        """Modify scraping configuration"""
        self.console.print("[bold red]🔧 Scraping Configuration[/bold red]")
        
        default_limit = IntPrompt.ask("Default limit", default=self.config.scraping.default_limit)
        default_depth = IntPrompt.ask("Default depth", default=self.config.scraping.default_depth)
        include_comments = Confirm.ask("Include comments", default=self.config.scraping.include_comments)
        enable_sentiment = Confirm.ask("Enable sentiment", default=self.config.scraping.enable_sentiment)
        remove_duplicates = Confirm.ask("Remove duplicates", default=self.config.scraping.remove_duplicates)
        
        self.config.update_scraping_config(
            default_limit=default_limit,
            default_depth=default_depth,
            include_comments=include_comments,
            enable_sentiment=enable_sentiment,
            remove_duplicates=remove_duplicates
        )
        
        if self.config.save():
            self.ascii_art.display_success("Scraping configuration updated")
    
    def _modify_export_config(self):
        """Modify export configuration"""
        self.console.print("[bold red]🔧 Export Configuration[/bold red]")
        
        default_format = Prompt.ask("Default format", choices=["csv", "xlsx", "json", "txt"], default=self.config.export.default_format)
        output_directory = Prompt.ask("Output directory", default=self.config.export.output_directory)
        include_timestamp = Confirm.ask("Include timestamp", default=self.config.export.include_timestamp)
        compress_output = Confirm.ask("Compress output", default=self.config.export.compress_output)
        
        self.config.update_export_config(
            default_format=default_format,
            output_directory=output_directory,
            include_timestamp=include_timestamp,
            compress_output=compress_output
        )
        
        if self.config.save():
            self.ascii_art.display_success("Export configuration updated")
    
    def _modify_ui_config(self):
        """Modify UI configuration"""
        self.console.print("[bold red]🔧 UI Configuration[/bold red]")
        
        theme = Prompt.ask("Theme", choices=["horror", "itachi", "minimal"], default=self.config.ui.theme)
        show_quotes = Confirm.ask("Show quotes", default=self.config.ui.show_quotes)
        show_progress = Confirm.ask("Show progress", default=self.config.ui.show_progress)
        verbose_logging = Confirm.ask("Verbose logging", default=self.config.ui.verbose_logging)
        
        self.config.update_ui_config(
            theme=theme,
            show_quotes=show_quotes,
            show_progress=show_progress,
            verbose_logging=verbose_logging
        )
        
        if self.config.save():
            self.ascii_art.display_success("UI configuration updated")
    
    def _help_menu(self):
        """Display help and documentation"""
        self.ascii_art.display_menu_header("Help & Documentation")
        
        help_panel = Panel(
            "[bold red]📖 RedScraperPro Documentation[/bold red]\n\n"
            "[white]🔗 Links:[/white]\n"
            "• GitHub Repository: [link]https://github.com/yomazini/RedScraperPro[/link]\n"
            "• Full Documentation: [link]https://github.com/yomazini/RedScraperPro/blob/master/fullRedscrapperprohowtouse.pdf[/link]\n"
            "• Issue Tracker: [link]https://github.com/yomazini/RedScraperPro/issues[/link]\n"
            "• LinkedIn: [link]https://linkedin.com/in/yomazini[/link]\n\n"
            "[white]📋 Quick Commands:[/white]\n"
            "• Interactive Mode: [cyan]python src/main.py[/cyan]\n"
            "• Keyword Scraping: [cyan]python src/main.py --mode keyword --query \"python\"[/cyan]\n"
            "• Subreddit Scraping: [cyan]python src/main.py --mode subreddit --target programming[/cyan]\n"
            "• User Scraping: [cyan]python src/main.py --mode user --target username[/cyan]\n"
            "• Configuration: [cyan]python src/main.py --setup[/cyan]\n\n"
            "[white]🆘 Support:[/white]\n"
            "For issues, questions, or contributions, please visit our GitHub repository.",
            style="blue",
            border_style="blue"
        )
        self.console.print(help_panel)
    
    def _exit_application(self):
        """Exit the application gracefully"""
        self.ascii_art.display_separator("blood")
        
        exit_panel = Panel(
            "[bold red]🩸 FAREWELL, DATA SEEKER 🩸[/bold red]\n\n"
            "Thank you for using RedScraperPro!\n\n"
            "[dim italic]\"The truth will set you free, but first it will piss you off.\" - Gloria Steinem[/dim italic]\n\n"
            "[white]Remember:[/white]\n"
            "• Use data responsibly and ethically\n"
            "• Respect Reddit's Terms of Service\n"
            "• Share knowledge, not just data\n\n"
            "[yellow]🌟 Star us on GitHub: https://github.com/yomazini/RedScraperPro[/yellow]",
            style="red",
            border_style="red"
        )
        self.console.print(exit_panel)
        
        self.logger.info("Application exited by user")
        sys.exit(0)
