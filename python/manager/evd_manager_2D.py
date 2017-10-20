from pyqtgraph.Qt import QtCore
import datatypes
import ROOT

from evd_manager_base import evd_manager_base

class evd_manager_2D(evd_manager_base):

    '''
    Class to handle the 2D specific aspects of viewer
    '''

    def __init__(self, config, _file=None):
        super(evd_manager_2D, self).__init__(config, _file)
        self._drawableItems = datatypes.drawableItems()

    # this function is meant for the first request to draw an object or
    # when the producer changes
    def redrawProduct(self, product, producer, view_manager):
        
        # print "Received request to redraw ", product, " by ",producer
        # First, determine if there is a drawing process for this product:  
        
        if producer is None:
            if product in self._drawnClasses:
                self._drawnClasses[product].clearDrawnObjects(view_manager)
                self._drawnClasses.pop(product)
            return
        if product in self._drawnClasses:
            self._drawnClasses[product].setProducer(producer)
            self._drawnClasses[product].clearDrawnObjects(view_manager)
            self._drawnClasses[product].drawObjects(view_manager, self._io_manager, self.meta())
            return

        # Now, draw the new product
        if product in self._drawableItems.getListOfTitles():
            # drawable items contains a reference to the class, so
            # instantiate it
            drawingClass=self._drawableItems.getDict()[product][0]()

            drawingClass.setProducer(producer)
            self._drawnClasses.update({product: drawingClass})

            # Need to process the event
            drawingClass.drawObjects(view_manager, self._io_manager, self.meta())


    def clearAll(self, view_manager):
        for recoProduct in self._drawnClasses:
            self._drawnClasses[recoProduct].clearDrawnObjects(view_manager)
        # self.clearTruth()

    def drawFresh(self, view_manager):

        self.clearAll(view_manager)
        # Draw objects in a specific order defined by drawableItems
        order = self._drawableItems.getListOfTitles()
        # self.drawTruth()
        for item in order:
            if item in self._drawnClasses:
                self._drawnClasses[item].drawObjects(view_manager, self._io_manager, self.meta())



    def getPlane(self, plane):
        if self._drawWires:
            return self._wireDrawer.getPlane(plane)
