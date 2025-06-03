"""
Correlation analysis module for analyzing relationships between sentiment and stock movements.
"""

import pandas as pd
import numpy as np
from scipy import stats
import logging
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CorrelationAnalyzer:
    def __init__(self):
        """Initialize the CorrelationAnalyzer class."""
        pass

    def calculate_correlation(self, df, sentiment_col='sentiment_score', return_col='Daily_Return'):
        """
        Calculate correlation between sentiment and returns.
        
        Args:
            df (pd.DataFrame): DataFrame with sentiment and return data
            sentiment_col (str): Name of sentiment score column
            return_col (str): Name of return column
            
        Returns:
            dict: Dictionary containing correlation metrics
        """
        try:
            # Calculate Pearson correlation
            pearson_corr = df[sentiment_col].corr(df[return_col])
            
            # Calculate Spearman correlation
            spearman_corr = df[sentiment_col].corr(df[return_col], method='spearman')
            
            # Calculate time-lagged correlations
            lagged_corrs = {}
            for lag in range(1, 6):  # Calculate for 1-5 day lags
                lagged_corrs[f'lag_{lag}'] = df[sentiment_col].corr(
                    df[return_col].shift(-lag)
                )
            
            results = {
                'pearson_correlation': pearson_corr,
                'spearman_correlation': spearman_corr,
                'lagged_correlations': lagged_corrs
            }
            
            logger.info("Successfully calculated correlations")
            return results
            
        except Exception as e:
            logger.error(f"Error calculating correlations: {str(e)}")
            raise

    def analyze_market_conditions(self, df, sentiment_col='sentiment_score', return_col='Daily_Return'):
        """
        Analyze correlation under different market conditions.
        
        Args:
            df (pd.DataFrame): DataFrame with sentiment and return data
            sentiment_col (str): Name of sentiment score column
            return_col (str): Name of return column
            
        Returns:
            dict: Dictionary containing correlation metrics for different market conditions
        """
        try:
            # Define market conditions
            df['market_condition'] = pd.cut(
                df[return_col],
                bins=[-np.inf, -0.01, 0.01, np.inf],
                labels=['Bearish', 'Neutral', 'Bullish']
            )
            
            # Calculate correlations for each market condition
            condition_corrs = {}
            for condition in ['Bearish', 'Neutral', 'Bullish']:
                condition_data = df[df['market_condition'] == condition]
                condition_corrs[condition] = {
                    'pearson': condition_data[sentiment_col].corr(condition_data[return_col]),
                    'spearman': condition_data[sentiment_col].corr(
                        condition_data[return_col],
                        method='spearman'
                    )
                }
            
            logger.info("Successfully analyzed market conditions")
            return condition_corrs
            
        except Exception as e:
            logger.error(f"Error analyzing market conditions: {str(e)}")
            raise

    def plot_correlation_matrix(self, df, columns=None):
        """
        Plot correlation matrix for selected columns.
        
        Args:
            df (pd.DataFrame): DataFrame with data to analyze
            columns (list): List of columns to include in correlation matrix
            
        Returns:
            matplotlib.figure.Figure: Correlation matrix plot
        """
        try:
            if columns is None:
                columns = df.select_dtypes(include=[np.number]).columns
            
            # Calculate correlation matrix
            corr_matrix = df[columns].corr()
            
            # Create plot
            plt.figure(figsize=(12, 8))
            sns.heatmap(
                corr_matrix,
                annot=True,
                cmap='coolwarm',
                center=0,
                fmt='.2f'
            )
            plt.title('Correlation Matrix')
            
            logger.info("Successfully created correlation matrix plot")
            return plt.gcf()
            
        except Exception as e:
            logger.error(f"Error creating correlation matrix plot: {str(e)}")
            raise 