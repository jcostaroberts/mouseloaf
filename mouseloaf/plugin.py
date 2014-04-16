#!/usr/bin/env python

import os
import imp

# Mostly lifted off Eli Bendersky

class PluginRegistry(type):
    plugins = []
    def __init__(cls, name, bases, attrs):
        if "Base" not in name:
            PluginRegistry.plugins.append(cls)

def load_plugins(plugin_dir, modules):
    loaded = []
    for root, dirs, files in os.walk(plugin_dir):
        for filename in files:
            modname, ext = os.path.splitext(filename)
            if ext == '.py' and modname in modules:
                 loaded.append(modname)
                 file, path, descr = imp.find_module(modname, [root])
                 if file:
                     mod = imp.load_module(modname, file, path, descr)
                     loaded.append(modname)
    assert set(loaded) == set(modules), \
            "Failed to load %s" % list(set(modules)-set(loaded))
    return PluginRegistry.plugins
