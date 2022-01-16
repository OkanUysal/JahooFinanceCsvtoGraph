from re import A
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from yahoofinancials import YahooFinancials
import sys
import os
from optparse import OptionParser
pd.options.plotting.backend = "plotly"

#0.22, 0.0952, 0.0392, 0.0198

def calculateEmaStandard(day):
    return 2 / (day + 1);

def main():
    parser = OptionParser(usage='usage: %prog [options] ')

    parser.add_option(
        "--symbol",
        action="store",
        type="string",
        dest='symbol',
        default="BTC-USD",
        help="""Enter the desired symbol found in Yahoo finance.
Like a 'BTC-USD'""",
    )

    parser.add_option(
        "--start-date",
        action="store",
        dest='start_date',
        type="string",
        default="2015-01-01",
        help="""Enter your desired start date""",
    )

    parser.add_option(
        "--end-date",
        action="store",
        dest='end_date',
        type="string",
        default="2023-01-01",
        help="""Enter your desired end date. If you select a future date, it will get today's date.""",
    )

    parser.add_option(
        "--sma-all",
        action="store_true",
        dest='sma_all',
        help="""Open sma 8-20-50-100 days average""",
    )

    parser.add_option(
        "--ema-all",
        action="store_true",
        dest='ema_all',
        help="""Open ema 8-20-50-100 days average""",
    )

    parser.add_option(
        "--sma8",
        action="store_true",
        dest='sma8',
        help="""Open sma 8 days average""",
    )

    parser.add_option(
        "--sma20",
        action="store_true",
        dest='sma20',
        help="""Open sma 20 days average""",
    )

    parser.add_option(
        "--sma50",
        action="store_true",
        dest='sma50',
        help="""Open sma 50 days average""",
    )

    parser.add_option(
        "--sma100",
        action="store_true",
        dest='sma100',
        help="""Open sma 100 days average""",
    )

    parser.add_option(
        "--ema8",
        action="store_true",
        dest='ema8',
        help="""Open ema 8 days average""",
    )

    parser.add_option(
        "--ema20",
        action="store_true",
        dest='ema20',
        help="""Open ema 20 days average""",
    )

    parser.add_option(
        "--ema50",
        action="store_true",
        dest='ema50',
        help="""Open ema 50 days average""",
    )

    parser.add_option(
        "--ema100",
        action="store_true",
        dest='ema100',
        help="""Open ema 100 days average""",
    )

    (options, args) = parser.parse_args()

    yahoo_finance(options)

def yahoo_finance(options):
    yahoo_financials = YahooFinancials(options.symbol)
    data = yahoo_financials.get_historical_price_data(start_date=options.start_date, 
                                                    end_date=options.end_date, 
                                                    time_interval='daily')

    df = pd.DataFrame(data[options.symbol]['prices'])
    df = df[['formatted_date', 'close']]

    if options.sma8 == True :
        df["sma8"] = np.nan
        rangeCount = 7;
    if options.sma20 == True :
        df["sma20"] = np.nan
        rangeCount = 19;
    if options.sma50 == True :
        df["sma50"] = np.nan
        rangeCount = 49;
    if options.sma100 == True :
        df["sma100"] = np.nan
        rangeCount = 99;

    if options.ema_all == True :
        df["ema8"] = np.nan
        df["ema20"] = np.nan
        df["ema50"] = np.nan
        df["ema100"] = np.nan
        rangeCount = 99;

    if options.sma_all == True :
        df["sma8"] = np.nan
        df["sma20"] = np.nan
        df["sma50"] = np.nan
        df["sma100"] = np.nan
        rangeCount = 99;

    for i in range(rangeCount, len(df.index)):
        if options.sma8 == True or options.sma_all == True:
            df.at[i,"sma8"]=df[['close']].iloc[(i - 7):(i + 1),:].mean()
        if options.sma20 == True or options.sma_all == True:
            df.at[i,"sma20"]=df[['close']].iloc[(i - 19):(i + 1),:].mean()
        if options.sma50 == True or options.sma_all == True:
            df.at[i,"sma50"]=df[['close']].iloc[(i - 49):(i + 1),:].mean()
        if options.sma100 == True or options.sma_all == True:
            df.at[i,"sma100"]=df[['close']].iloc[(i - 99):(i + 1),:].mean()

    for i in range(rangeCount, len(df.index)):
        if options.ema8 == True or options.ema_all == True:
            if i == rangeCount :
                df.at[i,"ema8"]=df[['close']].iloc[(i - 7):(i + 1),:].mean()
            else :
                df.at[i,"ema8"]=df.at[i, "close"] * calculateEmaStandard(8) + df.at[i - 1, "ema8"] * (1 - calculateEmaStandard(8)) 
        if options.ema20 == True or options.ema_all == True:
            if i == rangeCount :
                df.at[i,"ema20"]=df[['close']].iloc[(i - 19):(i + 1),:].mean()
            else :
                df.at[i,"ema20"]=df.at[i, "close"] * calculateEmaStandard(20) + df.at[i - 1, "ema20"] * (1 - calculateEmaStandard(20))
        if options.ema50 == True or options.ema_all == True:
            if i == rangeCount :
                df.at[i,"ema50"]=df[['close']].iloc[(i - 49):(i + 1),:].mean()
            else :
                df.at[i,"ema50"]=df.at[i, "close"] * calculateEmaStandard(50) + df.at[i - 1, "ema50"] * (1 - calculateEmaStandard(50))
        if options.ema100 == True or options.ema_all == True:
            if i == rangeCount :
                df.at[i,"ema100"]=df[['close']].iloc[(i - 99):(i + 1),:].mean()
            else :
                df.at[i,"ema100"]=df.at[i, "close"] * calculateEmaStandard(100) + df.at[i - 1, "ema100"] * (1 - calculateEmaStandard(100))
#0.22, 0.0952, 0.0392, 0.0198

    df = df.drop(df.index[0:rangeCount]).set_index('formatted_date')

    fig = df.plot()
    if os.path.isdir("graphics") == False:
        os.mkdir("graphics")

    fig.write_html("graphics/" + options.symbol + ".html")

if __name__ == '__main__':
    main()