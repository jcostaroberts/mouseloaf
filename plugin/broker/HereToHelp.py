#!/usr/bin/env python

from broker import BrokerBase
from datetime import datetime

class HereToHelp(BrokerBase):
    def broker_init(self):
        pass

    def handle_order(self, order_id, symbol, quantity, limit_price, stop_price):
        print "[%s] Broker %s received order %s for %d shares of %s at %f/share" % \
                (datetime.now(), self.name, order_id, quantity, symbol, limit_price)
        self._report_order_status(order_id,
                                  status=BrokerBase.FILLED,
                                  filled=quantity,
                                  remaining=0,
                                  price=0.01)
