from .database import recoBase
from pyqtgraph.Qt import QtGui, QtCore
from .connectedObjects import connectedBox, boxCollection

import larcv

class cluster2d(recoBase):

    """docstring for cluster2d"""

    def __init__(self):
        super(cluster2d, self).__init__()
        self._product_name = 'cluster2d'

        self._listOfClusters = []

        # Defining the cluster2d colors:
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

        #Get the list of cluster2d sets:
        event_sparse_cluster = io_manager.get_data(self._product_name, str(self._producerName))
        event_sparse_cluster = larcv.EventSparseCluster2D.to_sparse_cluster(event_sparse_cluster)
        # if self._producerName in io_manager.producer_list(self._product_name):
        #     hasROI = True
        # else:
        #     hasROI = False

        # if hasROI:
        #     event_roi = io_manager.get_data(self._product_name, str(self._producerName))

        for plane, view in view_manager.getViewPorts().items():
            colorIndex = 0

            # Get the cluster2d clusters for this plane:
            # try:
            clusters = event_sparse_cluster.sparse_cluster(plane)
            # except:
                # continue

            # extend the list of clusters
            self._listOfClusters.append([])

            for i in range(max(1,clusters.as_vector().size() -1)):
                cluster = clusters.as_vector()[i]
                # Now make the cluster
                cluster_box_coll = boxCollection()
                cluster_box_coll.setColor(self._clusterColors[colorIndex])
                cluster_box_coll.setPlane(plane)

                # Keep track of the cluster for drawing management
                self._listOfClusters[plane].append(cluster_box_coll)

                # draw the hits in this cluster:
                cluster_box_coll.drawHits(view, cluster, clusters.meta())



                colorIndex += 1
                if colorIndex >= len(self._clusterColors):
                    colorIndex = 0

    def clearDrawnObjects(self, view_manager):
        i_plane = 0
        # erase the clusters
        for plane in self._listOfClusters:
            view = view_manager.getViewPorts()[i_plane]
            i_plane += 1
            for cluster in plane:
                cluster.clearHits(view)


        self._listOfClusters = []
