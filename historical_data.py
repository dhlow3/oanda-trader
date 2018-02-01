"""Get .csv data file of historical FX prices."""
import argparse
from os.path import exists

import oandapyV20.endpoints.instruments as instruments
import pandas as pd
from oandapyV20 import API

from config import get_config


def get_args():
    """Get arguments from command line.

    Returns
    ----------
    args: dict
        Arguments parsed from the command line and any defaults not parsed.

    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Get historical data for an FX pair.')
    parser.add_argument('pair',
                        help='currency pair for which data is required '
                             '(e.g. EUR_USD)')
    parser.add_argument('config_file',
                        help='configuration file with Oanda access token')
    parser.add_argument('-g',
                        dest='granularity',
                        metavar='GRANULARITY',
                        default='M5',
                        help='the granularity of the timeframe')
    parser.add_argument('-c',
                        dest='count',
                        metavar='COUNT',
                        default='30',
                        type=int,
                        help='the number of bars to get')
    parser.add_argument('-o',
                        dest='output',
                        metavar='OUTPUT',
                        default='./sample.csv',
                        help='the path for the output file')
    parser_args = parser.parse_args()

    args = dict(pair=parser_args.pair.upper(),
                config_file=parser_args.config_file,
                granularity=parser_args.granularity,
                count=parser_args.count,
                output=parser_args.output)

    # handle argument errors
    assert '_' in args['pair'], "Currency pair must be '_' separated"
    base, target = args['pair'].split('_')
    assert len(base) == 3, 'base currency must have len of 3 e.g. EUR'
    assert len(target) == 3, 'target currency must have len of 3 e.g. EUR'

    assert exists(args['config_file'])

    assert args['count'] > 0, 'count must be positive integer'

    return args


def get_price_data(pair, config_file, output, **kwargs):
    """Get data from Oanda and put in CSV.

    Parameters
    ----------
    pair: str
        The instrument pair in which to fetch prices.
    config_file : str
        Location of configuration file.
    output: str
        Location and name of output .csv file.

    """
    conf = get_config(config_file)
    kwargs['price'] = 'BA'

    r = instruments.InstrumentsCandles(instrument=pair, params=kwargs)
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
    df.to_csv(output, sep='\t', index=False)


if __name__ == '__main__':
    # Get arguments from parser
    args = get_args()

    # Get required arguments for get_price_data
    pair = args.pop('pair')
    config_file = args.pop('config_file')
    output = args.pop('output')

    # Get price data
    kwargs = args
    get_price_data(pair, config_file, output, **kwargs)
