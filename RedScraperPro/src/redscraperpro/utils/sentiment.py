"""
Sentiment Analysis for RedScraperPro
🩸 Lightweight sentiment analysis functionality 🩸
"""

from typing import Dict, Any, Optional, List
from redscraperpro.utils.logger import Logger


class SentimentAnalyzer:
    """Handles sentiment analysis for scraped content"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.textblob_available = False
        self.vader_available = False
        
        # Try to import sentiment analysis libraries
        try:
            from textblob import TextBlob
            self.TextBlob = TextBlob
            self.textblob_available = True
            self.logger.debug("TextBlob sentiment analysis available")
        except ImportError:
            self.logger.warning("TextBlob not available for sentiment analysis")
        
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.vader_analyzer = SentimentIntensityAnalyzer()
            self.vader_available = True
            self.logger.debug("VADER sentiment analysis available")
        except ImportError:
            self.logger.warning("VADER sentiment not available for sentiment analysis")
    
    def analyze_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Analyze sentiment of a single text"""
        if not text or not text.strip():
            return None
        
        sentiment_data = {}
        
        # TextBlob analysis
        if self.textblob_available:
            try:
                blob = self.TextBlob(text)
                sentiment_data['textblob'] = {
                    'polarity': blob.sentiment.polarity,  # -1 (negative) to 1 (positive)
                    'subjectivity': blob.sentiment.subjectivity,  # 0 (objective) to 1 (subjective)
                    'classification': self._classify_textblob_sentiment(blob.sentiment.polarity)
                }
            except Exception as e:
                self.logger.error(f"TextBlob analysis failed: {str(e)}")
                sentiment_data['textblob'] = None
        
        # VADER analysis
        if self.vader_available:
            try:
                scores = self.vader_analyzer.polarity_scores(text)
                sentiment_data['vader'] = {
                    'positive': scores['pos'],
                    'negative': scores['neg'],
                    'neutral': scores['neu'],
                    'compound': scores['compound'],  # -1 (negative) to 1 (positive)
                    'classification': self._classify_vader_sentiment(scores['compound'])
                }
            except Exception as e:
                self.logger.error(f"VADER analysis failed: {str(e)}")
                sentiment_data['vader'] = None
        
        # Combined analysis
        if sentiment_data:
            sentiment_data['combined'] = self._combine_sentiments(sentiment_data)
        
        return sentiment_data if sentiment_data else None
    
    def analyze_batch(self, texts: List[str]) -> List[Optional[Dict[str, Any]]]:
        """Analyze sentiment for a batch of texts"""
        results = []
        
        for i, text in enumerate(texts):
            try:
                sentiment = self.analyze_text(text)
                results.append(sentiment)
                
                # Log progress for large batches
                if (i + 1) % 100 == 0:
                    self.logger.debug(f"Processed {i + 1}/{len(texts)} texts for sentiment analysis")
                    
            except Exception as e:
                self.logger.error(f"Error analyzing text {i}: {str(e)}")
                results.append(None)
        
        return results
    
    def analyze_reddit_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add sentiment analysis to Reddit data"""
        if not self.is_available():
            self.logger.warning("No sentiment analysis libraries available")
            return data
        
        self.logger.info(f"Starting sentiment analysis for {len(data)} items")
        
        for i, item in enumerate(data):
            try:
                # Get text content based on item type
                text = self._extract_text_from_item(item)
                
                if text:
                    sentiment = self.analyze_text(text)
                    item['sentiment'] = sentiment
                else:
                    item['sentiment'] = None
                
                # Log progress
                if (i + 1) % 50 == 0:
                    self.logger.debug(f"Sentiment analysis progress: {i + 1}/{len(data)}")
                    
            except Exception as e:
                self.logger.error(f"Error analyzing sentiment for item {i}: {str(e)}")
                item['sentiment'] = None
        
        self.logger.success(f"Sentiment analysis completed for {len(data)} items")
        return data
    
    def _extract_text_from_item(self, item: Dict[str, Any]) -> str:
        """Extract text content from Reddit item"""
        if item.get('type') == 'post':
            # For posts, combine title and selftext
            title = item.get('title', '')
            selftext = item.get('selftext', '') or item.get('content', '')
            return f"{title} {selftext}".strip()
        
        elif item.get('type') == 'comment':
            # For comments, use body
            return item.get('body', '') or item.get('content', '')
        
        else:
            # Fallback to any available text content
            return item.get('content', '') or item.get('body', '') or item.get('title', '')
    
    def _classify_textblob_sentiment(self, polarity: float) -> str:
        """Classify TextBlob polarity into categories"""
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def _classify_vader_sentiment(self, compound: float) -> str:
        """Classify VADER compound score into categories"""
        if compound >= 0.05:
            return 'positive'
        elif compound <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def _combine_sentiments(self, sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Combine TextBlob and VADER results"""
        combined = {
            'classification': 'neutral',
            'confidence': 0.0,
            'agreement': False
        }
        
        textblob_result = sentiment_data.get('textblob')
        vader_result = sentiment_data.get('vader')
        
        if textblob_result and vader_result:
            # Check if both methods agree
            tb_class = textblob_result['classification']
            vader_class = vader_result['classification']
            
            combined['agreement'] = tb_class == vader_class
            
            if combined['agreement']:
                # Both agree, use the classification
                combined['classification'] = tb_class
                
                # Calculate confidence based on both scores
                tb_confidence = abs(textblob_result['polarity'])
                vader_confidence = abs(vader_result['compound'])
                combined['confidence'] = (tb_confidence + vader_confidence) / 2
            else:
                # Disagreement, use the one with higher confidence
                tb_confidence = abs(textblob_result['polarity'])
                vader_confidence = abs(vader_result['compound'])
                
                if tb_confidence > vader_confidence:
                    combined['classification'] = tb_class
                    combined['confidence'] = tb_confidence
                else:
                    combined['classification'] = vader_class
                    combined['confidence'] = vader_confidence
        
        elif textblob_result:
            # Only TextBlob available
            combined['classification'] = textblob_result['classification']
            combined['confidence'] = abs(textblob_result['polarity'])
        
        elif vader_result:
            # Only VADER available
            combined['classification'] = vader_result['classification']
            combined['confidence'] = abs(vader_result['compound'])
        
        return combined
    
    def is_available(self) -> bool:
        """Check if sentiment analysis is available"""
        return self.textblob_available or self.vader_available
    
    def get_available_methods(self) -> List[str]:
        """Get list of available sentiment analysis methods"""
        methods = []
        if self.textblob_available:
            methods.append('textblob')
        if self.vader_available:
            methods.append('vader')
        return methods
    
    def get_sentiment_statistics(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate sentiment statistics for analyzed data"""
        if not data:
            return {}
        
        # Filter items with sentiment data
        items_with_sentiment = [item for item in data if item.get('sentiment')]
        
        if not items_with_sentiment:
            return {'error': 'No sentiment data found'}
        
        # Count classifications
        classifications = {}
        positive_scores = []
        negative_scores = []
        neutral_scores = []
        
        for item in items_with_sentiment:
            sentiment = item['sentiment']
            
            # Use combined classification if available, otherwise use first available method
            if sentiment.get('combined'):
                classification = sentiment['combined']['classification']
                confidence = sentiment['combined']['confidence']
            elif sentiment.get('textblob'):
                classification = sentiment['textblob']['classification']
                confidence = abs(sentiment['textblob']['polarity'])
            elif sentiment.get('vader'):
                classification = sentiment['vader']['classification']
                confidence = abs(sentiment['vader']['compound'])
            else:
                continue
            
            classifications[classification] = classifications.get(classification, 0) + 1
            
            if classification == 'positive':
                positive_scores.append(confidence)
            elif classification == 'negative':
                negative_scores.append(confidence)
            else:
                neutral_scores.append(confidence)
        
        # Calculate statistics
        total_analyzed = len(items_with_sentiment)
        
        stats = {
            'total_analyzed': total_analyzed,
            'total_items': len(data),
            'coverage_percentage': (total_analyzed / len(data)) * 100,
            'classifications': classifications,
            'percentages': {
                classification: (count / total_analyzed) * 100
                for classification, count in classifications.items()
            },
            'average_confidence': {
                'positive': sum(positive_scores) / len(positive_scores) if positive_scores else 0,
                'negative': sum(negative_scores) / len(negative_scores) if negative_scores else 0,
                'neutral': sum(neutral_scores) / len(neutral_scores) if neutral_scores else 0
            },
            'methods_used': self.get_available_methods()
        }
        
        return stats
    
    def filter_by_sentiment(self, data: List[Dict[str, Any]], 
                          sentiment_type: str = 'positive',
                          min_confidence: float = 0.1) -> List[Dict[str, Any]]:
        """Filter data by sentiment classification and confidence"""
        filtered_data = []
        
        for item in data:
            sentiment = item.get('sentiment')
            if not sentiment:
                continue
            
            # Get classification and confidence
            if sentiment.get('combined'):
                classification = sentiment['combined']['classification']
                confidence = sentiment['combined']['confidence']
            elif sentiment.get('textblob'):
                classification = sentiment['textblob']['classification']
                confidence = abs(sentiment['textblob']['polarity'])
            elif sentiment.get('vader'):
                classification = sentiment['vader']['classification']
                confidence = abs(sentiment['vader']['compound'])
            else:
                continue
            
            # Filter by sentiment type and confidence
            if classification == sentiment_type and confidence >= min_confidence:
                filtered_data.append(item)
        
        return filtered_data
