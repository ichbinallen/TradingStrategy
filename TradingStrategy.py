import pandas as pd
import matplotlib.pyplot as plt


class TradingStrategy:
    ''' Implement a naive stock trading strategy

    Buy and hold when the short term signal is higher than the long term signal
    '''

    def __init__(self, stock_data, short_signal=10, long_signal=50):
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
        pass

    def show_data(self, nrows=10):
        print(self.stock.head(nrows))

    def plot(self):
        pass


if __name__ == '__main__':
    apple = TradingStrategy('./data/microsoft.csv')
    apple.show_data(50)
