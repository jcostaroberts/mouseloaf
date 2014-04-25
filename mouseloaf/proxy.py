#!/usr/bin/env python

class ReadOnlyProxyException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ReadOnlyProxy(object):
    def __init__(self, obj):
        object.__setattr__(self, "_obj", obj)

    def __getattr__(self, attrib):
        return getattr(self._obj, attrib)

    def __setattr__(self, attrib, value):
        raise ReadOnlyProxyException("Attempt to set proxy attribute '%s'" % attrib)

