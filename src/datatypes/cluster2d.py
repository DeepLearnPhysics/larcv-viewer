from .database import recoBase
from pyqtgraph.Qt import QtGui, QtCore


import pyqtgraph, numpy
import larcv

class cluster2d(recoBase):

    """docstring for cluster2d"""

    def __init__(self):
        super(cluster2d, self).__init__()
        self._product_name = 'cluster2d'

        # self._listOfClusters = []

        # Defining the cluster2d colors:
        self._clusterColors = [
            (0, 147, 147, 125),    # dark teal
            (0, 0, 252, 125),      # bright blue
            (156, 0, 156, 125),    # purple
            (255, 0, 255, 125),    # pink
            (255, 0, 0, 125),      # red
            (175, 0, 0, 125),      # red/brown
            (252, 127, 0, 125),    # orange
            (102, 51, 0, 125),     # brown
            (100, 253, 0, 125),    # bright green
            (255, 248, 202, 125),  # tan
            (255, 248, 202, 125),  # tan
            (255, 148, 241, 125),  # pink
        ]

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):

        #Get the list of cluster2d sets:
        event_sparse_cluster = io_manager.get_data(self._product_name, str(self._producerName))
        # event_sparse_cluster = larcv.EventSparseCluster2D.to_sparse_cluster(event_sparse_cluster)
        # if self._producerName in io_manager.producer_list(self._product_name):
        #     hasROI = True
        # else:
        #     hasROI = False

        # if hasROI:
        #     event_roi = io_manager.get_data(self._product_name, str(self._producerName))

        pen = pyqtgraph.mkPen((0, 0, 0), width=1)

        for plane, view in view_manager.getViewPorts().items():
            
            self._drawnObjects.append([])

            colorIndex = 0

            # Get the cluster2d clusters for this plane:
            # try:
            sparse_clusters = event_sparse_cluster.sparse_cluster(plane)
            # except:
                # continue
            meta = sparse_clusters.meta()

            # extend the list of clusters
            # self._listOfClusters.append([])

            clusters = sparse_clusters.as_vector()
            for i, cluster  in enumerate(clusters):
                if i == len(clusters) - 1: break


                indexes = cluster.indexes()
                values  = cluster.values()
                if len(values) == 0: continue

                # # Reject all out-of-bounds indexes:
                in_bounds = indexes < meta.total_voxels()
                # oob = indexes >= meta.total_voxels()
                # Merge the bounds:
                # in_bounds = numpy.logical_and(in_bounds, oob)
                indexes = indexes[in_bounds]
                values  = values[in_bounds]

                dims = [meta.number_of_voxels(0), meta.number_of_voxels(1) ]
                x, y = numpy.unravel_index(indexes, dims)

                y = y.astype(float) + 0.5
                x = x.astype(float) + 0.5

                # colors = cmap.map(values, mode='float')


                this_item = pyqtgraph.ScatterPlotItem()
                color = pyqtgraph.mkColor(self._clusterColors[colorIndex])

                this_item.setData(x, y, size=1, pxMode=False, 
                    symbol='s', pen=None, 
                    brush = color,
                    # hoverable=True, hoverPen=pen
                    )

                view._plot.addItem(this_item)
                self._drawnObjects[plane].append(this_item)




                colorIndex += 1
                if colorIndex >= len(self._clusterColors):
                    colorIndex = 0

    # def clearDrawnObjects(self, view_manager):
    #     i_plane = 0
    #     # erase the clusters
    #     for plane in self._listOfClusters:
    #         view = view_manager.getViewPorts()[i_plane]
    #         i_plane += 1
    #         for cluster in plane:
    #             cluster.clearHits(view)


    #     self._listOfClusters = []
