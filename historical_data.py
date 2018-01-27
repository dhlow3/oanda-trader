"""Get .csv data for feed."""
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
from oandapyV20 import API

from config import get_config


def get_price_data(pair, config_file, dst, **kwargs):
    """Get data from Oanda and put in CSV.

    Parameters
    ----------
    pair: str
        The instrument pair in which to fetch prices.
    config_file : str
        Location of configuration file.
    dst: str
        Location and name of output .csv file.

    """
    conf = get_config(config_file)
    params = dict(kwargs)
    params['price'] = 'BA'
    print(params)
    r = instruments.InstrumentsCandles(instrument=pair, params=params)
    api = API(access_token=conf['token'])
    api.request(r)

    prices = []
    for _ in r.response['candles']:
        prices.append([_['time'],
                       _['bid']['c'],
                       _['ask']['c'],
                       float(_['ask']['c']) -
                       float(_['bid']['c'])])

    df = pd.DataFrame(prices)
    df.columns = ['time', 'bid', 'ask', 'spread']
    df.to_csv(dst, sep='\t', index=False)


if __name__ == '__main__':
    params = {'granularity': 'M5', 'count': 10}
    pair = 'EUR_USD'

    get_price_data(pair=pair,
                   config_file='./oanda.conf',
                   dst='./data/sample.csv',
                   **params)
