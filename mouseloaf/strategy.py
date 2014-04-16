#!/usr/bin/env python

from actor import Actor
from plugin import PluginRegistry


class StrategyBase(Actor):
    __metaclass__=PluginRegistry
    def __init__(self, config, coordinator):
        super(StrategyBase, self).__init__(coordinator)
        self._subscribe(config.feed, self._handle_feed_data)
        self._subscribe(config.broker, self._handle_broker)
        self._strategy_init()

    """ API exposed to Strategy subclasses """
    def _place_order(self, stuff):
        # should we build order types in this layer or make strategy
        # implementations do it?
        self._publish(stuff)

    def _portfolio(self):
        pass

    """ Interface implemented by Strategy subclasses """
    def _handle_feed_data(self, data):
        raise NotImplementedError("Strategy subclasses must implement this.")

    def _handle_broker(self, data):
        raise NotImplementedError("Strategy subclasses must implement this.")

    def _strategy_init(self):
        raise NotImplementedError("Strategy subclasses must implement this.")
