#!/usr/bin/env python

from broker import BrokerBase
from datetime import datetime
from strategy import StrategyBase

class Buy(StrategyBase):
    def strategy_init(self):
        self.sid = "BOGUS"
        self._request_symbol(self.sid)
        self.portfolio = self._auxiliary_data("portfolio").data

    def place_limit_order(self):
        order_id = self._place_order(self.sid, quantity=1, limit_price=0.01)

    def handle_order_status(self, order_id, status, filled, remaining, price):
        assert status == BrokerBase.FILLED
        print "[%s] Strategy %s received order status FILLED for order %s:" % \
                (str(datetime.now()), self.name, order_id)
        print "  %d shares of %s at %f/share" % (filled,
                                                 self.sid,
                                                 price)

    def handle_feed_data(self, symbol, exchange, time,
                         bid_price, bid_quantity,
                         ask_price, ask_quantity):
        print "[%s] Strategy %s received feed data: %s is %f/share" % \
                (datetime.now(), self.name, symbol, ask_price)
        if self.portfolio.cash > 0:
            self.place_limit_order()
        else:
            print "[%s] Strategy %s is out of money!" % (datetime.now(),
                                                         self.name)
            f = open("/tmp/test.out", "w")
            f.write("Success")
            f.close()
            self.coordinator.stop()
