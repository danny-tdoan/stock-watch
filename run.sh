#!/bin/bash
export STOCK_WATCH_HOME=/home/empty/projects/deployment/StockWatch/

python3 $STOCK_WATCH_HOME/daily_download.py > /tmp/download.log 2>&1
python3 $STOCK_WATCH_HOME/check_signal.py > /tmp/check.log 2>&1 &
python3 $STOCK_WATCH_HOME/check_signal_2day_macd.py > /tmp/check_2day_macd.log 2>&1 &
python3 $STOCK_WATCH_HOME/check_signal_rsi_oversold.py > /tmp/check_rsi_oversold.log 2>&1 &
