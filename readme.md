# Overview
This project downloads the daily stock movements of ASX (open/close/high/low/volume) and compute buy signals, sell signals and other indicators to shortlist the stocks to buy/sell in short term.

It mainly supports ASX. Wit suitable downloader, it can be expanded to other markets.

The indicators include:

1. Moving Average
2. Relative Strength Indicator (RSI)
3. Parabolic Stop and Reverse (PSAR)
4. Moving Average Convergence Divergence (MACD)

The script can be scheduled (e.g., in cron) for daily download. The daily shortlisted stocks are put in a text file.

The logic is simple: the stocks that have the most buy signals are likely to increase in short terms. Currently it used a simple yes/no checking. More sophisticated model can built by using the statistics and the indicators as features.

**NOTE: Yahoo Finance API is deprecated since Apr 2018. The program needs to be migrated to use Google Finance instead.**

An example is given [here](https://www.learndatasci.com/tutorials/python-finance-part-yahoo-finance-api-pandas-matplotlib/)

# Usage
1. The downloader (daily_download.py) should be scheduled to download daily movements
2. Generate different indicators/signals by using `check_signal.py` or `check_signal_2day_macd.py` or `check_signal_rsi_oversold.py`

Check `run.sh` for more details.