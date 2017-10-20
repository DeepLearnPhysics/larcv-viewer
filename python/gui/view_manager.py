from pyqtgraph.Qt import QtGui, QtCore

# Import the class that manages the view windows
from viewport import viewport


class view_manager(QtCore.QObject):
  """This class manages a collection of viewports"""


  def __init__(self):
    super(view_manager, self).__init__()
    self._nviews = 0
    self._drawerList = []
    self._cmapList = []

    self._selectedPlane = -1

    


  def addEvdDrawer(self,plane):
    self._drawerList.append(viewport(plane))
    self._nviews += 1
  
  def selectPlane(self,plane):
    self._selectedPlane = plane


  def restoreDefaults(self):
    for view in self._drawerList:
      view.restoreDefaults()


  def getDrawListWidget(self):

    self._widgetList = []

    # loop through the list and add the drawing windows and their scale
    self._widget = QtGui.QWidget()
    self._layout = QtGui.QVBoxLayout()
    self._layout.setSpacing(0)
    # self._layout.setMargin(0)
    self._layout.setContentsMargins(0,0,0,0)

    self._planeWidgets = []
    for view in self._drawerList:
      widget,layout = view.getWidget()
      self._planeWidgets.append(widget)
      self._layout.addWidget(widget,0)

    self._widget.setLayout(self._layout)

    return self._widget

  def refreshDrawListWidget(self):

    # Draw all planes:
    if self._selectedPlane == -1:
      i = 0
      for widget in self._planeWidgets:
        widget.setVisible(True)
        i += 1

    else:
      i = 0
      for widget in self._planeWidgets:
        if i == self._selectedPlane:
          widget.setVisible(True)
        else:
          widget.setVisible(False)
        i += 1


  def connectStatusBar(self,statusBar):
    for view in self._drawerList:
      view.connectStatusBar(statusBar)


  def setRangeToMax(self):
    for view in self._drawerList:
      view.setRangeToMax()

  def autoRange(self,event_manager):
    for view in self._drawerList:
      xRange,yRange = event_manager.getAutoRange(view.plane())
      view.autoRange(xRange,yRange)

  def lockAR(self, lockRatio):
    for view in self._drawerList:
      view.lockRatio(lockRatio)

 


  def getViewPorts(self):
    return self._drawerList
