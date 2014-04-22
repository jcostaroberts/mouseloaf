#!/usr/bin/env python

class Actor(object):

    def __init__(self, coordinator):
        #self.name = "%s-%s" % \
        #    (self.__class__.__bases__[0].__name__.replace("Base", ""),
        #     self.__class__.__name__)
        self.name = self.__class__.__name__
        self.coordinator = coordinator

    """ API exposed to subclasses """
    def _subscribe(self, publisher, handler):
        self.coordinator.subscribe(self.name, publisher, handler)

    def _publish(self, message):
        self.coordinator.publish(self.name, message)

    def _register_activity(self, activity_name, activity):
        self.coordinator.register_activity(activity_name, self.name, activity)

    def _register_auxiliary_data(self, name, data):
        return self.coordinator.register_auxiliary_data(name, data)

    def _auxiliary_data(self, name):
        return self.coordinator.auxiliary_data(self.name, name)
