"""
Data loading and preprocessing module for financial news and stock price analysis.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        """Initialize the DataLoader class."""
        self.news_data = None
        self.stock_data = None

    def load_news_data(self, file_path):
        """
        Load financial news data from CSV file.
        
        Args:
            file_path (str): Path to the news data CSV file
            
        Returns:
            pd.DataFrame: Processed news data
        """
        try:
            self.news_data = pd.read_csv(file_path)
            logger.info(f"Successfully loaded news data with {len(self.news_data)} records")
            
            # Convert date column to datetime
            self.news_data['date'] = pd.to_datetime(self.news_data['date'])
            
            # Basic preprocessing
            self.news_data = self.news_data.dropna(subset=['headline', 'stock'])
            self.news_data = self.news_data.drop_duplicates()
            
            return self.news_data
        except Exception as e:
            logger.error(f"Error loading news data: {str(e)}")
            raise

    def load_stock_data(self, stock_symbols, start_date, end_date):
        """
        Load stock price data using yfinance.
        
        Args:
            stock_symbols (list): List of stock symbols
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            
        Returns:
            dict: Dictionary of stock data DataFrames
        """
        try:
            self.stock_data = {}
            for symbol in stock_symbols:
                stock = yf.Ticker(symbol)
                df = stock.history(start=start_date, end=end_date)
                
                if not df.empty:
                    # Calculate daily returns
                    df['Daily_Return'] = df['Close'].pct_change()
                    
                    # Calculate volatility (20-day rolling standard deviation)
                    df['Volatility'] = df['Daily_Return'].rolling(window=20).std()
                    
                    self.stock_data[symbol] = df
                    logger.info(f"Successfully loaded data for {symbol}")
                else:
                    logger.warning(f"No data found for {symbol}")
            
            return self.stock_data
        except Exception as e:
            logger.error(f"Error loading stock data: {str(e)}")
            raise

    def align_data(self):
        """
        Align news and stock data by date.
        
        Returns:
            dict: Dictionary containing aligned data for each stock
        """
        if self.news_data is None or self.stock_data is None:
            raise ValueError("News data and stock data must be loaded first")
        
        aligned_data = {}
        for symbol in self.stock_data.keys():
            # Filter news for this stock
            stock_news = self.news_data[self.news_data['stock'] == symbol].copy()
            
            # Merge with stock data
            merged_data = pd.merge_asof(
                stock_news.sort_values('date'),
                self.stock_data[symbol].reset_index().rename(columns={'Date': 'date'}),
                on='date',
                direction='backward'
            )
            
            aligned_data[symbol] = merged_data
            
        return aligned_data 