import ROOT
from ROOT import larcv
from pyqtgraph.Qt import QtCore

from .event_meta import event_meta

class evd_manager_base(QtCore.QObject):

    eventChanged = QtCore.pyqtSignal()
    drawFreshRequested = QtCore.pyqtSignal()
    metaRefreshed = QtCore.pyqtSignal(event_meta)

    """docstring for lariat_manager"""

    def __init__(self, config, _file=None):
        super(evd_manager_base, self).__init__()
        QtCore.QObject.__init__(self)
        self._config = config
        self.init_manager(_file)

    def init_manager(self, _file):
        # For the larcv manager, using the IOManager to get at the data
        self._driver =  larcv.ProcessDriver('ProcessDriver')
        self._driver.configure(self._config)
        self._io_manager = self._driver.io()

        # Meta keeps track of information about number of planes, visible
        # regions, etc.:
        self._meta = event_meta()


        # Drawn classes is a list of things getting drawn, as well.
        self._drawnClasses = dict()

        self._keyTable = dict()


        if _file != None:
            flist=ROOT.std.vector('std::string')()
            if type(_file) is list:
                for f in _file: flist.push_back(f)
                self._driver.override_input_file(flist)
            else:
                flist.push_back(_file)
                self._driver.override_input_file(flist)

        self._driver.initialize()

        self._driver.process_entry()
        # self._driver.set_id(run,subrun,event)

        self.refresh_meta()


    def refresh_meta(self):
        # # Read in any of the image2d products if none is specified.
        # # Use it's meta info to build up the meta for the viewer
        # _producers = self._io_manager.producer_list('image2d')
        # if 'wire' in _producers:
        #     _producer = 'wire'
        # else:
        #     _producer = _producers[-1]
        # _event_image2d = self._io_manager.get_data('image2d',_producer)
        
        # Look for the meta_event_tree to get the event meta out of the file:
        _producers = self._io_manager.producer_list('meta')
        if '2D' in _producers:
            _producer = '2D'
        elif _producers.size() > 0:
            _producer = _producers[0]
        else:
            print("Error, no meta available for the viewer.")
            exit()

        _global_meta = self._io_manager.get_data('meta',_producer)


        self._meta.refresh(_global_meta)

    def meta(self):
        return self._meta

    # This function will return all producers for the given product
    def getProducers(self, product):
        if self._io_manager is not None:
            return self._io_manager.producer_list(product)

    # This function returns the list of products that can be drawn:
    def getDrawableProducts(self):
        return self._drawableItems.getDict()

    # override the run,event,subrun functions:
    def run(self):
        if self._io_manager is None:
            return 0
        return self._io_manager.event_id().run()

    def event(self):
        if self._io_manager is None:
            return 0
        return self._io_manager.event_id().event()

    def subrun(self):
        if self._io_manager is None:
            return 0
        return self._io_manager.event_id().subrun()

    # def internalEvent(self):
    def entry(self):
        if self._io_manager is not None:
            return self._io_manager.current_entry()
        else:
            return -1

    def n_entries(self):
        if self._io_manager is not None:
            return self._io_manager.get_n_entries()
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
