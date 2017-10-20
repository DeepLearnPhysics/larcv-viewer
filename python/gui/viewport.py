
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import numpy

class viewport(pg.GraphicsLayoutWidget):


  def __init__(self,plane=-1):
    super(viewport, self).__init__(border=None)

    # add a view box, which is a widget that allows an image to be shown
    self._plot = self.addPlot(border=None)

    # add an image item which handles drawing (and refreshing) the image
    self._item = pg.ImageItem(useOpenGL=True)

    self._plot.addItem(self._item)

    # # connect the scene to click events, used to get wires
    # self.scene().sigMouseClicked.connect(self.mouseClicked)
    # # connect the views to mouse move events, used to update the info box at the bottom
    self.scene().sigMouseMoved.connect(self.mouseMoved)
    self._plane = plane

    self._x_axis = self._plot.getAxis("bottom")
    self._y_axis = self._plot.getAxis("left")

    self._x_max_range = (-1, 1)
    self._y_max_range = (-1, 1)

    # Set up the blank data:
    self.setBackground('w')

    # each drawer contains its own color gradient and levels
    # this class can return a widget containing the right layout for everything
    # Define some color collections:

    self._bwMap = {'ticks': [(0, (0,0,0,255)),
                             (1, (255, 255, 255))],
                   'mode' : 'rgb'}

    self._colorMap = {'ticks': [(0, (30, 30, 255, 255)),
                       (0.33333, (0, 255, 255, 255)), 
                       (0.66666, (255,255,100,255)), 
                       (1, (255, 0, 0, 255))], 
                     'mode': 'rgb'}

    self._activeMap = self._bwMap

    self._cmap = pg.GradientWidget(orientation='right')
    self._cmap.restoreState(self._activeMap)
    self._cmap.sigGradientChanged.connect(self.refreshGradient)
    self._cmap.resize(1,1)

    # These boxes control the levels.
    self._upperLevel = QtGui.QLineEdit()
    self._lowerLevel = QtGui.QLineEdit()

    self._upperLevel.returnPressed.connect(self.levelChanged)
    self._lowerLevel.returnPressed.connect(self.levelChanged)

    self._lowerLevel.setText(str(-10))
    self._upperLevel.setText(str(10))


    # Fix the maximum width of the widgets:
    self._upperLevel.setMaximumWidth(35)
    self._cmap.setMaximumWidth(25)
    self._lowerLevel.setMaximumWidth(35)

    colors = QtGui.QVBoxLayout()
    colors.addWidget(self._upperLevel)
    colors.addWidget(self._cmap)
    colors.addWidget(self._lowerLevel)
    self._totalLayout = QtGui.QHBoxLayout()
    self._totalLayout.addWidget(self)
    self._totalLayout.addLayout(colors)
    self._widget = QtGui.QWidget()
    self._widget.setLayout(self._totalLayout)

  def falseColor(self, apply_fc):
    if apply_fc:
      self._activeMap = self._colorMap
    else:
      self._activeMap = self._bwMap
    self._cmap.restoreState(self._activeMap)
    self.refreshGradient()

  def restoreDefaults(self):
    self._lowerLevel.setText(str(self._geometry.getLevels(self._plane)[0]))
    self._upperLevel.setText(str(self._geometry.getLevels(self._plane)[1]))

    self._cmap.restoreState(self._activeMap)

  def mouseDrag(self):
    print "mouse was dragged"

  def getWidget(self):
    return self._widget, self._totalLayout

  def levelChanged(self):
    # First, get the current values of the levels:
    lowerLevel = int(self._lowerLevel.text())
    upperLevel = int(self._upperLevel.text())

    # set the levels as requested:
    levels = (lowerLevel, upperLevel)

    # last, update the levels in the image:
    self._item.setLevels(levels)

  def refreshGradient(self):
    self._item.setLookupTable(self._cmap.getLookupTable(255))

  def mouseMoved(self, pos):


    self.q = self._item.mapFromScene(pos)
    self._lastPos = self.q
    if (pg.Qt.QtVersion.startswith('4')):
      message= QtCore.QString()
    else:
      message= str()
    if type(message) != str:
      message.append("X: ")
      message.append("{0:.1f}".format(self.q.x()))
    else:
      message += "X: "
      message += "{0:.1f}".format(self.q.x())
    if type(message) != str:
      message.append(", Y: ")
      message.append("{0:.1f}".format(self.q.y()))
    else:
      message += ", Y: "
      message += "{0:.1f}".format(self.q.y())
    

    # print message
    # if self.q.x() > 0 and self.q.x() < self._geometry.wRange(self._plane):
    #   if self.q.y() > 0 and self.q.y() < self._geometry.tRange():
    self._statusBar.showMessage(message)

  def updateRange(self, meta):

    # create the sets of ticks to update the image with:
    # Format is
    # [
    # [ (majorTickValue1, majorTickString1), (majorTickValue2, majorTickString2), ... ],
    # [ (minorTickValue1, minorTickString1), (minorTickValue2, minorTickString2), ... ],
    # ...
    # ]

    # Major ticks are the pixel widths, or 1
    # Minor ticks are 1
    x_major_tick_vals   = numpy.arange(meta.cols(), step=50)
    self._x_max_range = (x_major_tick_vals[-1], x_major_tick_vals[0])
    x_major_tick_labels = numpy.arange(meta.min_x(), meta.max_x(), 50*int(meta.pixel_width()))
    x_major = numpy.column_stack((x_major_tick_vals, x_major_tick_labels))

    x_minor_tick_vals = numpy.arange(int(meta.width()))
    x_minor_tick_labels = numpy.arange(meta.min_x(), meta.max_x(), 1)
    x_minor = numpy.column_stack((x_minor_tick_vals, x_minor_tick_labels))

    x_ticks = [x_major, x_minor]

    y_major_tick_vals   = numpy.arange(meta.rows(), step=50)
    self._y_max_range = (y_major_tick_vals[-1], y_major_tick_vals[0])
    y_major_tick_labels = numpy.arange(meta.min_y(), meta.max_y(), 50*int(meta.pixel_height()))
    y_major = numpy.column_stack((y_major_tick_vals, y_major_tick_labels))
    
    y_minor_tick_vals = numpy.arange(int(meta.height()))
    y_minor_tick_labels = numpy.arange(meta.min_y(), meta.max_y(), 1)
    y_minor = numpy.column_stack((y_minor_tick_vals, y_minor_tick_labels))

    y_ticks = [y_major, y_minor]

    self._x_axis.setTicks(x_ticks)
    self._y_axis.setTicks(y_ticks)

    self.setRangeToMax()

  def connectStatusBar(self, _statusBar):
    self._statusBar = _statusBar

  def setRangeToMax(self):
    self._plot.setRange(xRange=self._x_max_range,yRange=self._y_max_range, padding=0.002)



  def plane(self):
    return self._plane

  def lockRatio(self, lockAR ):
    ratio = (self._x_max_range[1] - self._x_max_range[0]) / (self._y_max_range[1] - self._y_max_range[0])
    if lockAR:
      self._plot.setAspectLocked(True, ratio=ratio)
    else:
      self._plot.setAspectLocked(False)

  def drawPlane(self, image):
    self._item.setImage(image,autoLevels=False)
    self._item.setLookupTable(self._cmap.getLookupTable(255))
    self._cmap.setVisible(True)
    self._upperLevel.setVisible(True)
    self._lowerLevel.setVisible(True)
    self._item.setVisible(False)
    self._item.setVisible(True)
    # Make sure the levels are actually set:
    self.levelChanged()

  def drawBlank(self):
    self._item.clear()
    self._cmap.setVisible(True)
    self._upperLevel.setVisible(True)
    self._lowerLevel.setVisible(True)





