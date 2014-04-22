#!/usr/bin/env python

import argparse
import sys
from os import path
from event import Coordinator
from plugin import load_plugins

parser = argparse.ArgumentParser()
parser.add_argument("--config", dest="config", action="store", default=None)

class Config(object):
    def __init__(self, feed, strategy, broker):
        self.plugins = [feed, strategy, broker]

def parse_config(config_file):
    # XXX this all goes away once we have YAML
    assert config_file
    f = open(config_file, "r")
    lines = f.readlines()
    feed = None
    broker = None
    strategy = None
    for line in lines:
        if "Feed" in line:
            feed = line.split()[-1]
        elif "Strategy" in line:
            strategy = line.split()[-1]
        elif "Broker" in line:
            broker = line.split()[-1]
    assert feed and strategy and broker
    return Config(feed, strategy, broker)

def main():
    pdir = path.join(path.split(path.dirname(sys.argv[0]))[0], "plugin")
    args = parser.parse_args()
    config = parse_config(args.config)
    plugins = load_plugins(pdir, config.plugins)
    coordinator = Coordinator()
    modules = [ P(config, coordinator) for P in plugins ]

    coordinator.loop()

if __name__ == "__main__":
    main()
