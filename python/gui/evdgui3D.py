try:
    import pyqtgraph.opengl as gl
except:
    print("ERROR: Must have opengl for this display.")

from gui3D import gui3D
from pyqtgraph.Qt import QtGui, QtCore
from manager import evd_manager_3D

from recobox import recoBox

# Inherit the basic gui to extend it
# override the gui to give the lariat display special features:


class evdgui3D(gui3D):

    """special larlite gui for 3D"""

    def __init__(self):
        super(evdgui3D, self).__init__()


    def connect_manager(self, _manager):
        self._event_manager = _manager
        self._event_manager.eventChanged.connect(self.update)
        self._view_manager.refreshColors.connect(self.refreshColors)

    # override the initUI function to change things:
    def initUI(self):
        super(evdgui3D, self).initUI()
        # Change the name of the labels for lariat:
        self.update()

    def refreshColors(self):
        self._event_manager.refreshColors(self._view_manager)

    # This function sets up the eastern widget
    def getEastLayout(self):
        # This function just makes a dummy eastern layout to use.
        label1 = QtGui.QLabel("LArCV")
        label2 = QtGui.QLabel("EVD 3D")
        font = label1.font()
        font.setBold(True)
        label1.setFont(font)
        label2.setFont(font)

        self._eastWidget = QtGui.QWidget()
        # This is the total layout
        self._eastLayout = QtGui.QVBoxLayout()
        # add the information sections:
        self._eastLayout.addWidget(label1)
        self._eastLayout.addWidget(label2)
        self._eastLayout.addStretch(1)
        
        # self._paramsDrawBox = QtGui.QCheckBox("Draw Params.")
        # self._paramsDrawBox.stateChanged.connect(self.paramsDrawBoxWorker)
        # self._eastLayout.addWidget(self._paramsDrawBox)
        # self._eastLayout.addStretch(1)

        # Now we get the list of items that are drawable:
        drawableProducts = self._event_manager.getDrawableProducts()
        self._listOfRecoBoxes = []
        for product in drawableProducts:
            thisBox = recoBox(self,
                              product,
                              drawableProducts[product][1],
                              self._event_manager.getProducers(
                                  drawableProducts[product][1]))
            self._listOfRecoBoxes.append(thisBox)
            thisBox.activated[str].connect(self.recoBoxHandler)
            self._eastLayout.addWidget(thisBox)

        self._eastLayout.addStretch(2)

        self._eastWidget.setLayout(self._eastLayout)
        self._eastWidget.setMaximumWidth(150)
        self._eastWidget.setMinimumWidth(100)
        return self._eastWidget

    def drawableProductsChanged(self):
        # self.removeItem(self._eastLayout)
        self._eastWidget.close()
        east = self.getEastLayout()
        self.slave.addWidget(east)
        self.update()


    def recoBoxHandler(self, text):
        sender = self.sender()
        # print sender.product(), "was changed to" , text
        if text == "--Select--" or text == "--None--":
            self._event_manager.redrawProduct(sender.name(), None, self._view_manager)
            return
        else:
            self._event_manager.redrawProduct(sender.name(), text, self._view_manager)
