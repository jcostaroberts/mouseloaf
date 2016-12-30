#!/usr/bin/env python

from broker import BrokerBase
from datetime import datetime

HistoricalDataOrder = namedtuple("HistoricalDataOrder",
                                 ["order_id",
                                  "symbol",
                                  "quantity",
                                  "limit_price",
                                  "stop_price"])

class HistoricalDataBroker(BrokerBase):
    # - Come up with some generic way of specifying fee structure
    def broker_init(self):
        self.active_limit_orders = {} # by symbol

    def feed_init(self):
        # - Set start time.
        # - do setup for tracking symbols
        self.symbols = []
        self._get_quote_on_timer(self.name, self._get_quotes, 0)

    def _complete_trade(self):
        # - calculate fees
        # - update portfolio
        # - publish order status successful
        self._report_order_status(stuff)

    def _complete_active_limit_orders(self, quote):
        # - check whether the quote satisfies any outstanding order
        completed = []
        if symbol in self.active_limit_orders:
            for order in self.active_limit_orders[symbol]:
                if order.order_type == "BUY" and order.limit_price <= quote:
                    completed.append(order)
                    self._complete_trade()
            for c in completed:
                # delete from list
                pass

    def _get_quotes(self):
        # - move forward one time step
        # - get the next line of data for each symbol we care
        #   about
        for symbol in self.symbols:
            quote = self._get_next_quote(symbol)
            self._complete_active_limit_orders(quote)
            self._publish_data(stuff)

    def seed_portfolio(self):
        pass

    def handle_symbol_request(self, symbol):
        # pull in data and get up to current time with it
        pass
    
    def handle_order(self, order_id, symbol, quantity,
                     limit_price, stop_price):
        if limit_price:
            # limit order; store it
            if symbol not in self.active_limit_orders:
                self.active_limit_orders[symbol] = {}
            o = HistoricalDataOrder(order_id, symbol, quantity,
                                    limit_price, stop_price)
            self.active_limit_orders[symbol][order_id] = o
        else:
            # market order; take it and update portfolio
            pass
