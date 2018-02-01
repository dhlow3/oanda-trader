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

    return config


def main():
    """Do main stuff."""
    c = get_config('./oanda.conf')
    print(c)


if __name__ == '__main__':
    main()
