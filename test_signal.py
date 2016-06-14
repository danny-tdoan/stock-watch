import matplotlib.mlab as mlab
import technical_indicators as ti
import plot_graph
import statistics
import datetime
import os
import sys

def generate_indicator(ticker):
    #load the content from file
    f='data/'+ticker+'.txt'

    tickerData=mlab.csv2rec(f)
    tickerData.sort()

    prices=tickerData.adj_close

    volumes=tickerData.volume

    #only proceed if it's not a penny stock, with high liquidity
    #if

    #generate the MA
    ma20=ti.moving_average(prices,20,type='simple')
    ma200=ti.moving_average(prices,20,type='simple')

    #RSI
    rsi=ti.relative_strength(prices)

    #MACD
    emaSlow,emaFast,macd=ti.moving_average_convergence(prices,nslow=26,nfast=12)
    ema9=ti.moving_average(macd,9,type='exponential')

    return [tickerData,ma20,ma200,rsi,macd,ema9]


if len(sys.argv)<2:
	print("No stock given")
else:
	ticker=sys.argv[1]
	(tickerData,ma20,ma200,rsi,macd,ema9)=generate_indicator(ticker)

	today=datetime.date.today()
	fh=open("raw_technicals/"+ticker+"_"+str(today)+".txt","w")

	fh.write("TICKER DATA:\n")

	fh.write(str(tickerData)+"\n======================================================================================\n")

	fh.write("MA20: "+str(ma20)+"\n")

	fh.write("MA200: "+str(ma200)+"\n")

	fh.write("RSI: "+str(rsi)+"\n")

	fh.write("MACD: "+str(macd)+"\n")

	fh.write("EMA9: "+str(ema9)+"\n")
