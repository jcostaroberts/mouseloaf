#!/usr/bin/env python

from event import Message

class FeedData(Message):
    def __init__(self, symbol, exchange=None, time=None,
                 bid_price=None, bid_quantity=None,
                 ask_price=None, ask_quantity=None):
        self.symbol = symbol
        self.exchange = exchange
        self.time = time
        self.bid_price = bid_price
        self.bid_quantity = bid_quantity
        self.ask_price = ask_price
        self.ask_quantity = ask_quantity

   def msg_type(self):
       return "%s-%s" % (self._msg_type(), self.symbol)

class SymbolRequest(Message):
    def __init__(self, symbol):
        self.symbol = symbol

"""
Coordinator should deal with just simple message types, which are strings.
The Message type will be defined in the event module. Then the next layer
will implement a sort of protocol that defines several message types.
The *Base classes know about and use these types. Messages have types.
Message subclasses are responsible for setting those types and for 
subscribing to the riht types, etc.
StrategyBAse
"""
