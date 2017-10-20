# Import the class that manages the view windows
from viewport3D import viewport3D
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

colorMap = {'ticks': [(1, (151, 30, 22, 255)),
                      (0.791, (0, 181, 226, 255)),
                      (0.645, (76, 140, 43, 255)),
                      (0.47, (0, 206, 24, 255)),
                      (0.33333, (254, 209, 65, 255)),
                      (0, (255, 255, 255, 255))],
            'mode': 'rgb'}

class view_manager3D(QtCore.QObject):
    """This class manages a collection of viewports"""

    refreshColors = QtCore.pyqtSignal()

    def __init__(self):
        super(view_manager3D, self).__init__()
        self._view = viewport3D()


        # Define some color collections:

        self._cmap = pg.GradientWidget(orientation='right')
        self._cmap.restoreState(colorMap)
        self._cmap.sigGradientChanged.connect(self.gradientChangeFinished)
        # self._cmap.sigGradientChangeFinished.connect(self.gradientChangeFinished)
        self._cmap.resize(1, 1)

        self._lookupTable = self._cmap.getLookupTable(255, alpha=0.75)

        # These boxes control the levels.
        self._upperLevel = QtGui.QLineEdit()
        self._lowerLevel = QtGui.QLineEdit()

        self._upperLevel.returnPressed.connect(self.colorsChanged)
        self._lowerLevel.returnPressed.connect(self.colorsChanged)

        self._lowerLevel.setText(str(0.0))
        self._upperLevel.setText(str(2.0))

        # Fix the maximum width of the widgets:
        self._upperLevel.setMaximumWidth(35)
        self._cmap.setMaximumWidth(25)
        self._lowerLevel.setMaximumWidth(35)



        self._layout = QtGui.QHBoxLayout()
        self._layout.addWidget(self._view)

        colors = QtGui.QVBoxLayout()
        colors.addWidget(self._upperLevel)
        colors.addWidget(self._cmap)
        colors.addWidget(self._lowerLevel)

        self._layout.addLayout(colors)

    def gradientChangeFinished(self):
        self._lookupTable = self._cmap.getLookupTable(255, alpha=0.75)
        self.refreshColors.emit()


    def getLookupTable(self):
        return self._lookupTable*(1./255)


    def colorsChanged(self):
        self.refreshColors.emit() 



    def getLayout(self):
        return self._layout


    def setRangeToMax(self):
        pass

    def getView(self):
        return self._view

    def getLevels(self):
        _max = float(self._upperLevel.text())
        _min = float(self._lowerLevel.text())
        return (_min, _max)

    def setCameraPosition(self, pos=None, distance=None, elevation=None, azimuth=None):
        if pos is not None:
            self._view.setCameraPos(pos)
        else:
            self._view.setCameraPosition(distance=distance,elevation=elevation,azimuth=azimuth)

    def setCenter(self, center=None):
        if center is not None:
            self._view.setCenter(center)

    def pan(self, dx, dy, dz, relative=False):
        pass

    def update(self):
        self._view.update()

    def restoreDefaults(self):
        print "restoreDefaults called but not implemented"
