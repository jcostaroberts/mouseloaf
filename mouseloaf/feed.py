#!/usr/bin/env python

from actor import Actor
from event import Activity
from protocol import FeedData
from protocol import SymbolRequest
from plugin import PluginRegistry


class FeedBase(Actor):
    __metaclass__=PluginRegistry
    def __init__(self, config, coordinator):
        super(FeedBase, self).__init__(coordinator)
        self._subscribe(SymbolRequest("").msg_type(),
                        self._handle_symbol_request)
        self.feed_init()

    def _handle_symbol_request(self, symbol_request):
        assert type(symbol_request) == SymbolRequest
        self.handle_symbol_request(symbol_request.symbol)

    """ API exposed to Feed subclasses """
    def _publish_data(self, symbol, exchange=None, time=None,
                      bid_price=None, bid_quantity=None,
                      ask_price=None, ask_quantity=None):
        fd = FeedData(symbol, exchange, time, bid_price, bid_quantity,
                      ask_price, ask_quantity)
        self._publish(fd)

    def _get_quote_on_timer(self, feed_name, quote_getter, frequency):
        self._register_activity(feed_name, Activity(quote_getter, frequency))

    """ Interface implemented by Feed subclass """
    def feed_init(self):
        raise NotImplementedError("Feed subclasses must implement this.")

    def handle_symbol_request(symbol_request):
        raise NotImplementedError("Feed subclasses must implement this.")

