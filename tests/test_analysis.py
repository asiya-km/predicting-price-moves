"""
Test cases for the analysis modules.
"""

import pytest
import pandas as pd
import numpy as np
from src.data_loader import DataLoader
from src.technical_analysis import TechnicalAnalyzer
from src.sentiment_analysis import SentimentAnalyzer
from src.correlation_analysis import CorrelationAnalyzer

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    dates = pd.date_range(start='2023-01-01', end='2023-01-10', freq='D')
    data = pd.DataFrame({
        'date': dates,
        'Open': np.random.randn(10) + 100,
        'High': np.random.randn(10) + 102,
        'Low': np.random.randn(10) + 98,
        'Close': np.random.randn(10) + 100,
        'Volume': np.random.randint(1000, 10000, 10),
        'headline': [
            'Stock price increases significantly',
            'Company reports strong earnings',
            'Market shows positive momentum',
            'Investors remain cautious',
            'New product launch successful',
            'Competition increases market share',
            'Economic concerns grow',
            'Positive outlook for future',
            'Industry faces challenges',
            'Strong quarterly results'
        ]
    })
    return data

def test_technical_analysis(sample_data):
    """Test technical analysis functionality."""
    analyzer = TechnicalAnalyzer()
    result = analyzer.calculate_indicators(sample_data)
    
    # Check if required indicators are present
    assert 'SMA_20' in result.columns
    assert 'RSI' in result.columns
    assert 'MACD' in result.columns
    
    # Check if values are within expected ranges
    assert result['RSI'].between(0, 100).all()
    assert not result['SMA_20'].isnull().all()

def test_sentiment_analysis(sample_data):
    """Test sentiment analysis functionality."""
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_sentiment(sample_data)
    
    # Check if sentiment scores are present
    assert 'sentiment_score' in result.columns
    assert 'sentiment_category' in result.columns
    
    # Check if sentiment scores are within expected range
    assert result['sentiment_score'].between(-1, 1).all()
    
    # Check if categories are valid
    assert set(result['sentiment_category'].unique()).issubset(
        {'Negative', 'Neutral', 'Positive'}
    )

def test_correlation_analysis(sample_data):
    """Test correlation analysis functionality."""
    # Add sentiment scores first
    sentiment_analyzer = SentimentAnalyzer()
    data_with_sentiment = sentiment_analyzer.analyze_sentiment(sample_data)
    
    # Calculate daily returns
    data_with_sentiment['Daily_Return'] = data_with_sentiment['Close'].pct_change()
    
    analyzer = CorrelationAnalyzer()
    correlations = analyzer.calculate_correlation(data_with_sentiment)
    
    # Check if correlation results are present
    assert 'pearson_correlation' in correlations
    assert 'spearman_correlation' in correlations
    assert 'lagged_correlations' in correlations
    
    # Check if correlations are within valid range
    assert -1 <= correlations['pearson_correlation'] <= 1
    assert -1 <= correlations['spearman_correlation'] <= 1

def test_market_conditions(sample_data):
    """Test market conditions analysis."""
    # Add sentiment scores and returns
    sentiment_analyzer = SentimentAnalyzer()
    data_with_sentiment = sentiment_analyzer.analyze_sentiment(sample_data)
    data_with_sentiment['Daily_Return'] = data_with_sentiment['Close'].pct_change()
    
    analyzer = CorrelationAnalyzer()
    conditions = analyzer.analyze_market_conditions(data_with_sentiment)
    
    # Check if all market conditions are present
    assert 'Bearish' in conditions
    assert 'Neutral' in conditions
    assert 'Bullish' in conditions
    
    # Check if correlations are within valid range
    for condition in conditions.values():
        assert -1 <= condition['pearson'] <= 1
        assert -1 <= condition['spearman'] <= 1 