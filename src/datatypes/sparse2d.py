from .database import recoBase
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph, numpy
from .connectedObjects import connectedBox, boxCollection

import larcv

class sparse2d(recoBase):

    """docstring for sparse2d"""

    def __init__(self):
        super(sparse2d, self).__init__()
        self._product_name = 'sparse2d'

        self._listOfClusters = []

        # Defining the sparse2d colors:
        self._clusterColors = [
            (0, 147, 147, 125),  # dark teal
            (0, 0, 252, 125),   # bright blue
            (156, 0, 156, 125),  # purple
            (255, 0, 255, 125),  # pink
            (255, 0, 0, 125),  # red
            (175, 0, 0, 125),  # red/brown
            (252, 127, 0, 125),  # orange
            (102, 51, 0, 125),  # brown
            (127, 127, 127, 125),  # dark gray
            (210, 210, 210, 125),  # gray
            (100, 253, 0, 125)  # bright green
        ]

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):

        #Get the list of sparse2d sets:
        sparse_2d_set = io_manager.get_data(self._product_name, str(self._producerName))
        # sparse_2d_set = larcv.EventSparseTensor2D.to_sparse_tensor(sparse_2d_set)
        # if self._producerName in io_manager.producer_list(self._product_name):
        #     hasROI = True
        # else:
        #     hasROI = False

        # if hasROI:
        #     event_roi = io_manager.get_data(self._product_name, str(self._producerName))

        for plane, view in view_manager.getViewPorts().items():
            self._drawnObjects.append([])

            colorIndex = 0

            active_map = view._activeMap
            cols = []
            vals = []
            for val, rgba in active_map['ticks']:
                cols.append(numpy.asarray(rgba) / 255.)
                vals.append(val)

            cmap = pyqtgraph.ColorMap(vals, cols)

            # n = len(uids); 
            # colors = cmap(range(n), bytes = True);


            # Get the sparse2d clusters for this plane:
            # try:
            voxelset = sparse_2d_set.sparse_tensor(plane)

            # Voxelset doesn't manager memory for just indexes or just values
            # Therefore, we keep a reference to these.
            # If we don't, the memory underneath for the std::vectors will
            # be freed and anything might end up there.  This will corrupt the 
            # numpy arrays below since they share the memory.
            meta = voxelset.meta()

            # cpp_indexes = voxelset.indexes()
            # cpp_values = voxelset.values()

            # indexes = larcv.as_ndarray_sizet(cpp_indexes)
            # values  = larcv.as_ndarray_float(cpp_values)

            indexes = voxelset.indexes()
            values = voxelset.values()

            # Reject all out-of-bounds indexes:
            in_bounds = indexes < meta.total_voxels()
            oob = indexes >= meta.total_voxels()
            indexes = indexes[in_bounds]
            values  = values[in_bounds]

            dims = [meta.number_of_voxels(0), meta.number_of_voxels(1) ]
            x, y = numpy.unravel_index(indexes, dims)

            y = y.astype(float) + 0.5
            x = x.astype(float) + 0.5



            this_item = pyqtgraph.ScatterPlotItem()

            this_item.setData(x, y, size=1, pxMode=False, symbol='s', pen=None)

            view._plot.addItem(this_item)
            self._drawnObjects[plane].append(this_item)

