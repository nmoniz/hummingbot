from typing import (
    Any,
    Dict,
    Optional)

import hummingbot.connector.exchange.luno.luno_constants as constants
from hummingbot.client.config.config_methods import using_exchange
from hummingbot.client.config.config_var import ConfigVar

CENTRALIZED = True
EXAMPLE_PAIR = "ETH-BTC"
DEFAULT_FEES = [0.1, 0.1]

KEYS = {
    "luno_api_key":
        ConfigVar(key="luno_api_key",
                  prompt="Enter your Luno API key >>> ",
                  required_if=using_exchange("luno"),
                  is_secure=True,
                  is_connect_key=True),
    "luno_api_secret":
        ConfigVar(key="luno_api_secret",
                  prompt="Enter your Luno API secret >>> ",
                  required_if=using_exchange("luno"),
                  is_secure=True,
                  is_connect_key=True),
}


def convert_from_exchange_trading_pair(exchange_trading_pair: str) -> Optional[str]:
    return exchange_trading_pair[:3] + "-" + exchange_trading_pair[3:]


def convert_to_exchange_trading_pair(hb_trading_pair: str) -> Optional[str]:
    return hb_trading_pair.strip("-")


def convert_from_exchange_symbol(symbol: str) -> str:
    # Assuming if starts with Z or X and has 4 letters then Z/X is removable
    if (symbol[0] == "X" or symbol[0] == "Z") and len(symbol) == 4:
        symbol = symbol[1:]
    return constants.KRAKEN_TO_HB_MAP.get(symbol, symbol)


def split_to_base_quote(exchange_trading_pair: str) -> (Optional[str], Optional[str]):
    base, quote = exchange_trading_pair.split("-")
    return base, quote


def is_dark_pool(trading_pair_details: Dict[str, Any]):
    '''
    Want to filter out dark pool trading pairs from the list of trading pairs
    For more info, please check
    https://support.kraken.com/hc/en-us/articles/360001391906-Introducing-the-Kraken-Dark-Pool
    '''
    if trading_pair_details.get('altname'):
        return trading_pair_details.get('altname').endswith('.d')
    return False
