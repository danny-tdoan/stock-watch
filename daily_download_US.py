"""This is mostly similar to daily_download, but to carter for US markets. There are 3 mains markets in US.
"""

import os
import sys
import datetime
import matplotlib.finance as finance
import urllib.request as ur
import matplotlib.mlab as mlab

ASX_TICKER_LIST = 'http://www.asx.com.au/asx/research/ASXListedCompanies.csv'
AMEX_TICKER_LIST = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download'
NASDAQ_TICKER_LIST = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
NYSE_TICKER_LIST = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download'

today = datetime.date.today()
startdate = enddate = today - datetime.timedelta(1)


def download_ticker_US(ticker, sd=startdate, ed=enddate, market=''):
    fh = finance.fetch_historical_yahoo(ticker, sd, ed)

    # archive to disk
    # append to the existing files without the header
    # otherwise create it with the header
    f = 'data/' + market + '/' + ticker + '.txt'
    if not os.path.exists(f):
        fhWrite = open(f, 'w')
        header = fh.readline()
        fhWrite.write(header)
    else:
        fhWrite = open(f, 'a')
        # get the content, ignore the header
        fh.readline()

    r = fh.read()
    if r:
        # sort the records based on the dates
        r = '\r\n'.join(sorted(r.split()))
        fhWrite.write(r)
        # fhWrite.write('\r\n')
        fhWrite.close()


def download_tickers_US(tickers, sd=startdate, ed=enddate, market=''):
    for ticker in tickers:
        # handle the error, if something happen to a stock, move on
        print(ticker)
        try:
            download_ticker_US(ticker, sd, ed, market)
        except (RuntimeError, ur.HTTPError):
            print('Error with ticker ' + ticker)


# for now focus only  in ASX
def download_all_tickers_US(market='ASX', sd=startdate, ed=enddate):
    # new style of naming variable
    amx_tickers = ur.urlopen(AMEX_TICKER_LIST).read().decode()
    nasdaq_tickers = ur.urlopen(NASDAQ_TICKER_LIST).read().decode()
    nyse_tickers = ur.urlopen(NYSE_TICKER_LIST).read().decode()

    data = amx_tickers.split('\r\n')[1:] + nasdaq_tickers.split('\r\n')[1:] + nyse_tickers.split('\r\n')[1:]
    all_tickers = []

    f = 'data/StockList/US.txt'
    fh_write = open(f, 'w')
    for line in data:
        all_tickers.append(line.split(',')[0].strip('"').strip())
        fh_write.write(line.split(',')[0].strip('"').strip() + '\n')
    fh_write.close()

    download_tickers_US(all_tickers, sd, ed, market='US')

    return all_tickers


# check the number of arguments
if len(sys.argv) == 3:
    startdate = datetime.datetime.strptime(sys.argv[1], '%Y.%m.%d')
    enddate = datetime.datetime.strptime(sys.argv[2], '%Y.%m.%d')

download_all_tickers_US('US', sd, ed)
