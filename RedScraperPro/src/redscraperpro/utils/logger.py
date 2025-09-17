"""
Logging System for RedScraperPro
🩸 Comprehensive logging with themed output 🩸
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text
from loguru import logger as loguru_logger


class Logger:
    """Enhanced logging system with Rich integration"""
    
    def __init__(self, verbose: bool = False, quiet: bool = False, log_file: Optional[str] = None):
        self.console = Console()
        self.verbose = verbose
        self.quiet = quiet
        
        # Create logs directory
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Set up log file path
        if log_file:
            self.log_file = Path(log_file)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file = self.logs_dir / f"redscraperpro_{timestamp}.log"
        
        # Configure loguru
        self._setup_loguru()
        
        # Configure standard logging
        self._setup_standard_logging()
    
    def _setup_loguru(self):
        """Set up loguru logger"""
        # Remove default handler
        loguru_logger.remove()
        
        # Add file handler
        loguru_logger.add(
            self.log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="7 days",
            compression="zip"
        )
        
        # Add console handler if not quiet
        if not self.quiet:
            log_level = "DEBUG" if self.verbose else "INFO"
            loguru_logger.add(
                sys.stderr,
                format="<red>🩸</red> <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
                level=log_level,
                colorize=True
            )
    
    def _setup_standard_logging(self):
        """Set up standard Python logging"""
        # Configure root logger
        logging.basicConfig(
            level=logging.DEBUG if self.verbose else logging.INFO,
            format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
            handlers=[
                logging.FileHandler(self.log_file),
                RichHandler(console=self.console, show_path=False) if not self.quiet else logging.NullHandler()
            ]
        )
        
        # Get logger
        self.logger = logging.getLogger("RedScraperPro")
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        loguru_logger.debug(message, **kwargs)
        if self.verbose and not self.quiet:
            debug_text = Text(f"🔍 DEBUG: {message}", style="dim white")
            self.console.print(debug_text)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        loguru_logger.info(message, **kwargs)
        if not self.quiet:
            info_text = Text(f"ℹ️  {message}", style="blue")
            self.console.print(info_text)
    
    def success(self, message: str, **kwargs):
        """Log success message"""
        loguru_logger.success(message, **kwargs)
        if not self.quiet:
            success_text = Text(f"✅ {message}", style="bold green")
            self.console.print(success_text)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        loguru_logger.warning(message, **kwargs)
        if not self.quiet:
            warning_text = Text(f"⚠️  {message}", style="bold yellow")
            self.console.print(warning_text)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        loguru_logger.error(message, **kwargs)
        if not self.quiet:
            error_text = Text(f"❌ {message}", style="bold red")
            self.console.print(error_text)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        loguru_logger.critical(message, **kwargs)
        if not self.quiet:
            critical_text = Text(f"💀 CRITICAL: {message}", style="bold red on white")
            self.console.print(critical_text)
    
    def scraping_start(self, mode: str, target: str, limit: int):
        """Log scraping start"""
        message = f"Starting {mode} scraping for '{target}' (limit: {limit})"
        loguru_logger.info(message)
        if not self.quiet:
            start_text = Text(f"🕷️  {message}", style="bold cyan")
            self.console.print(start_text)
    
    def scraping_progress(self, current: int, total: int, item_type: str = "items"):
        """Log scraping progress"""
        percentage = (current / total) * 100 if total > 0 else 0
        message = f"Progress: {current}/{total} {item_type} ({percentage:.1f}%)"
        loguru_logger.debug(message)
        if self.verbose and not self.quiet:
            progress_text = Text(f"📊 {message}", style="cyan")
            self.console.print(progress_text)
    
    def scraping_complete(self, stats: dict):
        """Log scraping completion"""
        message = f"Scraping completed - Posts: {stats.get('posts', 0)}, Comments: {stats.get('comments', 0)}, Total: {stats.get('total', 0)}"
        loguru_logger.success(message)
        if not self.quiet:
            complete_text = Text(f"🎯 {message}", style="bold green")
            self.console.print(complete_text)
    
    def export_start(self, format_type: str, filename: str):
        """Log export start"""
        message = f"Exporting data to {format_type.upper()} format: {filename}"
        loguru_logger.info(message)
        if not self.quiet:
            export_text = Text(f"📤 {message}", style="magenta")
            self.console.print(export_text)
    
    def export_complete(self, filepath: str, record_count: int):
        """Log export completion"""
        message = f"Export completed: {record_count} records saved to {filepath}"
        loguru_logger.success(message)
        if not self.quiet:
            complete_text = Text(f"💾 {message}", style="bold green")
            self.console.print(complete_text)
    
    def api_request(self, endpoint: str, params: dict = None):
        """Log API request"""
        params_str = f" with params: {params}" if params else ""
        message = f"API request to {endpoint}{params_str}"
        loguru_logger.debug(message)
        if self.verbose and not self.quiet:
            api_text = Text(f"🌐 {message}", style="dim blue")
            self.console.print(api_text)
    
    def api_response(self, endpoint: str, status: str, count: int = None):
        """Log API response"""
        count_str = f" ({count} items)" if count is not None else ""
        message = f"API response from {endpoint}: {status}{count_str}"
        loguru_logger.debug(message)
        if self.verbose and not self.quiet:
            response_text = Text(f"📡 {message}", style="dim green")
            self.console.print(response_text)
    
    def rate_limit_warning(self, wait_time: float):
        """Log rate limit warning"""
        message = f"Rate limit approached, waiting {wait_time:.1f} seconds"
        loguru_logger.warning(message)
        if not self.quiet:
            rate_text = Text(f"⏳ {message}", style="yellow")
            self.console.print(rate_text)
    
    def sentiment_analysis(self, processed: int, total: int):
        """Log sentiment analysis progress"""
        message = f"Sentiment analysis: {processed}/{total} items processed"
        loguru_logger.debug(message)
        if self.verbose and not self.quiet:
            sentiment_text = Text(f"🧠 {message}", style="purple")
            self.console.print(sentiment_text)
    
    def duplicate_removal(self, original: int, after_removal: int):
        """Log duplicate removal"""
        removed = original - after_removal
        message = f"Duplicate removal: {removed} duplicates removed ({original} → {after_removal})"
        loguru_logger.info(message)
        if not self.quiet:
            duplicate_text = Text(f"🧹 {message}", style="yellow")
            self.console.print(duplicate_text)
    
    def config_loaded(self, config_path: str):
        """Log configuration loading"""
        message = f"Configuration loaded from: {config_path}"
        loguru_logger.info(message)
        if self.verbose and not self.quiet:
            config_text = Text(f"⚙️  {message}", style="cyan")
            self.console.print(config_text)
    
    def config_saved(self, config_path: str):
        """Log configuration saving"""
        message = f"Configuration saved to: {config_path}"
        loguru_logger.info(message)
        if not self.quiet:
            config_text = Text(f"💾 {message}", style="green")
            self.console.print(config_text)
    
    def session_start(self, session_id: str):
        """Log session start"""
        message = f"Session started: {session_id}"
        loguru_logger.info(message)
        if not self.quiet:
            session_text = Text(f"🚀 {message}", style="bold blue")
            self.console.print(session_text)
    
    def session_resume(self, session_id: str):
        """Log session resume"""
        message = f"Session resumed: {session_id}"
        loguru_logger.info(message)
        if not self.quiet:
            resume_text = Text(f"🔄 {message}", style="bold yellow")
            self.console.print(resume_text)
    
    def session_save(self, session_file: str):
        """Log session save"""
        message = f"Session saved: {session_file}"
        loguru_logger.info(message)
        if self.verbose and not self.quiet:
            save_text = Text(f"💾 {message}", style="dim green")
            self.console.print(save_text)
    
    def exception(self, exc: Exception, context: str = ""):
        """Log exception with context"""
        context_str = f" in {context}" if context else ""
        message = f"Exception{context_str}: {type(exc).__name__}: {str(exc)}"
        loguru_logger.exception(message)
        if not self.quiet:
            exc_text = Text(f"💥 {message}", style="bold red")
            self.console.print(exc_text)
    
    def get_log_file_path(self) -> str:
        """Get the current log file path"""
        return str(self.log_file)
    
    def get_log_stats(self) -> dict:
        """Get logging statistics"""
        if self.log_file.exists():
            file_size = self.log_file.stat().st_size
            with open(self.log_file, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
            
            return {
                'file_path': str(self.log_file),
                'file_size': file_size,
                'line_count': line_count,
                'created': datetime.fromtimestamp(self.log_file.stat().st_ctime)
            }
        return {}
    
    def display_log_stats(self):
        """Display logging statistics"""
        from rich.table import Table
        
        stats = self.get_log_stats()
        if stats:
            table = Table(title="📊 Logging Statistics", show_header=True, header_style="bold red")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("Log File", stats['file_path'])
            table.add_row("File Size", f"{stats['file_size']:,} bytes")
            table.add_row("Line Count", f"{stats['line_count']:,}")
            table.add_row("Created", stats['created'].strftime("%Y-%m-%d %H:%M:%S"))
            
            self.console.print(table)
    
    def cleanup_old_logs(self, days: int = 7):
        """Clean up old log files"""
        import time
        
        current_time = time.time()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        removed_count = 0
        for log_file in self.logs_dir.glob("redscraperpro_*.log*"):
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                    removed_count += 1
                except Exception as e:
                    self.warning(f"Could not remove old log file {log_file}: {e}")
        
        if removed_count > 0:
            self.info(f"Cleaned up {removed_count} old log files")
        
        return removed_count
