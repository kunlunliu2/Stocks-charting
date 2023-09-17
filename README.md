# Stocks-charting
It is a repository that downloads, plots, and records the US—stock data for trend analysis. The code uses PythonV3 with packages, PyQt5, yfinance, datetime, and pandas. Hence, to use the code, one shall install these packages on the computer. More specifically:
  (1) python -m pip install PyQt5
  (2) python -m pip install finance
  (3) python -m pip install pandas
  (4) python -m pip install datetime
  (5) python -m pip install numpy

After the installation, stockAna3.py is the main executable. The Volatility indicator is calculated by: (Today's close - Today's open) / (Today's volume * Today's close) * factor + 50. This indicator measures how easily the stock price can be moved by volume. when > 50, it is bullish and bearish when < 50. High-frequency oscillation with large amplitude indicates the domination of short team swing trading. This is often seen when the stock moves to a high peak or bottom. 
