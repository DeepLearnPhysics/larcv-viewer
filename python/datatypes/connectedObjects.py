from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

# This class wraps the hit object to allow them to all function together
class connectedBox(QtGui.QGraphicsRectItem):

    """docstring for connectedBox"""

    def __init__(self, *args, **kwargs):
        super(connectedBox, self).__init__(*args)
        self.setAcceptHoverEvents(True)
        self._isHighlighted = False

    def hoverEnterEvent(self, e):
        self.setToolTip(self._ownerToolTip())
        self._ownerHoverEnter(e)

    def hoverLeaveEvent(self, e):
        self._ownerHoverExit(e)

    def mouseDoubleClickEvent(self, e):
        self._toggleHighlight()

    def connectOwnerHoverEnter(self, ownerHoverEnter):
        self._ownerHoverEnter = ownerHoverEnter

    def connectOwnerHoverExit(self, ownerHoverExit):
        self._ownerHoverExit = ownerHoverExit

    def connectToggleHighlight(self, ownerTH):
        self._toggleHighlight = ownerTH

    def connectToolTip(self, ownerToolTip):
        self._ownerToolTip = ownerToolTip


class connectedCircle(QtGui.QGraphicsEllipseItem):

    """docstring for connectedCircle"""

    def __init__(self, *args, **kwargs):
        super(connectedCircle, self).__init__(*args, **kwargs)
        self.setAcceptHoverEvents(True)
        self._isHighlighted = False

    def hoverEnterEvent(self, e):
        self.setToolTip(self._ownerToolTip())
        self._ownerHoverEnter(e)

    def hoverLeaveEvent(self, e):
        self._ownerHoverExit(e)

    def mouseDoubleClickEvent(self, e):
        self._toggleHighlight()

    def connectOwnerHoverEnter(self, ownerHoverEnter):
        self._ownerHoverEnter = ownerHoverEnter

    def connectOwnerHoverExit(self, ownerHoverExit):
        self._ownerHoverExit = ownerHoverExit

    def connectToggleHighlight(self, ownerTH):
        self._toggleHighlight = ownerTH

    def connectToolTip(self, ownerToolTip):
        self._ownerToolTip = ownerToolTip


class boxCollection(QtCore.QObject):
    # This class wraps a collection of hits and connects them together
    # it can draw and delete itself when provided with view_manage
    #
    mouseEnter = QtCore.pyqtSignal(QtGui.QGraphicsSceneHoverEvent)
    mouseExit = QtCore.pyqtSignal(QtGui.QGraphicsSceneHoverEvent)
    highlightChange = QtCore.pyqtSignal()

    def __init__(self):
        super(boxCollection, self).__init__()
        self._color = (0, 0, 0)
        self._plane = -1
        self._listOfHits = []
        self._isHighlighted = False
        self._acceptHoverEvents = False
        self._label = None

    def setColor(self, color):
        self._color = color

    def setPlane(self, plane):
        self._plane = plane

    def attachParams(self, params):
        self._params = params

    # Can connect boxCollections to other boxCollections or to cluster params
    def connect(self, other):
        self.mouseEnter.connect(other.hoverEnter)
        self.mouseExit.connect(other.hoverExit)
        self.highlightChange.connect(other.toggleHighlight)

    def setLabel(self, label):
        self._label = label

    def genToolTip(self):
        nhits = len(self._listOfHits)
        tip = "Hits: " + str(nhits)
        if self._label is not None:
            tip += "\nLabel: {}".format(self._label)
        return tip

    def hoverEnter(self, e):
        for hit in self._listOfHits:
            hit.setPen(pg.mkPen((0, 0, 0), width=1))
        # When the function is called from a box, the sender is none
        # When its passed from the params, the sender is something
        if self.sender() == None:
            self.mouseEnter.emit(e)

    def hoverExit(self, e):
        if self._isHighlighted:
            return
        for hit in self._listOfHits:
            hit.setPen(pg.mkPen(None))
        # When the function is called from a box, the sender is none
        # When its passed from the params, the sender is something
        if self.sender() == None:
            self.mouseExit.emit(e)

    def toggleHighlight(self):
        self._isHighlighted = not self._isHighlighted
        # When the function is called from a box, the sender is none
        # When its passed from the params, the sender is something
        if self.sender() == None:
            self.highlightChange.emit()

    def drawHits(self, view, cluster, meta):
        for i in xrange(cluster.as_vector().size()):
            voxel = cluster.as_vector()[i]
            col = meta.col(meta.position(voxel.id()).x)
            row = meta.row(meta.position(voxel.id()).y)
            # Draws a rectangle at (x,y,xlength, ylength)
            # print "Drawing voxel at ({}, {})".format(voxel.X(), voxel.Y())
            r = connectedBox(col, row, 1, 1) #, voxel.Width())
            r.setPen(pg.mkPen(None))
            r.setBrush(pg.mkColor(self._color))
            self._listOfHits.append(r)
            view._plot.addItem(r)

            # Connect the voxel's actions with the clusters functions
            r.connectOwnerHoverEnter(self.hoverEnter)
            r.connectOwnerHoverExit(self.hoverExit)
            r.connectToggleHighlight(self.toggleHighlight)
            r.connectToolTip(self.genToolTip)

    def clearHits(self, view):
        for voxel in self._listOfHits:
            view._plot.removeItem(voxel)
        self._listOfHits = []
        self._label = None