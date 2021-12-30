from re import A
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from yahoofinancials import YahooFinancials
import sys
from optparse import OptionParser
pd.options.plotting.backend = "plotly"

def main():
    parser = OptionParser(usage='usage: %prog [options] ')

    parser.add_option(
        "--symbol",
        action="store",
        type="string",
        default="BTC-USD",
        help="""Enter the desired symbol found in Yahoo finance.
Like a 'BTC-USD'""",
    )

    (options, args) = parser.parse_args()

    yahoo_finance(options.symbol)

def yahoo_finance(symbol):
    yahoo_financials = YahooFinancials(symbol)
    data = yahoo_financials.get_historical_price_data(start_date='2015-11-01', 
                                                    end_date='2022-12-01', 
                                                    time_interval='daily')

    df = pd.DataFrame(data[symbol]['prices'])
    df = df[['formatted_date', 'close']]
    df["last8"] = np.nan
    df["last20"] = np.nan
    df["last50"] = np.nan
    df["last100"] = np.nan

    for i in range(99, len(df.index)):
        df.at[i,"last8"]=df[['close']].iloc[(i - 7):(i + 1),:].mean()
        df.at[i,"last20"]=df[['close']].iloc[(i - 19):(i + 1),:].mean()
        df.at[i,"last50"]=df[['close']].iloc[(i - 49):(i + 1),:].mean()
        df.at[i,"last100"]=df[['close']].iloc[(i - 99):(i + 1),:].mean()

    df = df.drop(df.index[0:99]).set_index('formatted_date')

    fig = df.plot()
    fig.write_html(symbol + ".html")

if __name__ == '__main__':
    main()