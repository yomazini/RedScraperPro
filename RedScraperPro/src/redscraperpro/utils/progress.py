"""
Progress Tracking System for RedScraperPro
🩸 Real-time progress tracking with themed display 🩸
"""

import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from rich.console import Console
from rich.progress import Progress, TaskID, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


@dataclass
class ScrapingStats:
    """Statistics for scraping operations"""
    posts_scraped: int = 0
    comments_scraped: int = 0
    total_items: int = 0
    duplicates_removed: int = 0
    errors_encountered: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    current_target: str = ""
    mode: str = ""
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()
    
    @property
    def elapsed_time(self) -> timedelta:
        """Get elapsed time"""
        end = self.end_time or datetime.now()
        return end - self.start_time if self.start_time else timedelta(0)
    
    @property
    def items_per_second(self) -> float:
        """Get items per second rate"""
        elapsed = self.elapsed_time.total_seconds()
        return self.total_items / elapsed if elapsed > 0 else 0.0
    
    def finish(self):
        """Mark the operation as finished"""
        self.end_time = datetime.now()


class ProgressTracker:
    """Enhanced progress tracking with Rich integration"""
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.stats = ScrapingStats()
        self.progress: Optional[Progress] = None
        self.main_task: Optional[TaskID] = None
        self.sub_tasks: Dict[str, TaskID] = {}
        self.session_data: Dict[str, Any] = {}
        
        # Horror/Itachi themed elements
        self.blood_drop = "🩸"
        self.sharingan = "👁️"
        self.crow = "🐦‍⬛"
        self.kunai = "🗡️"
        self.moon = "🌙"
    
    def start_session(self, mode: str, target: str, total_expected: int = 0):
        """Start a new scraping session"""
        self.stats = ScrapingStats(
            mode=mode,
            current_target=target,
            start_time=datetime.now()
        )
        
        # Create progress display
        self.progress = Progress(
            SpinnerColumn(style="red"),
            TextColumn("[bold red]{task.description}"),
            BarColumn(bar_width=40, style="red", complete_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=self.console
        )
        
        # Start progress display
        self.progress.start()
        
        # Add main task
        self.main_task = self.progress.add_task(
            f"{self.blood_drop} Scraping {mode}: {target}",
            total=total_expected if total_expected > 0 else None
        )
        
        # Display session start
        self._display_session_start()
    
    def update_progress(self, advance: int = 1, description: Optional[str] = None):
        """Update main progress"""
        if self.progress and self.main_task is not None:
            if description:
                self.progress.update(self.main_task, description=f"{self.blood_drop} {description}")
            self.progress.advance(self.main_task, advance)
    
    def add_subtask(self, name: str, description: str, total: int = 0) -> Optional[TaskID]:
        """Add a subtask"""
        if self.progress:
            task_id = self.progress.add_task(
                f"{self.sharingan} {description}",
                total=total if total > 0 else None
            )
            self.sub_tasks[name] = task_id
            return task_id
        return None
    
    def update_subtask(self, name: str, advance: int = 1, description: Optional[str] = None):
        """Update a subtask"""
        if self.progress and name in self.sub_tasks:
            task_id = self.sub_tasks[name]
            if description:
                self.progress.update(task_id, description=f"{self.sharingan} {description}")
            self.progress.advance(task_id, advance)
    
    def complete_subtask(self, name: str):
        """Complete a subtask"""
        if self.progress and name in self.sub_tasks:
            task_id = self.sub_tasks[name]
            self.progress.update(task_id, completed=True)
            self.progress.remove_task(task_id)
            del self.sub_tasks[name]
    
    def increment_posts(self, count: int = 1):
        """Increment posts scraped count"""
        self.stats.posts_scraped += count
        self.stats.total_items += count
        self.update_progress(count)
    
    def increment_comments(self, count: int = 1):
        """Increment comments scraped count"""
        self.stats.comments_scraped += count
        self.stats.total_items += count
        self.update_progress(count)
    
    def increment_duplicates(self, count: int = 1):
        """Increment duplicates removed count"""
        self.stats.duplicates_removed += count
    
    def increment_errors(self, count: int = 1):
        """Increment errors encountered count"""
        self.stats.errors_encountered += count
    
    def set_total(self, total: int):
        """Set the total expected items"""
        if self.progress and self.main_task is not None:
            self.progress.update(self.main_task, total=total)
    
    def finish_session(self):
        """Finish the current session"""
        self.stats.finish()
        
        if self.progress:
            # Complete all remaining subtasks
            for name in list(self.sub_tasks.keys()):
                self.complete_subtask(name)
            
            # Complete main task
            if self.main_task is not None:
                self.progress.update(self.main_task, completed=True)
            
            # Stop progress display
            self.progress.stop()
        
        # Display completion summary
        self._display_completion_summary()
    
    def pause_session(self):
        """Pause the current session"""
        if self.progress:
            self.progress.stop()
    
    def resume_session(self):
        """Resume the current session"""
        if self.progress:
            self.progress.start()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        return {
            'posts': self.stats.posts_scraped,
            'comments': self.stats.comments_scraped,
            'total': self.stats.total_items,
            'duplicates_removed': self.stats.duplicates_removed,
            'errors': self.stats.errors_encountered,
            'elapsed_time': str(self.stats.elapsed_time),
            'items_per_second': round(self.stats.items_per_second, 2),
            'mode': self.stats.mode,
            'target': self.stats.current_target,
            'start_time': self.stats.start_time.isoformat() if self.stats.start_time else None,
            'end_time': self.stats.end_time.isoformat() if self.stats.end_time else None
        }
    
    def save_session(self, filepath: str):
        """Save session data to file"""
        import json
        from pathlib import Path
        
        session_data = {
            'stats': self.get_stats(),
            'session_data': self.session_data,
            'timestamp': datetime.now().isoformat()
        }
        
        save_path = Path(filepath)
        save_path.parent.mkdir(exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2)
    
    def load_session(self, filepath: str) -> bool:
        """Load session data from file"""
        import json
        from pathlib import Path
        
        load_path = Path(filepath)
        if not load_path.exists():
            return False
        
        try:
            with open(load_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Restore stats
            stats_data = session_data.get('stats', {})
            self.stats.posts_scraped = stats_data.get('posts', 0)
            self.stats.comments_scraped = stats_data.get('comments', 0)
            self.stats.total_items = stats_data.get('total', 0)
            self.stats.duplicates_removed = stats_data.get('duplicates_removed', 0)
            self.stats.errors_encountered = stats_data.get('errors', 0)
            self.stats.mode = stats_data.get('mode', '')
            self.stats.current_target = stats_data.get('target', '')
            
            # Restore session data
            self.session_data = session_data.get('session_data', {})
            
            return True
        except Exception:
            return False
    
    def _display_session_start(self):
        """Display session start information"""
        start_panel = Panel(
            f"[bold red]{self.crow} SCRAPING SESSION INITIATED {self.crow}[/bold red]\n\n"
            f"[white]Mode:[/white] [yellow]{self.stats.mode.upper()}[/yellow]\n"
            f"[white]Target:[/white] [cyan]{self.stats.current_target}[/cyan]\n"
            f"[white]Started:[/white] [green]{self.stats.start_time.strftime('%Y-%m-%d %H:%M:%S')}[/green]\n\n"
            f"[dim italic]\"Those who cannot acknowledge themselves will eventually fail.\" - Itachi Uchiha[/dim italic]",
            style="red",
            border_style="red"
        )
        self.console.print(start_panel)
        self.console.print()
    
    def _display_completion_summary(self):
        """Display completion summary"""
        # Create statistics table
        stats_table = Table(title=f"{self.kunai} Scraping Statistics {self.kunai}", show_header=True, header_style="bold red")
        stats_table.add_column("Metric", style="cyan", width=20)
        stats_table.add_column("Value", style="white", width=15)
        stats_table.add_column("Details", style="dim white")
        
        stats_table.add_row("Posts Scraped", str(self.stats.posts_scraped), "Reddit posts collected")
        stats_table.add_row("Comments Scraped", str(self.stats.comments_scraped), "Comments collected")
        stats_table.add_row("Total Items", str(self.stats.total_items), "Combined posts + comments")
        stats_table.add_row("Duplicates Removed", str(self.stats.duplicates_removed), "Duplicate entries cleaned")
        stats_table.add_row("Errors Encountered", str(self.stats.errors_encountered), "API/Network errors")
        stats_table.add_row("Elapsed Time", str(self.stats.elapsed_time).split('.')[0], "Total scraping time")
        stats_table.add_row("Items/Second", f"{self.stats.items_per_second:.2f}", "Average processing rate")
        
        self.console.print(stats_table)
        self.console.print()
        
        # Display completion message
        completion_panel = Panel(
            f"[bold green]{self.moon} SCRAPING COMPLETED SUCCESSFULLY {self.moon}[/bold green]\n\n"
            f"[white]Total Items Collected:[/white] [yellow]{self.stats.total_items}[/yellow]\n"
            f"[white]Processing Rate:[/white] [cyan]{self.stats.items_per_second:.2f} items/sec[/cyan]\n"
            f"[white]Session Duration:[/white] [green]{str(self.stats.elapsed_time).split('.')[0]}[/green]\n\n"
            f"[dim italic]\"Knowledge and awareness are vague, and perhaps better called illusions.\" - Itachi Uchiha[/dim italic]",
            style="green",
            border_style="green"
        )
        self.console.print(completion_panel)
    
    def display_current_stats(self):
        """Display current statistics during operation"""
        if not self.stats.start_time:
            return
        
        current_time = datetime.now()
        elapsed = current_time - self.stats.start_time
        
        stats_text = (
            f"{self.blood_drop} [bold red]Current Stats[/bold red] {self.blood_drop}\n"
            f"Posts: [yellow]{self.stats.posts_scraped}[/yellow] | "
            f"Comments: [yellow]{self.stats.comments_scraped}[/yellow] | "
            f"Total: [yellow]{self.stats.total_items}[/yellow] | "
            f"Rate: [cyan]{self.stats.items_per_second:.1f}/sec[/cyan] | "
            f"Elapsed: [green]{str(elapsed).split('.')[0]}[/green]"
        )
        
        self.console.print(stats_text)
    
    def display_eta(self, remaining_items: int):
        """Display estimated time of arrival"""
        if self.stats.items_per_second > 0:
            eta_seconds = remaining_items / self.stats.items_per_second
            eta_time = timedelta(seconds=int(eta_seconds))
            
            eta_text = Text(
                f"{self.moon} ETA: {str(eta_time).split('.')[0]} ({remaining_items} items remaining)",
                style="dim cyan"
            )
            self.console.print(eta_text)
    
    def set_session_data(self, key: str, value: Any):
        """Set session-specific data"""
        self.session_data[key] = value
    
    def get_session_data(self, key: str, default: Any = None) -> Any:
        """Get session-specific data"""
        return self.session_data.get(key, default)
