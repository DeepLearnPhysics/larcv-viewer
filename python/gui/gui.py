

import sys, signal
import argparse
# import collections
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

# import evdmanager
from view_manager import view_manager

class gui(QtGui.QWidget):

  def __init__(self):
    super(gui, self).__init__()

    # initUI should not do ANY data handling, it should only get the interface loaded
    self._view_manager = view_manager()

  def connect_manager(self,manager):
    self._event_manager = manager

  def closeEvent(self, event):
    self.quit()  

  def quit(self):
    # if self._running:
      # self.stopRun()
    QtCore.QCoreApplication.instance().quit()

  def metaChanged(self, meta):
    self._event_manager.refresh_meta()
    for view in self._view_manager.getViewPorts():
      view.updateRange(meta.meta(view.plane()))

  def update(self):
    # set the text boxes correctly:
    self._fileEntry.setText(str(self._event_manager.entry()))

    eventLabel = "Ev: " + str(self._event_manager.event())
    self._eventLabel.setText(eventLabel)
    runLabel = "Run: " + str(self._event_manager.run())
    self._runLabel.setText(runLabel)
    subrunLabel = "Subrun: " + str(self._event_manager.subrun())
    self._subrunLabel.setText(subrunLabel)
    self.metaChanged(self._event_manager.meta())
    
    self._event_manager.drawFresh(self._view_manager)

  # This function prepares the buttons such as prev, next, etc and returns a layout
  def getEventControlButtons(self):

    # This is a box to allow users to enter an event (larlite numbering)
    self._goToLabel = QtGui.QLabel("Go to: ")
    self._fileEntry = QtGui.QLineEdit()
    self._fileEntry.setToolTip("Enter an event to skip to that event (sequential numbering")
    self._fileEntry.returnPressed.connect(self.goToEventWorker)
    # These labels display current events
    self._runLabel = QtGui.QLabel("Run: 0")
    self._eventLabel = QtGui.QLabel("Ev.: 0")
    self._subrunLabel = QtGui.QLabel("Subrun: 0")

    # Jump to the next event
    self._nextButton = QtGui.QPushButton("Next")
    # self._nextButton.setStyleSheet("background-color: red")
    self._nextButton.clicked.connect(self._event_manager.next)
    self._nextButton.setToolTip("Move to the next event.")
    # Go to the previous event
    self._prevButton = QtGui.QPushButton("Previous")
    self._prevButton.clicked.connect(self._event_manager.prev)
    self._prevButton.setToolTip("Move to the previous event.")

    # pack the buttons into a box
    self._eventControlBox = QtGui.QVBoxLayout()

    # Make a horiztontal box for the event entry and label:
    self._eventGrid = QtGui.QHBoxLayout()
    self._eventGrid.addWidget(self._goToLabel)
    self._eventGrid.addWidget(self._fileEntry)
    # Another horizontal box for the run/subrun
    # self._runSubRunGrid = QtGui.QHBoxLayout()
    # self._runSubRunGrid.addWidget(self._eventLabel)
    # self._runSubRunGrid.addWidget(self._runLabel)
    # Pack it all together
    self._eventControlBox.addLayout(self._eventGrid)
    self._eventControlBox.addWidget(self._eventLabel)
    self._eventControlBox.addWidget(self._runLabel)
    self._eventControlBox.addWidget(self._subrunLabel)
    self._eventControlBox.addWidget(self._nextButton)
    self._eventControlBox.addWidget(self._prevButton)

    return self._eventControlBox
  

  # this function helps pass the entry of the line edit item to the event control
  def goToEventWorker(self):
    print "called goToEventWorker"
    try:
      event = int(self._fileEntry.text())
    except:
      print("Error, must enter an integer")
      self._fileEntry.setText(str(self._event_manager.entry()))
      return
    self._event_manager.go_to_entry(event)

  # This function prepares the range controlling options and returns a layout
  def getDrawingControlButtons(self):

    # Button to set range to max
    self._maxRangeButton = QtGui.QPushButton("Max Range")
    self._maxRangeButton.setToolTip("Set the range of the viewers to show the whole event")
    self._maxRangeButton.clicked.connect(self._view_manager.setRangeToMax)

    self._lockAspectRatio = QtGui.QCheckBox("Lock A.R.")
    self._lockAspectRatio.setToolTip("Lock the aspect ratio to 1:1")
    self._lockAspectRatio.stateChanged.connect(self.lockARWorker)

    self._falseColorSelection = QtGui.QCheckBox("False Color")
    self._falseColorSelection.setToolTip("Applies a false color scheme to images")
    self._falseColorSelection.stateChanged.connect(self.falseColorWorker)

    # add a box to restore the drawing defaults:
    self._restoreDefaults = QtGui.QPushButton("Restore Defaults")
    self._restoreDefaults.setToolTip("Restore the drawing defaults of the views.")
    self._restoreDefaults.clicked.connect(self.restoreDefaultsWorker)

    # Pack the stuff into a layout

    self._drawingControlBox = QtGui.QVBoxLayout()
    self._drawingControlBox.addWidget(self._restoreDefaults)
    self._drawingControlBox.addWidget(self._maxRangeButton)
    self._drawingControlBox.addWidget(self._lockAspectRatio)
    self._drawingControlBox.addWidget(self._falseColorSelection)

    return self._drawingControlBox

  def viewSelectWorker(self):

    i = 0
    for i in xrange(self._event_manager.n_views()):
      if self.sender() == self._viewButtonArray[i]:
        self._view_manager.selectPlane(i)
        self._view_manager.refreshDrawListWidget()
        return
      else:
        i += 1

    # if there wasn't a match, then it must be the ALL button:
    if self.sender() != None:
      self._view_manager.selectPlane(-1)
      self._view_manager.refreshDrawListWidget()
      return


  def lockARWorker(self):
    if self._lockAspectRatio.isChecked():
      self._view_manager.lockAR(True)
    else:
      self._view_manager.lockAR(False)

  def falseColorWorker(self):
    if self._falseColorSelection.isChecked():
      for view in self._view_manager.getViewPorts():
        view.falseColor(True)
    else:
      for view in self._view_manager.getViewPorts():
        view.falseColor(False)

  def restoreDefaultsWorker(self):
    self._view_manager.restoreDefaults()
    self._view_manager.setRangeToMax()
    
  # This function prepares the quit buttons layout and returns it
  def getQuitLayout(self):
    self._quitButton = QtGui.QPushButton("Quit")
    self._quitButton.setToolTip("Close the viewer.")
    self._quitButton.clicked.connect(self.quit)
    return self._quitButton

  # This function combines the control button layouts, range layouts, and quit button
  def getWestLayout(self):

    event_control = self.getEventControlButtons()
    draw_control = self.getDrawingControlButtons()


    # Add the quit button?
    quit_control = self.getQuitLayout()
    
    self._westLayout = QtGui.QVBoxLayout()
    self._westLayout.addLayout(event_control)
    self._westLayout.addStretch(1)
    self._westLayout.addLayout(draw_control)
    self._westLayout.addStretch(1)

    # Add a section to allow users to just view one window instead of two/three
    self._viewButtonGroup = QtGui.QButtonGroup()
    # Draw all planes:
    self._allViewsButton = QtGui.QRadioButton("All")
    self._allViewsButton.clicked.connect(self.viewSelectWorker)
    self._viewButtonGroup.addButton(self._allViewsButton)

    # Put the buttons in a layout
    self._viewChoiceLayout = QtGui.QVBoxLayout()

    # Make a label for this stuff:
    self._viewChoiceLabel = QtGui.QLabel("View Options")
    self._viewChoiceLayout.addWidget(self._viewChoiceLabel)
    self._viewChoiceLayout.addWidget(self._allViewsButton)

    i = 0
    self._viewButtonArray = []
    for plane in xrange(self._event_manager.n_views()):
      button = QtGui.QRadioButton("Plane" + str(i))
      i += 1
      self._viewButtonGroup.addButton(button)
      button.clicked.connect(self.viewSelectWorker)
      self._viewButtonArray.append(button)
      self._viewChoiceLayout.addWidget(button)

    self._westLayout.addLayout(self._viewChoiceLayout)

    self._westLayout.addStretch(1)

    self._westLayout.addWidget(quit_control)
    self._westWidget = QtGui.QWidget()
    self._westWidget.setLayout(self._westLayout)
    self._westWidget.setMaximumWidth(150)
    self._westWidget.setMinimumWidth(100)
    return self._westWidget


  def getSouthLayout(self):
    # This layout contains the status bar, message bar, and the capture screen buttons

    # The screen capture button:
    self._screenCaptureButton = QtGui.QPushButton("Capture Screen")
    self._screenCaptureButton.setToolTip("Capture the entire screen to file")
    self._screenCaptureButton.clicked.connect(self.screenCapture)
    self._southWidget = QtGui.QWidget()
    self._southLayout = QtGui.QHBoxLayout()
    # Add a status bar
    self._statusBar = QtGui.QStatusBar()
    self._statusBar.showMessage("Test message")
    self._southLayout.addWidget(self._statusBar)
    self._messageBar = QtGui.QStatusBar()
    self._southLayout.addWidget(self._messageBar)
    # self._southLayout.addStretch(1)
    self._southLayout.addWidget(self._screenCaptureButton)
    self._southWidget.setLayout(self._southLayout)

    return self._southWidget

  def updateMessageBar(self,message):
    # print "Received a message: {msg}".format(msg=message)
    self._messageBar.showMessage(message)

  def getEastLayout(self):
    # This function just makes a dummy eastern layout to use.
    label = QtGui.QLabel("Dummy")
    self._eastWidget = QtGui.QWidget()
    self._eastLayout = QtGui.QVBoxLayout()
    self._eastLayout.addWidget(label)
    self._eastLayout.addStretch(1)
    self._eastWidget.setLayout(self._eastLayout)
    self._eastWidget.setMaximumWidth(200)
    self._eastWidget.setMinimumWidth(100)
    return self._eastWidget

  def refreshEastLayout(self):
    east = getEastLayout()
    self._eastLayout.setVisible(False)
    self._eastLayout.setVisible(True)

  def refreshCenterView(self):

    # for child in self.centerWidget.children():
    #   print type(child)
    #   if type(child) == QtGui.QVBoxLayout:
    #     layout = child

    # print layout.children()
    # print layout

    widget = self._view_manager.getDrawListWidget()
    # for child in widget.children():
    #   print child

    # print widget
    # print layout

    # print layout.children()

    # for i in reversed(range(self.centerWidget.layout.count())): 
        # layout.itemAt(i).widget().setParent(None)

    self.centerWidget.setVisible(False)   
    self.centerWidget.setVisible(True)   

  def initUI(self):


    # Get all of the widgets:
    self.eastWidget  = self.getEastLayout()
    self.westWidget  = self.getWestLayout()
    self.southLayout = self.getSouthLayout()

    # Area to hold data:
    nviews = self._event_manager.n_views()
    # nviews = self._baseData._nviews
    for i in range(0, nviews):
      # These boxes hold the wire/time views:
      self._view_manager.addEvdDrawer(i)

    self._view_manager.connectStatusBar(self._statusBar)

    self.centerWidget = self._view_manager.getDrawListWidget()

    # Put the layout together


    self.master = QtGui.QVBoxLayout()
    self.slave = QtGui.QHBoxLayout()
    self.slave.addWidget(self.westWidget)
    self.slave.addWidget(self.centerWidget)
    self.slave.addWidget(self.eastWidget)
    self.master.addLayout(self.slave)
    self.master.addWidget(self.southLayout)

    self.setLayout(self.master)    


    self.setGeometry(0, 0, 2400, 1600)
    self.setWindowTitle('Event Display')    
    self.setFocus()
    self.show()
    self._view_manager.setRangeToMax()

  def keyPressEvent(self,e):
    if e.key() == QtCore.Qt.Key_N:
      self._event_manager.next()
      return
    if e.key() == QtCore.Qt.Key_P:
      self._event_manager.prev()
      return
    if e.key() == QtCore.Qt.Key_C:
      # print "C was pressed"
      if e.modifiers() and QtCore.Qt.ControlModifier :
        self.quit()
        return

    # if e.key() == QtCore.Qt.Key_C:
  #     self._dataListsAndLabels['Clusters'].setFocus()
    # if e.key() == QtCore.Qt.Key_H:
  #     self._dataListsAndLabels['Hits'].setFocus()

    if e.key() == QtCore.Qt.Key_R:
      self.setRangeToMax()
      return

    super(gui, self).keyPressEvent(e)

  def screenCapture(self):
    print("Screen Capture!")
    dialog = QtGui.QFileDialog()
    r = self._event_manager.run()
    e = self._event_manager.event()
    s = self._event_manager.subrun()
    name = "evd_" + self._geometry.name() + "_R" + str(r)
    name = name + "_S" + str(s)
    name = name + "_E" + str(e) + ".png"
    f = dialog.getSaveFileName(self,"Save File",name,
        "PNG (*.png);;JPG (*.jpg);;All Files (*)")

    if pg.Qt.QT_LIB == pg.Qt.PYQT4:
      pixmapImage = QtGui.QPixmap.grabWidget(self)
      pixmapImage.save(f,"PNG")
    else:
      pixmapImage = super(gui, self).grab()
      pixmapImage.save(f[0],"PNG")


