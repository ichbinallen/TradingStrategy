import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class TradingStrategy:
    ''' Implement a naive stock trading strategy

    Buy and hold when the short term signal is higher than the long term signal
    '''

    def __init__(self, stock_data, short_signal=10, long_signal=30):
        ''' Read data from a csv file

        stock_data -- a csv file with columns:
            Date: (YYYY-mm-dd)
            Open: Opening price on that trading day
            High: High price on that trading day
            Close: Closing price on that trading day
            Adj Close: ??? Not sure what this is, not needed currently
            Volume: Number of trades on that trading day
        short_signal -- Short signal = <short_signal> day moving average
        long_signal -- Long signal = <long_signal> day moving average
        '''
        self.short_signal = short_signal
        self.long_signal = long_signal
        self.stock = pd.read_csv(stock_data, index_col='Date')

    def trade(self):
        ''' Compute what would happen by following the trading strategy
        Return Null and modify self.stock

        when the short signal moving average rises above the long term moving average,
        we hold the asset. Otherwise, sell.
        Return is the daily profit/loss from the trading strategy.
        '''
        self.stock['short_signal'] = self.stock['Close'].rolling(self.short_signal).mean()
        self.stock['long_signal'] = self.stock['Close'].rolling(self.long_signal).mean()
        self.stock['Hold'] = np.where(
            self.stock['short_signal'] > self.stock['long_signal'], 1, 0
        )
        self.stock['Diff'] = self.stock['Close'].shift(-1) - self.stock['Close']
        self.stock['Return'] = np.where(self.stock['Hold'], self.stock['Diff'], 0)

    def profit(self, strategy, start_date, end_date):
        ''' Compute profit under the trading strategy and return as a float

        strategy -- one of 'hold' or 'trade'
            hold: buy and hold the stock for the entire duration
            trade: hold when short_sig > long_sig
        '''
        daily_profit = self.stock.loc[
            (self.stock.index >= start_date) & (self.stock.index <= end_date),
            ['Return', 'Diff']]
        if strategy == 'hold':
            total_profit = daily_profit['Diff'].sum()
        elif strategy == 'trade':
            total_profit = daily_profit['Return'].sum()
        else:
            print('Warning: strategy should be one of ("hold", "trade")')
            return(None)

        print(total_profit)
        total_profit = np.round(total_profit, 2)
        return(total_profit)

    def show_data(self, nrows=10):
        ''' Silly little print method for debugging convenience '''
        mr = pd.options.display.max_rows
        pd.set_option('display.max_rows', nrows)
        print(self.stock.head(nrows))
        pd.set_option('display.max_rows', mr)

    def plot(self):
        self.stock.loc[:, ['Close', 'short_signal', 'long_signal']].plot()
        plt.show()


if __name__ == '__main__':
    apple = TradingStrategy('./data/apple.csv', short_signal=10, long_signal=50)
    apple.trade()
    apple.show_data(20)
    start_date = '2006-10-02'
    end_date = '2017-12-29'
    hold_profit = apple.profit('hold', start_date, end_date)
    trade_profit = apple.profit('trade', start_date, end_date)
    print(f'profit by trading: {trade_profit}')
    print(f'profit by holding: {hold_profit}')
    print(f'Trading strategy gains: {trade_profit - hold_profit}')
    apple.plot()
