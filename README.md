# Predicting Price Moves with News Sentiment

A comprehensive analysis project that explores the relationship between financial news sentiment and stock market movements. This project combines natural language processing techniques with technical analysis to identify patterns and correlations that could potentially predict stock price movements.

## Features

- **News Sentiment Analysis**: Analyze financial news headlines using TextBlob for sentiment scoring
- **Technical Analysis**: Calculate various technical indicators using TA-Lib
- **Correlation Analysis**: Study relationships between news sentiment and stock movements
- **Market Condition Analysis**: Analyze sentiment impact under different market conditions
- **Data Visualization**: Generate insightful visualizations of price movements and sentiment

## Project Structure

```
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows
│       ├── unittests.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── technical_analysis.py
│   ├── sentiment_analysis.py
│   ├── correlation_analysis.py
│   └── main.py
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── tests/
│   ├── __init__.py
│   └── test_analysis.py
└── scripts/
    ├── __init__.py
    └── README.md
```

## Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/asiya-km/predicting-price-moves.git
cd predicting-price-moves
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare your data:
   - Place your financial news data in the `data` directory as `financial_news.csv`
   - The CSV should contain columns: headline, date, stock, etc.

2. Run the analysis:
```bash
python src/main.py
```

3. View results:
   - Processed data will be saved in the `output` directory
   - Visualizations will be generated as PNG files
   - Logs will show correlation metrics and analysis results

## Project Tasks

### Task 1: Git and GitHub
- [x] Setting up Python environment
- [x] Git version control
- [x] CI/CD setup

### Task 2: Quantitative Analysis
- [x] Technical indicators using TA-Lib
- [x] Financial metrics with PyNance
- [x] Data visualization

### Task 3: News-Stock Correlation
- [x] Sentiment analysis of news headlines
- [x] Correlation analysis between sentiment and stock movements
- [x] Statistical validation

## Technical Details

### Data Processing
- News data preprocessing and cleaning
- Stock price data retrieval using yfinance
- Time alignment of news and price data

### Analysis Components
- **Technical Analysis**: Moving averages, RSI, MACD, Bollinger Bands
- **Sentiment Analysis**: Text preprocessing, sentiment scoring, category classification
- **Correlation Analysis**: Pearson/Spearman correlations, time-lagged analysis

### Visualization
- Price and sentiment time series plots
- Sentiment distribution histograms
- Correlation matrices
- Market condition analysis charts

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- TextBlob for sentiment analysis
- TA-Lib for technical indicators
- yfinance for stock data
- PyNance for financial metrics

mkdir -p data output

