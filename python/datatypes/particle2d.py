from database import recoBase
from ROOT import larcv
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

class particle2d(recoBase):

    """docstring for cluster"""

    def __init__(self):
        super(particle2d, self).__init__()
        self._product_name = 'particle'
        larcv.load_pyutil()

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):


        event_particle = io_manager.get_data(self._product_name, str(self._producerName))

        self._drawnObjects = []
        for view in view_manager.getViewPorts():
            # get the plane
            thisPlane = view.plane()
            self._drawnObjects.append([])

            for i in xrange(event_particle.size()):

                particle = event_particle.at(i)
                print particle.BoundingBox2D()
                print particle.BoundingBox2D().size()
                for box in particle.BoundingBox2D():
                    print box
                return
                if particle.BB().size() == 0:
                    continue

                _type = particle.Type()
                bounding_box = particle.BB(thisPlane)
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
