import os
import sys
import datetime
import matplotlib.finance as finance
import urllib.request as ur
import matplotlib.mlab as mlab

ASX_TICKER_LIST='http://www.asx.com.au/asx/research/ASXListedCompanies.csv'

today=datetime.date.today()
startdate=enddate=today-datetime.timedelta(1)

def download_ticker(ticker,sd=startdate,ed=enddate):
    fh=finance.fetch_historical_yahoo(ticker,sd,ed)

    #archive to disk
    #append to the existing files without the header
    #otherwise create it with the header
    f='data/'+ticker+'.txt'
    if not os.path.exists(f):
        fhWrite=open(f,'w')
        header=fh.readline()
        fhWrite.write(header)
    else:
        fhWrite=open(f,'a')
        #get the content, ignore the header
        fh.readline()

    r=fh.read()
    r='\r\n'.join(sorted(r.split()))
    fhWrite.write(r)
    fhWrite.write('\r\n')
    fhWrite.close()

def download_tickers(tickers,sd=startdate,ed=enddate):
    for ticker in tickers:
        #handle the error, if something happen to a stock, move on
        print(ticker)
        try:
            download_ticker(ticker,sd,ed)
        except (RuntimeError,ur.HTTPError):
            print('Error with ticker '+ticker)

#for now focus only  in ASX
def download_all_tickers(market='ASX',sd=startdate,ed=enddate):
    if market=='ASX':
        allTickers=str(ur.urlopen(ASX_TICKER_LIST).read()).strip("b")

        lines=allTickers.split("\\r\\n")
        f='data/StockList/ASX.txt'
        fhWrite=open(f,'w')

        fhWrite.write('CompanyName,ASXCode,GICS\n')
        for i in range(3,len(lines)):
            fhWrite.write(lines[i]+"\n")
        fhWrite.close()

        allTickers=mlab.csv2rec(f)
        #print(allTickers)

        #get all the tickers
        tickers=allTickers.asxcode;

        tickers=[x+'.AX' for x in tickers]

        download_tickers(tickers,sd,ed)
        return tickers


#check the number of arguments
if len(sys.argv)==3:
    startdate=datetime.datetime.strptime(sys.argv[1],'%Y.%m.%d')
    enddate=datetime.datetime.strptime(sys.argv[2],'%Y.%m.%d')

print(len(sys.argv))
print(sys.argv)
print(startdate)
print(enddate)
#ticker='1PG.AX'
#sd=datetime.date(2014,1,1)
#sd=datetime.date(2015,1,21)
#ed=datetime.date(2016,3,23)
#download_ticker(ticker,sd,ed)
download_all_tickers('ASX',startdate,enddate)
