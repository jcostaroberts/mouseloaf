#!/usr/bin/env python

from actor import Actor
from plugin import PluginRegistry
from protocol import FeedData
from protocol import SymbolRequest
from protocol import Order
from protocol import OrderStatus

class StrategyBase(Actor):
    __metaclass__=PluginRegistry
    def __init__(self, config, coordinator):
        super(StrategyBase, self).__init__(coordinator)
        self._subscribe(OrderStatus("", 0).msg_type(),
                        self._handle_order_status)
        self.strategy_init()

    def _handle_feed_data(self, data):
        assert type(data) == FeedData
        self.handle_feed_data(data.symbol, data.exchange, data.time,
                              data.bid_price, data.bid_quantity,
                              data.ask_price, data.ask_quantity)

    def _handle_order_status(self, status):
        assert type(status) == OrderStatus
        self.handle_order_status(status.order_id, status.status,
                                 status.filled, status.remaining,
                                 status.price)

    """ API exposed to Strategy subclasses """
    def _request_symbol(self, symbol):
        self._subscribe(FeedData(symbol).msg_type(),
                        self._handle_feed_data)
        self._publish(SymbolRequest(symbol))

    def _place_order(self, symbol, quantity, limit_price=None, stop_price=None):
        order = Order(symbol, quantity, limit_price, stop_price)
        self._publish(order)
        return order.order_id

    def _portfolio(self):
        pass

    """ Interface implemented by Strategy subclasses """
    def handle_feed_data(self, symbol, exchange, time,
                         bid_price, bid_quantity,
                         ask_price, ask_quantity):
        raise NotImplementedError("Strategy subclasses must implement this.")

    def handle_order_status(self, order_id, status):
        raise NotImplementedError("Strategy subclasses must implement this.")

    def strategy_init(self):
        raise NotImplementedError("Strategy subclasses must implement this.")

