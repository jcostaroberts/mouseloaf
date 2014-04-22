#!/usr/bin/env python

import uuid
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

class Order(Message):
    def __init__(self, symbol, quantity, limit_price=None,
                 stop_price=None):
        self.order_id = uuid.uuid1()
        self.symbol = symbol
        self.quantity = quantity
        self.limit_price = limit_price
        self.stop_price = stop_price

class OrderStatus(Message):
    def __init__(self, order_id, status, filled=0, remaining=0, price=None):
        self.order_id = order_id
        self.status = status
        self.filled = filled
        self.remaining = remaining
        self.price = price

"""
Coordinator should deal with Messages, each of which has a string msg_type().
The Message class will be defined in the event module. Then the next layer
will implement a sort of protocol that defines several message types.
The *Base classes know about and use these types. Message subclasses are
responsible for setting the message types if they want something other than
a string of the subclass' name. The base classes also have to subscribe to
these types, and translate between the messages whizzing around and the
handler implementations they call. This way the base classes can do type
checking and it simplifies the implementors' job.
"""
