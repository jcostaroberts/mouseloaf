#!/usr/bin/env python

import copy
from collections import namedtuple
from proxy import ReadOnlyProxy
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

Activity = namedtuple("Activity", ["activity", "frequency"])
AuxData = namedtuple("AuxData", ["data", "owner", "writable"])

class Message(object):
    def _msg_type(self):
        return self.__class__.__name__

    def msg_type(self):
        return self._msg_type()

class Coordinator(object):
    def __init__(self):
        self.handlers_ = {}
        self.activities_ = {}
        self.auxiliary_ = {}

    def subscribe(self, subscriber, msg_type, handler):
        if msg_type not in self.handlers_:
            self.handlers_[msg_type] = {}
        if subscriber not in self.handlers_[msg_type]:
            self.handlers_[msg_type][subscriber] = handler

    def publish(self, publisher, message):
        msg_type = message.msg_type()
        for subscriber in self.handlers_[msg_type]:
            message_copy = copy.deepcopy(message)
            self.handlers_[msg_type][subscriber](message_copy)

    def register_activity(self, name, publisher, activity):
        assert type(activity) == Activity, "Must register an Activity"
        if publisher not in self.activities_:
            self.activities_[publisher] = {}
        self.activities_[publisher][name] = activity

    def register_auxiliary_data(self, name, aux_data):
        assert type(aux_data) == AuxData, "Must register an AuxData"
        if name not in self.auxiliary_:
            if not aux_data.writable:
                self.auxiliary_[name] = ReadOnlyProxy(aux_data)
            else:
                self.auxiliary_[name] = aux_data
        return self.auxiliary_[name]

    def auxiliary_data(self, accessor, name):
        if name not in self.auxiliary_:
            return None
        return self.auxiliary_[name]

    def loop(self):
        for publisher in self.activities_:
            for activity_name in self.activities_[publisher]:
                activity = self.activities_[publisher][activity_name]
                lc = LoopingCall(activity.activity)
                lc.start(activity.frequency, now=False)
        reactor.run()

    def stop(self):
        reactor.stop()

