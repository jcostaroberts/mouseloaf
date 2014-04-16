#!/usr/bin/env python

import sys
from os import path
from event import Coordinator
from plugin import load_plugins

class Config(object):
    feed = "EverythingIsFree"
    strategy = "Buy"
    broker = "HereToHelp"
    plugins = [feed, strategy, broker]

def parse_config():
    config = Config()
    return config

def main():
    pdir = path.join(path.split(path.dirname(sys.argv[0]))[0], "plugin")

    config = parse_config()
    plugins = load_plugins(pdir, config.plugins)
    coordinator = Coordinator()
    modules = [ P(config, coordinator) for P in plugins ]

    coordinator.loop()

if __name__ == "__main__":
    main()
