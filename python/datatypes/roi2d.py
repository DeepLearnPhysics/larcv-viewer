from database import recoBase
from ROOT import larcv
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

class roi2d(recoBase):

    """docstring for cluster"""

    def __init__(self):
        super(roi2d, self).__init__()
        self._productName = 'roi2d'
        self._product_id = 1
        larcv.load_pyutil()

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):


        event_roi2d = io_manager.get_data(self._product_id, str(self._producerName))

        # print event_roi2d.ROIArray().size()

        for roi in event_roi2d.ROIArray():
            print "ROI Creation Process: {}".format(roi.CreationProcess())
            print 
        # return


        self._drawnObjects = []
        for view in view_manager.getViewPorts():
            # get the plane
            thisPlane = view.plane()
            self._drawnObjects.append([])

            for i in xrange(event_roi2d.ROIArray().size()):

                roi = event_roi2d.ROIArray().at(i)

                if roi.BB().size() == 0:
                    continue

                _type = roi.Type()
                bounding_box = roi.BB(thisPlane)
                if thisPlane == 0:
                    print "CM Left: {}".format(meta.wire_to_col(bounding_box.tl().x, thisPlane))
                    print "CM Right: {}".format(meta.wire_to_col(bounding_box.tr().x, thisPlane))
                    print "CM Top: {}".format(meta.time_to_row(bounding_box.tl().y, thisPlane))
                    print "CM Bottom: {}".format(meta.time_to_row(bounding_box.bl().y, thisPlane))
                    print "Wire Left: {}".format(bounding_box.tl().x)
                    print "Wire Right: {}".format(bounding_box.tr().x)
                    print "Time Top: {}".format(bounding_box.tl().y)
                    print "Time Bottom: {}".format(bounding_box.bl().y)

                    print 

                left = meta.wire_to_col(bounding_box.tl().x, thisPlane)
                right = meta.wire_to_col(bounding_box.tr().x, thisPlane)
                top = meta.time_to_row(bounding_box.tl().y, thisPlane)
                bottom = meta.time_to_row(bounding_box.bl().y, thisPlane)

                r = QtGui.QGraphicsRectItem(left, bottom, (right-left), (top - bottom))
                r.setPen(pg.mkPen('r'))
                r.setBrush(pg.mkColor((0,0,0,0)))
                self._drawnObjects[thisPlane].append(r)
                view._plot.addItem(r)

        return

    # def clearDrawnObjects(self, view_manager):
    #     i_plane = 0
    #     # erase the clusters
    #     for plane in self._listOfClusters:
    #         view = view_manager.getViewPorts()[i_plane]
    #         i_plane += 1
    #         for cluster in plane:
    #             cluster.clearHits(view)


    #     self._listOfClusters = []
