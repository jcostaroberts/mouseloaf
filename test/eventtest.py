#!/usr/bin/env python

import os
from mouseloaf.event import Activity
from mouseloaf.event import AuxData
from mouseloaf.event import Coordinator
from mouseloaf.event import Message
from mouseloaf.actor import Actor

"""
This is a basic sanity test on the event infrastructure.

First we instantiate a Coordinator.

Curly registers an activity that writes to a file every half second.

Larry registers an activity that reads the file every quarter second,
publishing the new contents in a LarryMessage.

Moe wants to learn all six of Curly's sayings so he subscribes to
Larry's messages, providing the Coordinator with the handler he
wishes to invoke to receive Larry's messages. He also registers an
auxiliary data structure called "finished" that he'll use to signal
that he has received all of Curly's sayings.

Curly has registered an activity to check whether Moe is finished.
He checks Moe's "finished" data every 20 seconds; once he sees Moe
is finished, Curly exits the program.
"""

curly_sayings = ["Nyuk nyuk nyuk!\n",
                 "Woop woop woop woop!\n",
                 "I'm a victim of circumstance.\n",
                 "Soitenly!\n",
                 "Wise guy!\n",
                 "Say a few syllables!\n"]

curly_file = "/tmp/curly.txt"

def write_curly_file(data, new=False):
    if new:
        try:
            os.remove(curly_file)
        except:
            pass
    f = open(curly_file, "a")
    if data:
        f.write(data)
    f.close()

def read_curly_file():
    f = open(curly_file)
    lines = f.readlines()
    f.close()
    return lines

class LarryFinished(object):
    def __init__(self, finished):
        self.finished = finished

class Curly(Actor):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        super(Curly, self).__init__(coordinator)
        self.lines_written = 0

        # Define and register two activities
        self.write_act = Activity(self.write_to_file, 0.5)
        self.finished_act = Activity(self.check_finished, 0.2)
        self._register_activity("write", self.write_act)
        self._register_activity("finished", self.finished_act)

        # Make sure file is empty and present
        write_curly_file("", new=True)

    def write_to_file(self):
        if self.lines_written < len(curly_sayings):
            write_curly_file(curly_sayings[self.lines_written])
            self.lines_written += 1

    def check_finished(self):
        if self._auxiliary_data("finished").data.finished:
            # Check that Curly can't write to it
            self._auxiliary_data("finished").data.finished = False
            assert self._auxiliary_data("finished").data.finished

            # Shut down event loop or it'll run forever
            self.coordinator.stop()
            print "---------------------------"
            print "Test completed successfully"

class Larry(Actor):
    larry_message = "LARRYMESSAGE"
    def __init__(self, coordinator):
        super(Larry, self).__init__(coordinator)
        self.activity = Activity(self.curly_reader, 0.25)
        self._register_activity(self.name, self.activity)
        self.lines_received = 0

    def curly_reader(self):
        lines = read_curly_file()
        if len(lines) > self.lines_received:
            message = Message(self.name, self.larry_message, lines[-1])
            self._publish(message)
            self.lines_received += 1

class Moe(Actor):
    def __init__(self, coordinator):
        super(Moe, self).__init__(coordinator)
        self.lines_received = 0
        self._subscribe("Larry", self.larry_handler)
        self.finished = AuxData(LarryFinished(False), self.name, False)
        self._register_auxiliary_data("finished", self.finished)

    def larry_handler(self, message):
        assert message.data == curly_sayings[self.lines_received]
        print message.data[:-1]
        self.lines_received += 1
        if self.lines_received == len(curly_sayings):
            self.finished.data.finished = True


coord = Coordinator()
curly = Curly(coord)
larry = Larry(coord)
moe = Moe(coord)
coord.loop()
