"""
Technical analysis module using TA-Lib for calculating various technical indicators.
"""

import pandas as pd
import numpy as np
import talib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    def __init__(self):
        """Initialize the TechnicalAnalyzer class."""
        pass

    def calculate_indicators(self, df):
        """
        Calculate various technical indicators for the given price data.
        
        Args:
            df (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.DataFrame: DataFrame with added technical indicators
        """
        try:
            # Ensure required columns exist
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("DataFrame must contain OHLCV columns")

            # Moving Averages
            df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
            df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
            df['EMA_20'] = talib.EMA(df['Close'], timeperiod=20)
            
            # RSI
            df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
            
            # MACD
            macd, macd_signal, macd_hist = talib.MACD(
                df['Close'],
                fastperiod=12,
                slowperiod=26,
                signalperiod=9
            )
            df['MACD'] = macd
            df['MACD_Signal'] = macd_signal
            df['MACD_Hist'] = macd_hist
            
            # Bollinger Bands
            upper, middle, lower = talib.BBANDS(
                df['Close'],
                timeperiod=20,
                nbdevup=2,
                nbdevdn=2,
                matype=0
            )
            df['BB_Upper'] = upper
            df['BB_Middle'] = middle
            df['BB_Lower'] = lower
            
            # Volume indicators
            df['OBV'] = talib.OBV(df['Close'], df['Volume'])
            
            # Momentum indicators
            df['MOM'] = talib.MOM(df['Close'], timeperiod=10)
            
            # Volatility indicators
            df['ATR'] = talib.ATR(
                df['High'],
                df['Low'],
                df['Close'],
                timeperiod=14
            )
            
            logger.info("Successfully calculated technical indicators")
            return df
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {str(e)}")
            raise

    def generate_signals(self, df):
        """
        Generate trading signals based on technical indicators.
        
        Args:
            df (pd.DataFrame): DataFrame with technical indicators
            
        Returns:
            pd.DataFrame: DataFrame with added trading signals
        """
        try:
            # Initialize signal column
            df['Signal'] = 0
            
            # RSI signals
            df.loc[df['RSI'] < 30, 'Signal'] = 1  # Oversold
            df.loc[df['RSI'] > 70, 'Signal'] = -1  # Overbought
            
            # MACD signals
            df.loc[df['MACD'] > df['MACD_Signal'], 'Signal'] += 1
            df.loc[df['MACD'] < df['MACD_Signal'], 'Signal'] -= 1
            
            # Bollinger Bands signals
            df.loc[df['Close'] < df['BB_Lower'], 'Signal'] += 1
            df.loc[df['Close'] > df['BB_Upper'], 'Signal'] -= 1
            
            # Normalize signals to -1, 0, 1
            df['Signal'] = np.sign(df['Signal'])
            
            logger.info("Successfully generated trading signals")
            return df
            
        except Exception as e:
            logger.error(f"Error generating trading signals: {str(e)}")
            raise 