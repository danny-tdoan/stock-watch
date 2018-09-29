import matplotlib.mlab as mlab
import technical_indicators as ti
import plot_graph
import statistics
import datetime


# load the stock and generate the indicators
# return [SMA,EMA,MACD,RSI]

def generate_indicator(ticker):
    # load the content from file
    f = 'data/' + ticker + '.txt'

    tickerData = mlab.csv2rec(f)
    tickerData.sort()

    prices = tickerData.adj_close

    volumes = tickerData.volume

    # only proceed if it's not a penny stock, with high liquidity
    # if

    # generate the MA
    ma20 = ti.moving_average(prices, 20, type='simple')
    ma200 = ti.moving_average(prices, 20, type='simple')

    # RSI
    rsi = ti.relative_strength(prices)

    # MACD
    emaSlow, emaFast, macd = ti.moving_average_convergence(prices, nslow=26, nfast=12)
    ema9 = ti.moving_average(macd, 9, type='exponential')

    return [tickerData, ma20, ma200, rsi, macd, ema9]


def check_indicator(ticker):
    try:
        # [tickerData,ma20,ma200,rsi,macd,ema9]=generate_indicator(ticker)
        f = 'data/' + ticker + '.txt'

        tickerData = mlab.csv2rec(f)
        tickerData.sort()

        prices = tickerData.adj_close

        volumes = tickerData.volume

        # only proceed if it's not a penny stock, with high liquidity, with sufficient records
        if statistics.mean(volumes[-10:]) < 150000:
            return False
        if statistics.mean(prices[-10:]) < 1:
            return False
        if len(prices) < 200:
            return False

        # generate the MA
        ma20 = ti.moving_average(prices, 20, type='simple')
        ma200 = ti.moving_average(prices, 200, type='simple')

        # RSI
        rsi = ti.relative_strength(prices)

        # MACD
        emaSlow, emaFast, macd = ti.moving_average_convergence(prices, nslow=26, nfast=12)
        ema9 = ti.moving_average(macd, 9, type='exponential')

        # check RSI
        RSICheck = check_rsi(rsi)

        # check MACD
        MACDCheck = check_macd(macd, ema9)

        buySignal = RSICheck and MACDCheck

        if buySignal:
            1
            # plot_graph.plot(tickerData,ticker)

        return buySignal
    except FileNotFoundError:
        # print('Error with ticker '+ticker)
        return False


def check_signal():
    # get the list of all tickers
    tickersFile = mlab.csv2rec('data/StockList/ASX.txt')
    tickers = tickersFile.asxcode
    tickers = [x + '.AX' for x in tickers]

    finalList = []
    for ticker in tickers:
        print('Checking ticker ' + ticker)
        if check_indicator(ticker):
            finalList.append(ticker)
            print(finalList)
    # write to file
    today = datetime.date.today()
    fp = open('output/STOCKS_' + str(today) + '.txt', 'w')
    fp.write(str(finalList))
    fp.close()

    return finalList


def check_rsi(rsi):
    '''Check the condition for RSI
        RSI is above 45-70 level but not in the overbougth area
        RSI just cross 50
        RSI increasing
    '''
    return rsi[-1] <= 55 and non_decreasing(rsi[-2:])


def check_macd(macd, ema9):
    '''MACD just passess ema9
        MACD just crosses 0
        for now just check MACD-EMA9 is not decreasing
    '''
    vals = macd - ema9
    a = vals[-3:]
    a1 = macd[-3:]
    a2 = ema9[-3:]
    # return non_decreasing(vals[-3:])
    return strictly_increasing(vals[-3:])


def check_psar(psarVals):
    return True


def check_cci(cciVals):
    return True


def strictly_increasing(L):
    return all(x < y for x, y in zip(L, L[1:]))


def strictly_decreasing(L):
    return all(x > y for x, y in zip(L, L[1:]))


def non_increasing(L):
    return all(x >= y for x, y in zip(L, L[1:]))


def non_decreasing(L):
    return all(x <= y for x, y in zip(L, L[1:]))


# print(check_indicator('MTS.AX'))
print(check_signal())
