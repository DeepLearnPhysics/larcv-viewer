from pyqtgraph.Qt import QtCore
from datatypes import drawableItems3D

import larcv 

from .evd_manager_base import evd_manager_base
from .event_meta import event_meta3D

try:
    import pyqtgraph.opengl as gl
except:
    print("Need opengl for the 3D viewer! Exiting ...")
    exit()

class evd_manager_3D(evd_manager_base):

    """This class handles file I/O and drawing for 3D viewer"""


    def __init__(self, config, _file=None):
        super(evd_manager_3D, self).__init__(config, _file)
        self._drawableItems = drawableItems3D()
                

    def init_manager(self, _file):

        # For the larcv manager, using the IOManager to get at the data
        self._driver =  larcv.ProcessDriver('ProcessDriver')
        self._driver.configure(self._config)

        # Meta keeps track of information about number of planes, visible
        # regions, etc.:
        self._meta = event_meta3D()


        # Drawn classes is a list of things getting drawn, as well.
        self._drawnClasses = dict()


        if _file != None:
            # flist=larcv.VectorOfString()
            if type(_file) is list:
            #     for f in _file: flist.push_back(f)
                self._driver.override_input_file(_file)
            else:
                flist = []
                flist.append(_file)
                self._driver.override_input_file(flist)

        self._driver.initialize()
        self.go_to_entry(0)

        self.refresh_meta()
        

    def refresh_meta(self, producer=None):
        # Read in any of the image2d products if none is specified.
        # Use it's meta info to build up the meta for the viewer


        product = "sparse3d"
        producers = self._driver.io().producer_list(product)
        if len(producers) == 0:
            product = "cluster3d"
            producers = self._driver.io().producer_list(product)
        
        if len(producers) == 0:
            raise Exception("No Meta avialable to define viewer boundaries")

        producer = producers[0]



        data = self._driver.io().get_data(product, producer)
        if product == "sparse3d":
            # data = larcv.EventSparseTensor3D.to_sparse_tensor(data)            
            meta = data.sparse_tensor(0).meta()
        if product == "cluster3d":
            # data = larcv.EventSparseCluster3D.to_sparse_cluster(data)
            meta = data.sparse_cluster(0).meta()

        self._meta.refresh(meta)




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
            self._drawnClasses[product].drawObjects(view_manager, self._driver.io(), self.meta())
            return

        # Now, draw the new product
        if product in self._drawableItems.getListOfTitles():
            # drawable items contains a reference to the class, so
            # instantiate it
            drawingClass=self._drawableItems.getDict()[product][0]()

            drawingClass.setProducer(producer)
            self._drawnClasses.update({product: drawingClass})

            # Need to process the event
            drawingClass.drawObjects(view_manager, self._driver.io(), self.meta())


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
                self._drawnClasses[item].drawObjects(view_manager, self._driver.io(), self.meta())


    def refreshColors(self, view_manager):
        order = self._drawableItems.getListOfTitles()
        for item in order:
            if item in self._drawnClasses:
                self._drawnClasses[item].refresh(view_manager)