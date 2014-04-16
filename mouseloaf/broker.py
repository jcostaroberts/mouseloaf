#!/usr/bin/env python

from actor import Actor
from event import AuxData
from plugin import PluginRegistry

class Portfolio(object):
    def __init__(self):
        self.stuff = "XXX"

class BrokerBase(Actor):
    __metaclass__=PluginRegistry
    def __init__(self, config, coordinator):
        super(BrokerBase, self).__init__(coordinator)
        self._subscribe(config.strategy, self._handle_order)
        self.portfolio = Portfolio()
        self._register_auxiliary_data("portfolio",
                                       AuxData(self.portfolio,
                                               self.name,
                                               False))
        self._subscribe(config.strategy, self._handle_order)
        self._broker_init()

    """ API exposed to Broker subclasses """
    def _report_order_status(self, order_status):
        self._publish(order_status)

    """ Interface implemented by Broker subclasses """
    def _handle_order(self, order):
        raise NotImplementedError("Broker subclasses must implement this.")

    def _broker_init(self):
        raise NotImplementedError("Broker subclasses must implement this.")
