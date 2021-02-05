from pyqtgraph.Qt import QtCore

from .event_meta import event_meta

import larcv

class evd_manager_base(QtCore.QObject):

    eventChanged = QtCore.pyqtSignal()
    drawFreshRequested = QtCore.pyqtSignal()
    metaRefreshed = QtCore.pyqtSignal(event_meta)


    def __init__(self, config, _file=None):
        super(evd_manager_base, self).__init__()
        QtCore.QObject.__init__(self)
        self._config = config
        self.init_manager(_file)

    def init_manager(self, _file):
        # For the larcv manager, using the IOManager to get at the data
        self._driver =  larcv.ProcessDriver("ProcessDriver")
        self._driver.configure(self._config)

        # Meta keeps track of information about number of planes, visible
        # regions, etc.:
        self._meta = event_meta()


        # Drawn classes is a list of things getting drawn, as well.
        self._drawnClasses = dict()

        self._keyTable = dict()


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

        self._driver.process_entry()
        # self._driver.set_id(run,subrun,event)

        self.refresh_meta()


    def refresh_meta(self):
        # # Read in any of the image2d products if none is specified.
        # # Use it's meta info to build up the meta for the viewer
        # _producers = self._driver.io().producer_list('image2d')
        # if 'wire' in _producers:
        #     _producer = 'wire'
        # else:
        #     _producer = _producers[-1]
        # _event_image2d = self._driver.io().get_data('image2d',_producer)
        

        # Meta information can come from either image2d, sparse2d or cluster2d
        # It's pull from image2d by default, from the first producer.
        # it goes to sparse2d next, then cluster2d

        product = "image2d"
        producers = self._driver.io().producer_list(product)



        if len(producers) == 0:
            product = "sparse2d"
            producers = self._driver.io().producer_list(product)
        if len(producers) == 0:
            product = "cluster2d"
            producers = self._driver.io().producer_list(product)
        
        if len(producers) == 0:
            raise Exception("No Meta avialable to define viewer boundaries")


        producer = producers[-1]


        meta_vec = []

        data = self._driver.io().get_data(product, producer)
        # if product == "image2d":
        #     data = larcv.EventImage2D.to_image2d(data)
        # if product == "sparse2d":
        #     data = larcv.EventSparseTensor2D.to_sparse_tensor(data)            
        # if product == "cluster2d":
        #     data = larcv.EventSparseCluster2D.to_sparse_cluster(data)

        for data_obj in data.as_vector():
            meta_vec.append(data_obj.meta())

        self._meta.refresh(meta_vec)

    def meta(self):
        return self._meta

    # This function will return all producers for the given product
    def getProducers(self, product):
        if self._driver.io() is not None:
            return self._driver.io().producer_list(product)

    # This function returns the list of products that can be drawn:
    def getDrawableProducts(self):
        return self._drawableItems.getDict()

    # override the run,event,subrun functions:
    def run(self):
        if self._driver.io() is None:
            return 0
        return self._driver.event_id().run()

    def event(self):
        if self._driver.io() is None:
            return 0
        return self._driver.event_id().event()

    def subrun(self):
        if self._driver.io() is None:
            return 0
        return self._driver.event_id().subrun()

    # def internalEvent(self):
    def entry(self):
        if self._driver.io() is not None:
            return self._driver.io().current_entry()
        else:
            return -1

    def n_entries(self):
        if self._driver.io() is not None:
            return self._driver.io().get_n_entries()
        else:
            return 0

    # override the functions from manager as needed here
    def next(self):
        if self.entry() + 1 < self.n_entries():
            # print self._driver.event()
            self._driver.clear_entry()            
            self._driver.process_entry(self.entry() + 1)
            self.eventChanged.emit()
        else:
            print("On the last event, can't go to next.")

    def prev(self):
        if self.entry != 0:
            self._driver.clear_entry()            
            self._driver.process_entry(self.entry() - 1)
            self.eventChanged.emit()
        else:
            print("On the first event, can't go to previous.")

    def go_to_entry(self, entry):
        if entry >= 0 and entry < self.n_entries():
            self._driver.clear_entry()            
            self._driver.process_entry(entry)
            self.eventChanged.emit()
        else:
            print("Can't go to entry {}, entry is out of range.".format(entry))

    def range(self, plane):
        # To get the range, we ask for the image meta and use it:
        return self._meta.range(plane)

    def n_views(self):
        return self._meta.n_views()
