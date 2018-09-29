"""This is to be pushed to crontab and called everyday to download the stock movements of the previous date.
The data will be used to generate indicators and signals, based on which it will shortlist a group of stocks
to buy (in short term)

NOTE: Yahoo Finance API is deprecated since Apr 2018. The program needs to be migrated to use Google Finance instead
https://www.learndatasci.com/tutorials/python-finance-part-yahoo-finance-api-pandas-matplotlib/

"""

import os
import sys
import datetime
import matplotlib.finance as finance
import urllib.request as ur
import matplotlib.mlab as mlab

ASX_TICKER_LIST = 'http://www.asx.com.au/asx/research/ASXListedCompanies.csv'

today = datetime.date.today()
startdate = enddate = today - datetime.timedelta(1)


def download_ticker(ticker, sd=startdate, ed=enddate):
    """Download stocks open/close/high/close/volume from ASX and push to the central csv"""
    fh = finance.fetch_historical_yahoo(ticker, sd, ed)

    # archive to disk
    # append to the existing files without the header
    # otherwise create it with the header
    f = 'data/' + ticker + '.txt'
    if not os.path.exists(f):
        fhWrite = open(f, 'w')
        header = fh.readline()
        fhWrite.write(header)
    else:
        fhWrite = open(f, 'a')

        # get the content, ignore the header
        fh.readline()

    r = fh.read()
    r = '\r\n'.join(sorted(r.split()))
    fhWrite.write(r)
    fhWrite.write('\r\n')
    fhWrite.close()


def download_tickers(tickers, sd=startdate, ed=enddate):
    for ticker in tickers:
        # handle the error, if something happen to a stock, move on
        print(ticker)
        try:
            download_ticker(ticker, sd, ed)
        except (RuntimeError, ur.HTTPError):
            print('Error with ticker ' + ticker)


# for now focus only  in ASX
def download_all_tickers(market='ASX', sd=startdate, ed=enddate):
    """Download all stocks of a market. The list of stocks can be easily downloaded from the Stock Exchange site.
    Only support ASX for now. Will expand to US markets later"""
    if market == 'ASX':
        allTickers = str(ur.urlopen(ASX_TICKER_LIST).read()).strip("b")

        lines = allTickers.split("\\r\\n")
        f = 'data/StockList/ASX.txt'
        fhWrite = open(f, 'w')

        fhWrite.write('CompanyName,ASXCode,GICS\n')
        for i in range(3, len(lines)):
            fhWrite.write(lines[i] + "\n")
        fhWrite.close()

        allTickers = mlab.csv2rec(f)
        # print(allTickers)

        # get all the tickers
        tickers = allTickers.asxcode;

        tickers = [x + '.AX' for x in tickers]

        download_tickers(tickers, sd, ed)
        return tickers


# check the number of arguments
if len(sys.argv) == 3:
    startdate = datetime.datetime.strptime(sys.argv[1], '%Y.%m.%d')
    enddate = datetime.datetime.strptime(sys.argv[2], '%Y.%m.%d')

download_all_tickers('ASX', startdate, enddate)
