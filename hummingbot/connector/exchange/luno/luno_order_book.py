#!/usr/bin/env python
import logging
from typing import (
    Dict,
    Optional
)
from hummingbot.logger import HummingbotLogger
from hummingbot.core.event.events import TradeType
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.data_type.order_book_message import (
    OrderBookMessage,
    OrderBookMessageType
)

_lob_logger = None


class LunoOrderBook(OrderBook):

    @classmethod
    def logger(cls) -> HummingbotLogger:
        global _lob_logger
        if _lob_logger is None:
            _lob_logger = logging.getLogger(__name__)
        return _lob_logger

    @classmethod
    def snapshot_message_from_exchange(cls,
                                       msg: Dict[str, any],
                                       timestamp: float,
                                       metadata: Optional[Dict] = None) -> OrderBookMessage:
        if metadata:
            msg.update(metadata)
        return OrderBookMessage(OrderBookMessageType.SNAPSHOT, {
            "trading_pair": msg["trading_pair"].replace("/", ""),
            "update_id": msg["latest_update"],
            "bids": msg["bids"],
            "asks": msg["asks"]
        }, timestamp=timestamp * 1e-3)

    @classmethod
    def diff_message_from_exchange(cls,
                                   pair: str,
                                   msg: Dict[str, any],
                                   timestamp: Optional[float] = None,
                                   metadata: Optional[Dict] = None) -> OrderBookMessage:
        if metadata:
            msg.update(metadata)
        return OrderBookMessage(OrderBookMessageType.DIFF, {
            "trading_pair": pair,
            "update_id": msg["sequence"],
            "bids": msg["bids"],
            "asks": msg["asks"]
        }, timestamp=msg["timestamp"] * 1e-3)

    @classmethod
    def snapshot_ws_message_from_exchange(cls,
                                          msg: Dict[str, any],
                                          timestamp: Optional[float] = None,
                                          metadata: Optional[Dict] = None) -> OrderBookMessage:
        if metadata:
            msg.update(metadata)
        return OrderBookMessage(OrderBookMessageType.SNAPSHOT, {
            "trading_pair": msg["trading_pair"].replace("/", ""),
            "update_id": msg["update_id"],
            "bids": msg["bids"],
            "asks": msg["asks"]
        }, timestamp=timestamp * 1e-3)

    @classmethod
    def trade_message_from_exchange(cls,
                                    pair: str,
                                    msg: Dict[str, any],
                                    metadata: Optional[Dict] = None):
        if metadata:
            msg.update(metadata)
        trade = msg["tradeUpdate"]
        return OrderBookMessage(OrderBookMessageType.TRADE, {
            "trading_pair": pair,
            "trade_type": float(TradeType.BUY.value) if trade["isBuy"] else float(TradeType.SELL.value),
            "trade_id": trade["sequence"],
            "update_id": trade["sequence"],
            "price": trade["counter"] / trade["base"],
            "amount": trade["base"]
        }, timestamp=trade["timestamp"] * 1e-3)

    @classmethod
    def from_snapshot(cls, msg: OrderBookMessage) -> "OrderBook":
        retval = LunoOrderBook()
        retval.apply_snapshot(msg.bids, msg.asks, msg.update_id)
        return retval
