#!/usr/bin/env python

from strategy import StrategyBase

class Buy(StrategyBase):
    def _strategy_init(self):
        pass

    def _handle_broker(self, data):
        from datetime import datetime
        print "[%s] Strategy %s received message %s" % (str(datetime.now()), self.name, data)

    def _handle_feed_data(self, data):
        from datetime import datetime
        print "[%s] Strategy %s received message %s" % (str(datetime.now()), self.name, data)
        self._place_order("BUY EVERYTHING")
