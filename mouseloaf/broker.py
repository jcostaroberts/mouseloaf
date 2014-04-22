#!/usr/bin/env python

from actor import Actor
from event import AuxData
from plugin import PluginRegistry
from protocol import Order
from protocol import OrderStatus

class Portfolio(object):
    def __init__(self):
        self.stuff = "XXX"

class BrokerBase(Actor):
    __metaclass__=PluginRegistry
    (OPEN, FILLED, CANCELED, EXPIRED, PARTIALLY_FILLED) = range(5)
    def __init__(self, config, coordinator):
        super(BrokerBase, self).__init__(coordinator)
        self._subscribe(Order("", 0).msg_type(), self._handle_order)
        self.portfolio = Portfolio()
        self._register_auxiliary_data("portfolio",
                                       AuxData(self.portfolio,
                                               self.name,
                                               False))
        self.broker_init()

    def _handle_order(self, order):
        assert type(order) == Order
        self.handle_order(order.order_id, order.symbol, order.quantity,
                          order.limit_price, order.stop_price)

    """ API exposed to Broker subclasses """
    def _report_order_status(self, order_id, status, filled, remaining, price):
        self._publish(OrderStatus(order_id, status, filled, remaining, price))

    """ Interface implemented by Broker subclasses """
    def handle_order(self, order_id, symbol, quantity, limit_price, stop_price):
        raise NotImplementedError("Broker subclasses must implement this.")

    def broker_init(self):
        raise NotImplementedError("Broker subclasses must implement this.")
