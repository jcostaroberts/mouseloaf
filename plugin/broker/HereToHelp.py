#!/usr/bin/env python

from broker import BrokerBase
from datetime import datetime

class HereToHelp(BrokerBase):
    def broker_init(self):
        pass

    def handle_order(self, order_id, symbol, quantity, limit_price, stop_price):
        print "[%s] Broker %s received order %s for %d shares of %s at %f/share" % \
                (datetime.now(), self.name, order_id, quantity, symbol, limit_price)
        # XXX_jcr: unless we're guaranteed to return to the
        # activity loop between calling report_order_status
        # and when the strategy's callback fires, there's a
        # weird ordering issue here where we have to make
        # portfolio changes before the _report() call,
        # which sucks.
        self.portfolio.cash -= quantity*0.01
        self._report_order_status(order_id,
                                  status=BrokerBase.FILLED,
                                  filled=quantity,
                                  remaining=0,
                                  price=0.01)

    def seed_portfolio(self):
        self.portfolio.cash = 0.10
