"""Get configuration variables."""
import yaml


def get_config(config_file):
    """Get configuration parameters for a .yaml file.

    Parameters
    ----------
    config_file : str
        Path to .yaml config file.

    Returns
    -------
    config_params: dict
        A dict with various config params.

    """
    with open(config_file) as c_file:
        config = yaml.load(c_file)

    config_params = {'user': config.get('user'),
                     'pass': config.get('pass'),
                     'token': config.get('token'),
                     'account': config.get('account')}
    return config_params


def main():
    """Do main stuff."""
    c = get_config('./oanda.conf')
    print('user: {user}\npass: {pass}\ntoken: {token}\naccount: {account}'
          .format(**c))


if __name__ == '__main__':
    main()
