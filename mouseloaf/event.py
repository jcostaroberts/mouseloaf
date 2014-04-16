#!/usr/bin/env python

import copy
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from collections import namedtuple

Activity = namedtuple("Activity", ["activity", "frequency"])
AuxData = namedtuple("AuxData", ["data", "owner", "writable"])
Message = namedtuple("Message", ["sender", "message_type", "data"])

class Coordinator(object):
    def __init__(self):
        self.handlers_ = {}
        self.activities_ = {}
        self.auxiliary_ = {}

    def subscribe(self, subscriber, publisher, handler):
        if publisher not in self.handlers_:
            self.handlers_[publisher] = {}
        if subscriber not in self.handlers_[publisher]:
            self.handlers_[publisher][subscriber] = handler

    def publish(self, publisher, message):
        for subscriber in self.handlers_[publisher]:
            message_copy = copy.deepcopy(message)
            self.handlers_[publisher][subscriber](message_copy)

    def register_activity(self, name, publisher, activity):
        assert type(activity) == Activity, "Must register an Activity"
        if publisher not in self.activities_:
            self.activities_[publisher] = {}
        self.activities_[publisher][name] = activity

    def register_auxiliary_data(self, name, aux_data):
        assert type(aux_data) == AuxData, "Must register an AuxData"
        if name not in self.auxiliary_:
            self.auxiliary_[name] = aux_data
        return self.auxiliary_[name]

    def auxiliary_data(self, accessor, name):
        if name not in self.auxiliary_:
            return None
        aux_data = self.auxiliary_[name]
        if accessor != aux_data.owner and not aux_data.writable:
            aux_data = copy.deepcopy(aux_data)
        return aux_data

    def loop(self):
        for publisher in self.activities_:
            for activityName in self.activities_[publisher]:
                activity = self.activities_[publisher][activityName]
                lc = LoopingCall(activity.activity)
                lc.start(activity.frequency, now=False)
        reactor.run()

    def stop(self):
        reactor.stop()

