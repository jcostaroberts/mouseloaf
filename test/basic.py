#!/usr/bin/env python

import subprocess

conf_file = "/tmp/basic.conf"
success_file = "/tmp/test.out"

conf = """
Feed: EverythingIsFree
Strategy: Buy
Broker: HereToHelp
"""

f = open(success_file, "w")
f.write("Failure")
f.close()

f = open(conf_file, "w")
f.write(conf)
f.close()

subprocess.check_output(["./mouseloaf/mouseloaf.py",
                         "--config=%s" % conf_file])
f = open(success_file, "r")
status = f.read()
f.close()

assert status == "Success"
print "Test completed successfully"


