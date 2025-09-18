"""
ASCII Art and Visual Themes for RedScraperPro
🩸 Horror/Itachi Uchiha Aesthetic 🩸
"""

import random
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align


class ASCIIArt:
    """Handles ASCII art and visual themes"""
    
    def __init__(self):
        self.console = Console()
        
        # Main logo
        self.logo = """
██████╗ ███████╗██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ ██████╗ ██████╗  ██████╗ 
██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔═══██╗
██████╔╝█████╗  ██║  ██║███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝██████╔╝██████╔╝██║   ██║
██╔══██╗██╔══╝  ██║  ██║╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗██╔═══╝ ██╔══██╗██║   ██║
██║  ██║███████╗██████╔╝███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║██║     ██║  ██║╚██████╔╝
╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
        """
        
        # Horror/Itachi themed elements
        self.sharingan = """
        ⚫⚪⚫
       ⚪🔴⚪
        ⚫⚪⚫
        """
        
        self.crow = """
    🐦‍⬛
   /   \\
  /     \\
 /       \\
        """
        
        self.blood_drop = "🩸"
        self.moon = "🌙"
        self.kunai = "🗡️"
        
        # Themed separators
        self.separators = [
            "═" * 80,
            "🩸" + "═" * 78 + "🩸",
            "🌙" + "─" * 78 + "🌙",
            "⚫" + "━" * 78 + "⚫",
        ]
    
    def display_header(self):
        """Display the main header with logo and theme"""
        # Clear screen effect
        self.console.clear()
        
        # Display logo in red
        logo_text = Text(self.logo, style="bold red")
        self.console.print(Align.center(logo_text))
        
        # Subtitle
        subtitle = Text("🩸 The Ultimate Reddit Scraping CLI Tool 🩸", style="bold white")
        self.console.print(Align.center(subtitle))
        
        # Philosophical quote
        quote = Text("\"In the darkness of data, we find the light of knowledge\"", style="italic dim white")
        self.console.print(Align.center(quote))
        
        # Separator
        separator = Text(random.choice(self.separators), style="red")
        self.console.print(Align.center(separator))
        
        # Educational notice
        notice = Panel(
            "[bold yellow]⚠️  EDUCATIONAL PURPOSE ONLY ⚠️[/bold yellow]\n\n"
            "This tool is designed for educational purposes, research, and legitimate data analysis only.\n"
            "Please ensure you comply with Reddit's Terms of Service, API guidelines, and respect rate limits.\n"
            "Always use this tool responsibly and ethically.\n\n"
            "[dim]GitHub: https://github.com/yomazini/RedScraperPro[/dim]\n"
            "[dim]LinkedIn: https://linkedin.com/in/youssef-mazini[/dim]",
            style="red",
            border_style="red"
        )
        self.console.print(notice)
        self.console.print()
    
    def display_separator(self, style="default"):
        """Display a themed separator"""
        if style == "blood":
            sep = "🩸" + "═" * 78 + "🩸"
        elif style == "moon":
            sep = "🌙" + "─" * 78 + "🌙"
        elif style == "sharingan":
            sep = "⚫" + "━" * 78 + "⚫"
        else:
            sep = random.choice(self.separators)
        
        separator_text = Text(sep, style="red")
        self.console.print(Align.center(separator_text))
    
    def display_loading_animation(self, text="Loading"):
        """Display a themed loading animation"""
        from rich.spinner import Spinner
        
        spinner_styles = ["dots", "dots2", "dots3", "dots4", "dots5", "dots6", "dots7", "dots8", "dots9", "dots10", "dots11", "dots12"]
        spinner = Spinner(random.choice(spinner_styles), text=f"🩸 {text}...", style="red")
        
        return spinner
    
    def display_success(self, message):
        """Display success message with theme"""
        success_text = Text(f"✅ {message}", style="bold green")
        self.console.print(success_text)
    
    def display_error(self, message):
        """Display error message with theme"""
        error_text = Text(f"❌ {message}", style="bold red")
        self.console.print(error_text)
    
    def display_warning(self, message):
        """Display warning message with theme"""
        warning_text = Text(f"⚠️  {message}", style="bold yellow")
        self.console.print(warning_text)
    
    def display_info(self, message):
        """Display info message with theme"""
        info_text = Text(f"ℹ️  {message}", style="bold blue")
        self.console.print(info_text)
    
    def display_progress_header(self, mode, target):
        """Display progress header for scraping"""
        header = Panel(
            f"[bold red]🕷️  SCRAPING IN PROGRESS 🕷️[/bold red]\n\n"
            f"[white]Mode:[/white] [yellow]{mode.upper()}[/yellow]\n"
            f"[white]Target:[/white] [cyan]{target}[/cyan]\n"
            f"[white]Time:[/white] [green]{self._get_current_time()}[/green]\n\n"
            f"[dim italic]\"The truth will set you free, but first it will piss you off.\" - Gloria Steinem[/dim italic]",
            style="red",
            border_style="red"
        )
        self.console.print(header)
    
    def display_completion_summary(self, stats):
        """Display completion summary with stats"""
        summary = Panel(
            f"[bold green]🎯 SCRAPING COMPLETED 🎯[/bold green]\n\n"
            f"[white]Posts Scraped:[/white] [yellow]{stats.get('posts', 0)}[/yellow]\n"
            f"[white]Comments Scraped:[/white] [yellow]{stats.get('comments', 0)}[/yellow]\n"
            f"[white]Total Items:[/white] [yellow]{stats.get('total', 0)}[/yellow]\n"
            f"[white]Export Format:[/white] [cyan]{stats.get('format', 'N/A')}[/cyan]\n"
            f"[white]Output File:[/white] [green]{stats.get('filename', 'N/A')}[/green]\n\n"
            f"[dim italic]\"In the end, we will remember not the words of our enemies, but the silence of our friends.\" - Martin Luther King Jr.[/dim italic]",
            style="green",
            border_style="green"
        )
        self.console.print(summary)
    
    def display_menu_header(self, title):
        """Display menu header with theme"""
        header = Panel(
            f"[bold red]{self.blood_drop} {title.upper()} {self.blood_drop}[/bold red]",
            style="red",
            border_style="red"
        )
        self.console.print(header)
    
    def _get_current_time(self):
        """Get current time formatted"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def display_sharingan(self):
        """Display Sharingan ASCII art"""
        sharingan_text = Text(self.sharingan, style="bold red")
        self.console.print(Align.center(sharingan_text))
    
    def display_crow(self):
        """Display crow ASCII art"""
        crow_text = Text(self.crow, style="bold black")
        self.console.print(Align.center(crow_text))
    
    def get_themed_prompt(self, message):
        """Get a themed prompt message"""
        return f"🩸 {message}: "
