from pyqtgraph.Qt import QtGui, QtCore


class ComboBoxWithKeyConnect(QtGui.QComboBox):

    def __init__(self):
        super(ComboBoxWithKeyConnect, self).__init__()

    def connectOwnerKPE(self, kpe):
        self._owner_KPE = kpe

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Up:
            super(ComboBoxWithKeyConnect, self).keyPressEvent(e)
            return
        if e.key() == QtCore.Qt.Key_Down:
            super(ComboBoxWithKeyConnect, self).keyPressEvent(e)
            return
        else:
            self._owner_KPE(e)
        # if e.key() == QtCore.Qt.Key_N:
        #     self._owner_KPE(e)
        #     pass
        # if e.key() == QtCore.Qt.Key_P:
        #     self._owner_KPE(e)
        #     pass
        # else:
        #     super(ComboBoxWithKeyConnect, self).keyPressEvent(e)
        #     self._owner_KPE(e)

# This is a widget class that contains the label and combo box
# It also knows what to do when updating



class recoBox(QtGui.QWidget):
    activated = QtCore.pyqtSignal(str)

    """docstring for recoBox"""

    def __init__(self, owner, name, product, producers):
        super(recoBox, self).__init__()
        self._label = QtGui.QLabel()
        self._name = name
        self._label.setText(self._name.capitalize() + ": ")
        self._box = ComboBoxWithKeyConnect()
        self._box.activated[str].connect(self.emitSignal)
        self._product = product
        if producers == None:
            self._box.addItem("--None--")
        else:
            self._box.addItem("--Select--")
            for producer in producers:
                self._box.addItem(producer)

        self._box.connectOwnerKPE(owner.keyPressEvent)

        # This is the widget itself, so set it up
        self._layout = QtGui.QVBoxLayout()
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._box)
        self.setLayout(self._layout)

    def keyPressEvent(self, e):
        self._box.keyPressEvent(e)
        super(recoBox, self).keyPressEvent(e)

    def emitSignal(self, text):
        self.activated.emit(text)

    def product(self):
        return self._product

    def name(self):
        return self._name


