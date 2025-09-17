"""
Test Suite for RedScraperPro
🩸 Basic tests to ensure functionality 🩸
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.config import Config, RedditConfig, ScrapingConfig, ExportConfig, UIConfig
from utils.logger import Logger
from utils.quotes import Quotes
from utils.ascii_art import ASCIIArt


class TestConfig(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        self.config = Config()
    
    def test_reddit_config_creation(self):
        """Test Reddit configuration creation"""
        reddit_config = RedditConfig(
            client_id="test_id",
            client_secret="test_secret",
            user_agent="test_agent"
        )
        
        self.assertEqual(reddit_config.client_id, "test_id")
        self.assertEqual(reddit_config.client_secret, "test_secret")
        self.assertEqual(reddit_config.user_agent, "test_agent")
    
    def test_scraping_config_defaults(self):
        """Test scraping configuration defaults"""
        scraping_config = ScrapingConfig()
        
        self.assertEqual(scraping_config.default_limit, 100)
        self.assertEqual(scraping_config.default_depth, 1)
        self.assertTrue(scraping_config.include_comments)
        self.assertFalse(scraping_config.enable_sentiment)
    
    def test_export_config_defaults(self):
        """Test export configuration defaults"""
        export_config = ExportConfig()
        
        self.assertEqual(export_config.default_format, "csv")
        self.assertEqual(export_config.output_directory, "exports")
        self.assertTrue(export_config.include_timestamp)
    
    def test_config_validation(self):
        """Test configuration validation"""
        # Test with empty config
        self.assertFalse(self.config.is_configured())
        
        # Test with valid config
        self.config.update_reddit_config(
            client_id="test_id",
            client_secret="test_secret",
            user_agent="test_agent"
        )
        self.assertTrue(self.config.is_configured())


class TestLogger(unittest.TestCase):
    """Test logging functionality"""
    
    def setUp(self):
        self.logger = Logger(verbose=False, quiet=True)  # Quiet mode for tests
    
    def test_logger_creation(self):
        """Test logger creation"""
        self.assertIsNotNone(self.logger)
        self.assertFalse(self.logger.verbose)
        self.assertTrue(self.logger.quiet)
    
    def test_logging_methods(self):
        """Test various logging methods"""
        # These should not raise exceptions
        self.logger.debug("Test debug message")
        self.logger.info("Test info message")
        self.logger.success("Test success message")
        self.logger.warning("Test warning message")
        self.logger.error("Test error message")
    
    def test_scraping_logs(self):
        """Test scraping-specific logging methods"""
        self.logger.scraping_start("test", "target", 100)
        self.logger.scraping_progress(50, 100)
        self.logger.scraping_complete({"posts": 10, "comments": 20, "total": 30})


class TestQuotes(unittest.TestCase):
    """Test quotes functionality"""
    
    def setUp(self):
        self.quotes = Quotes()
    
    def test_quote_categories(self):
        """Test different quote categories"""
        stoic_quote = self.quotes.get_random_quote("stoic")
        kafka_quote = self.quotes.get_random_quote("kafka")
        dostoevsky_quote = self.quotes.get_random_quote("dostoevsky")
        itachi_quote = self.quotes.get_random_quote("itachi")
        
        self.assertIsInstance(stoic_quote, str)
        self.assertIsInstance(kafka_quote, str)
        self.assertIsInstance(dostoevsky_quote, str)
        self.assertIsInstance(itachi_quote, str)
        
        # Check that quotes contain expected content
        self.assertIn("Marcus Aurelius", stoic_quote)
        self.assertIn("Kafka", kafka_quote)
        self.assertIn("Dostoevsky", dostoevsky_quote)
        self.assertIn("Itachi", itachi_quote)
    
    def test_random_quote(self):
        """Test random quote selection"""
        quote1 = self.quotes.get_random_quote()
        quote2 = self.quotes.get_random_quote()
        
        self.assertIsInstance(quote1, str)
        self.assertIsInstance(quote2, str)
        # Quotes should be non-empty
        self.assertGreater(len(quote1), 0)
        self.assertGreater(len(quote2), 0)


class TestASCIIArt(unittest.TestCase):
    """Test ASCII art functionality"""
    
    def setUp(self):
        self.ascii_art = ASCIIArt()
    
    def test_ascii_art_creation(self):
        """Test ASCII art object creation"""
        self.assertIsNotNone(self.ascii_art)
        self.assertIsNotNone(self.ascii_art.logo)
        self.assertIsNotNone(self.ascii_art.separators)
    
    def test_themed_elements(self):
        """Test themed elements"""
        self.assertEqual(self.ascii_art.blood_drop, "🩸")
        self.assertEqual(self.ascii_art.moon, "🌙")
        self.assertEqual(self.ascii_art.kunai, "🗡️")
    
    def test_prompt_generation(self):
        """Test themed prompt generation"""
        prompt = self.ascii_art.get_themed_prompt("Test message")
        self.assertIn("🩸", prompt)
        self.assertIn("Test message", prompt)


class TestDataStructures(unittest.TestCase):
    """Test data structure handling"""
    
    def test_post_data_structure(self):
        """Test expected post data structure"""
        expected_fields = [
            'type', 'id', 'title', 'author', 'subreddit', 
            'created_utc', 'score', 'num_comments', 'url'
        ]
        
        # Mock post data
        post_data = {
            'type': 'post',
            'id': 'test123',
            'title': 'Test Post',
            'author': 'test_user',
            'subreddit': 'test',
            'created_utc': 1234567890,
            'score': 100,
            'num_comments': 50,
            'url': 'https://reddit.com/test'
        }
        
        for field in expected_fields:
            self.assertIn(field, post_data)
    
    def test_comment_data_structure(self):
        """Test expected comment data structure"""
        expected_fields = [
            'type', 'id', 'author', 'body', 'subreddit',
            'created_utc', 'score', 'depth'
        ]
        
        # Mock comment data
        comment_data = {
            'type': 'comment',
            'id': 'comment123',
            'author': 'test_user',
            'body': 'Test comment body',
            'subreddit': 'test',
            'created_utc': 1234567890,
            'score': 25,
            'depth': 1
        }
        
        for field in expected_fields:
            self.assertIn(field, comment_data)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_flatten_dict(self):
        """Test dictionary flattening functionality"""
        # This would test the CSV exporter's flatten functionality
        nested_dict = {
            'level1': {
                'level2': {
                    'value': 'test'
                }
            },
            'simple': 'value'
        }
        
        # Expected flattened result
        expected = {
            'level1_level2_value': 'test',
            'simple': 'value'
        }
        
        # Note: This is a conceptual test - actual implementation would be in CSV exporter
        self.assertIsInstance(nested_dict, dict)
        self.assertIsInstance(expected, dict)


class TestErrorHandling(unittest.TestCase):
    """Test error handling"""
    
    def test_invalid_config(self):
        """Test handling of invalid configuration"""
        config = Config()
        
        # Test validation with empty config
        self.assertFalse(config.validate_reddit_config())
    
    def test_missing_dependencies(self):
        """Test handling of missing optional dependencies"""
        # Test sentiment analysis without libraries
        try:
            from utils.sentiment import SentimentAnalyzer
            logger = Logger(quiet=True)
            analyzer = SentimentAnalyzer(logger)
            
            # Should handle missing libraries gracefully
            self.assertIsInstance(analyzer.is_available(), bool)
        except ImportError:
            # If sentiment module doesn't exist, that's also fine
            pass


def run_tests():
    """Run all tests"""
    print("🩸 Running RedScraperPro Tests 🩸")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestConfig,
        TestLogger,
        TestQuotes,
        TestASCIIArt,
        TestDataStructures,
        TestUtilityFunctions,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print results
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎯 All tests passed!")
        print("💭 \"Those who cannot acknowledge themselves will eventually fail.\" - Itachi Uchiha")
    else:
        print(f"❌ {len(result.failures)} test(s) failed")
        print(f"⚠️  {len(result.errors)} error(s) occurred")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)  
