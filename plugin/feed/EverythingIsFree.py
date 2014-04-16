#!/usr/bin/env python

from feed import FeedBase

class EverythingIsFree(FeedBase):
    def _feed_init(self):
        self._get_quote_on_timer(self.name, self._getquote, 1)

    def _getquote(self):
        self._publish_data("EVERYTHING IS FREE")
