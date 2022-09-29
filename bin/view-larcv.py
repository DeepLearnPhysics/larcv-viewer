#!/usr/bin/env python

import larcv

def monkeypatch_ctypes():
    import os
    import ctypes.util
    uname = os.uname()
    if uname.sysname == "Darwin" and uname.release >= "20.":
        real_find_library = ctypes.util.find_library
        def find_library(name):
            if name in {"OpenGL", "GLUT"}:  # add more names here if necessary
                return f"/System/Library/Frameworks/{name}.framework/{name}"
            return real_find_library(name)
        ctypes.util.find_library = find_library
    return
monkeypatch_ctypes()


# from gui import evdgui
import argparse
import sys
import signal
from pyqtgraph.Qt import QtWidgets, QtCore

from manager import evd_manager_2D

import os
import json

# This is to allow key commands to work when focus is on a box

from gui import evdgui


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    sys.exit()


def main():

    parser = argparse.ArgumentParser(description='Python based event display.')
    parser.add_argument("-c", "-C", "--config", help="Optional config file override.")
    parser.add_argument('file', nargs='*', help="Optional input file to use")

    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)

    if args.config is None:
      print("No config supplied, using default configuration file.")
      args.config = larcv.ProcessDriver.default_config()
    # Else, convert it to json:
    else:
        with open(args.config, 'rb') as f:
            args.config = json.load(f)

    print(args.config)

    # If a file was passed, give it to the manager:
    if len(args.file) > 0:
        # Make sure the keys exist:
        if "IOManager" not in args.config:
            args.config["IOManager"] = {}
        if "Input" not in args.config["IOManager"]:
            args.config["IOManager"]["Input"] = {}

        args.config['IOManager']['Input']['InputFiles'] = args.file


    manager = evd_manager_2D(args.config)


    thisgui = evdgui()
    thisgui.connect_manager(manager)
    # manager.goToEvent(0)
    thisgui.initUI()

    manager.eventChanged.connect(thisgui.update)
    manager.metaRefreshed.connect(thisgui.metaChanged)


    signal.signal(signal.SIGINT, sigintHandler)
    timer = QtCore.QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.

    app.exec_()
    # sys.exit(app.exec_())


if __name__ == '__main__':
    main()
