#!/usr/bin/env python

from datetime import datetime
from feed import FeedBase

class EverythingIsFree(FeedBase):
    def feed_init(self):
        self.symbols = []
        self._get_quote_on_timer(self.name, self._get_quote, 1)

    def _get_quote(self):
        for s in self.symbols:
            self._publish_data(s, ask_price=0.01)

    def handle_symbol_request(self, symbol):
        self.symbols.append(symbol)
        print "[%s] Feed %s received request for ticker %s" % \
                (datetime.now(), self.name, symbol)
