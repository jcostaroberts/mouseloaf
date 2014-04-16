#!/usr/bin/env python

from broker import BrokerBase

class HereToHelp(BrokerBase):
    def _broker_init(self):
        pass

    def _handle_order(self, order):
        from datetime import datetime
        print "[%s] Broker %s received message %s" % (str(datetime.now()), self.name, order)
        self._report_order_status("ORDER_SUCCESSFUL")
