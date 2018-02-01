"""Stream FX price data."""
import argparse
from os.path import exists

from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingStream

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
        description='Stream live FX prices.')
    parser.add_argument('pair',
                        help='currency pair for which data is required '
                             '(e.g. EUR_USD)')
    parser.add_argument('config_file',
                        help='configuration file with Oanda access token and '
                             'environment')
    parser.add_argument('-c',
                        dest='count',
                        metavar='COUNT',
                        default='5',
                        type=int,
                        help='the number of bars to get')
    parser_args = parser.parse_args()

    args = dict(pair=parser_args.pair.upper(),
                config_file=parser_args.config_file,
                count=parser_args.count)

    # Handle argument errors
    assert '_' in args['pair'], "Currency pair must be '_' separated"
    base, target = args['pair'].split('_')
    assert len(base) == 3, 'base currency must have len of 3 e.g. EUR'
    assert len(target) == 3, 'target currency must have len of 3 e.g. EUR'

    assert exists(args['config_file'])

    assert args['count'] > 0, 'count must be positive integer'

    return args


def stream_prices(pair, config_file, count):
    """Stream price data.

    Parameters
    ----------
    pair: str
        The instrument pair in which to fetch prices.
    config_file : str
        Location of configuration file.
    count: int
        The number of price bars to get.

    """
    conf = get_config(config_file)
    api = API(access_token=conf['token'], environment=conf['environment'])
    r = PricingStream(accountID=conf['account'], params={'instruments': pair})
    api.request(r)

    if 'JPY' in pair:
        spread_multiplier = 100
    else:
        spread_multiplier = 10000

    n = 0
    print('\n{}'.format(pair))
    for _ in api.request(r):
        if _['type'] == 'PRICE':
            d = dict(bid=_['bids'][0]['price'],
                     ask=_['asks'][0]['price'])
            d['spread'] = round(float(d['ask']) * spread_multiplier -
                                float(d['bid']) * spread_multiplier, 1)
            print('Bid: {}'.format(d['bid']))
            print('Ask: {}'.format(d['ask']))
            print('Spread: {}\n'.format(d['spread']))
            n += 1
            if n >= count:
                break


if __name__ == '__main__':
    # Get arguments from parser
    args = get_args()

    # Get required arguments from stream_prices
    pair = args['pair']
    config_file = args['config_file']
    count = args['count']

    # Stream price data
    stream_prices(pair=pair, config_file=config_file, count=count)
