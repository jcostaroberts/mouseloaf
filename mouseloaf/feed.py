#!/usr/bin/env python

from actor import Actor
from event import Activity
from plugin import PluginRegistry


class FeedBase(Actor):
    __metaclass__=PluginRegistry
    def __init__(self, config, coordinator):
        super(FeedBase, self).__init__(coordinator)
        self._feed_init()

    """ API exposed to Feed subclasses """
    def _publish_data(self, data):
        self._publish(data)

    def _get_quote_on_timer(self, feed_name, quote_getter, frequency):
        self._register_activity(feed_name, Activity(quote_getter, frequency))

    """ Interface implemented by Feed subclass """
    def _feed_init(self):
        raise NotImplementedError("Feed subclasses must implement this.")
