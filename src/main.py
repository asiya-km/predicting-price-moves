"""
Main script demonstrating the usage of all modules for the project.
"""

import pandas as pd
import logging
from data_loader import DataLoader
from technical_analysis import TechnicalAnalyzer
from sentiment_analysis import SentimentAnalyzer
from correlation_analysis import CorrelationAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to demonstrate the project functionality."""
    try:
        # Initialize components
        data_loader = DataLoader()
        tech_analyzer = TechnicalAnalyzer()
        sentiment_analyzer = SentimentAnalyzer()
        correlation_analyzer = CorrelationAnalyzer()
        
        # Load data
        logger.info("Loading data...")
        news_data = data_loader.load_news_data('data/financial_news.csv')
        stock_data = data_loader.load_stock_data(
            stock_symbols=['AAPL', 'MSFT', 'GOOGL'],
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        
        # Align data
        logger.info("Aligning data...")
        aligned_data = data_loader.align_data()
        
        # Process each stock
        for symbol, data in aligned_data.items():
            logger.info(f"Processing {symbol}...")
            
            # Technical analysis
            data = tech_analyzer.calculate_indicators(data)
            data = tech_analyzer.generate_signals(data)
            
            # Sentiment analysis
            data = sentiment_analyzer.analyze_sentiment(data)
            sentiment_agg = sentiment_analyzer.aggregate_sentiment(data)
            
            # Correlation analysis
            correlations = correlation_analyzer.calculate_correlation(data)
            market_conditions = correlation_analyzer.analyze_market_conditions(data)
            
            # Create visualizations
            plt.figure(figsize=(15, 10))
            
            # Plot 1: Price and Sentiment
            plt.subplot(2, 1, 1)
            plt.plot(data['date'], data['Close'], label='Price')
            plt.title(f'{symbol} - Price and Sentiment')
            plt.legend()
            
            # Plot 2: Sentiment Distribution
            plt.subplot(2, 1, 2)
            sns.histplot(data['sentiment_score'], bins=50)
            plt.title('Sentiment Score Distribution')
            
            plt.tight_layout()
            plt.savefig(f'output/{symbol}_analysis.png')
            plt.close()
            
            # Save results
            data.to_csv(f'output/{symbol}_processed.csv', index=False)
            
            # Log results
            logger.info(f"Results for {symbol}:")
            logger.info(f"Correlation with returns: {correlations['pearson_correlation']:.3f}")
            logger.info(f"Market condition correlations: {market_conditions}")
            
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 