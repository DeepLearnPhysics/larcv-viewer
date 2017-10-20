from database import recoBase
from pyqtgraph.Qt import QtGui, QtCore
from connectedObjects import connectedBox, connectedCircle, boxCollection


class pixel2d(recoBase):

    """docstring for pixel2d"""

    def __init__(self):
        super(pixel2d, self).__init__()
        self._productName = 'pixel2d'
        self._product_id = 3

        self._listOfClusters = []

        # Defining the pixel2d colors:
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
            (100, 253, 0)  # bright green
        ]

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):

        #Get the list of pixel2d sets:
        event_pixel2d = io_manager.get_data(3, str(self._producerName))
        if self._producerName in io_manager.producer_list(1):
            hasROI = True
        else:
            hasROI = False

        if hasROI:    
            event_roi = io_manager.get_data(1, str(self._producerName))

        for view in view_manager.getViewPorts():
            colorIndex = 0
            # get the plane
            thisPlane = view.plane()

            # Get the pixel2d clusters for this plane:
            clusters = event_pixel2d.Pixel2DClusterArray(thisPlane)

            # extend the list of clusters
            self._listOfClusters.append([])

            for i in xrange(len(clusters)):
                cluster = clusters[i]
                # Now make the cluster
                cluster_box_coll = boxCollection()
                cluster_box_coll.setColor(self._clusterColors[colorIndex])
                cluster_box_coll.setPlane(thisPlane)

                # Keep track of the cluster for drawing management
                self._listOfClusters[thisPlane].append(cluster_box_coll)

                # Get the matching ROI information:
                _event_ID = cluster.ID()
                if hasROI:
                    label = event_roi.ROIArray().at(_event_ID).Type()
                    cluster_box_coll.setLabel(label)

                # draw the hits in this cluster:
                cluster_box_coll.drawHits(view, cluster)



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
