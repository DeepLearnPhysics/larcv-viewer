#!/usr/bin/env python


# from gui import evdgui
import argparse
import sys
import signal
from pyqtgraph.Qt import QtGui, QtCore
import larcv

try:
    import pyqtgraph.opengl as gl

except:
    print("Must have opengl to use the 3D viewer, exiting.")
    exit()

from gui import evdgui3D
from manager import evd_manager_3D
import os


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    sys.exit()


def main():

    parser = argparse.ArgumentParser(description='Python based event display.')
    parser.add_argument("-c", "-C", "--config", help="Optional config file override.")
    parser.add_argument('file', nargs='*', help="Optional input file to use")

    args = parser.parse_args()

    app = QtGui.QApplication(sys.argv)

    if args.config is None:
      print("No config supplied, using default configuration file.")
      args.config = larcv.ProcessDriver.default_config()


    # If a file was passed, give it to the manager:

    manager = evd_manager_3D(args.config, args.file)


    thisgui = evdgui3D()
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
