"""
Sentiment analysis module for analyzing financial news headlines.
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        """Initialize the SentimentAnalyzer class."""
        pass

    def preprocess_text(self, text):
        """
        Preprocess text for sentiment analysis.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Preprocessed text
        """
        if not isinstance(text, str):
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text

    def analyze_sentiment(self, df, text_column='headline'):
        """
        Perform sentiment analysis on text data.
        
        Args:
            df (pd.DataFrame): DataFrame containing text data
            text_column (str): Name of the column containing text
            
        Returns:
            pd.DataFrame: DataFrame with added sentiment scores
        """
        try:
            # Create a copy of the input DataFrame
            result_df = df.copy()
            
            # Preprocess text
            result_df['processed_text'] = result_df[text_column].apply(self.preprocess_text)
            
            # Calculate sentiment scores
            result_df['sentiment_score'] = result_df['processed_text'].apply(
                lambda x: TextBlob(x).sentiment.polarity
            )
            
            # Calculate sentiment magnitude
            result_df['sentiment_magnitude'] = result_df['processed_text'].apply(
                lambda x: TextBlob(x).sentiment.subjectivity
            )
            
            # Categorize sentiment
            result_df['sentiment_category'] = pd.cut(
                result_df['sentiment_score'],
                bins=[-1, -0.1, 0.1, 1],
                labels=['Negative', 'Neutral', 'Positive']
            )
            
            logger.info("Successfully performed sentiment analysis")
            return result_df
            
        except Exception as e:
            logger.error(f"Error performing sentiment analysis: {str(e)}")
            raise

    def aggregate_sentiment(self, df, group_by='date'):
        """
        Aggregate sentiment scores by date or other grouping.
        
        Args:
            df (pd.DataFrame): DataFrame with sentiment scores
            group_by (str): Column to group by
            
        Returns:
            pd.DataFrame: Aggregated sentiment scores
        """
        try:
            # Group by date and calculate mean sentiment
            aggregated = df.groupby(group_by).agg({
                'sentiment_score': ['mean', 'std', 'count'],
                'sentiment_magnitude': 'mean'
            }).reset_index()
            
            # Flatten column names
            aggregated.columns = [
                group_by,
                'mean_sentiment',
                'sentiment_std',
                'article_count',
                'mean_magnitude'
            ]
            
            logger.info("Successfully aggregated sentiment scores")
            return aggregated
            
        except Exception as e:
            logger.error(f"Error aggregating sentiment scores: {str(e)}")
            raise 