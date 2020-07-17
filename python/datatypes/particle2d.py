from .database import recoBase
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

class particle2d(recoBase):

    """docstring for cluster"""

    def __init__(self):
        super(particle2d, self).__init__()
        self._product_name = 'particle'

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):


        event_particle = io_manager.get_data(self._product_name, str(self._producerName))


        self._drawnObjects = []
        for plane, view in view_manager.getViewPorts().items():
            # get the plane
            # thisPlane = view.plane()
            self._drawnObjects.append([])

            for particle in event_particle.as_vector():
                
                if particle.parent_track_id() == 0:
                    print(particle)


                # particle = event_particle.at(i)
                # bounding_box = particle.boundingbox_2d(plane)

                # left = meta.wire_to_col(bounding_box.min_y(), plane)
                # right = meta.wire_to_col(bounding_box.max_y(), plane)
                # top = meta.time_to_row(bounding_box.min_x(), plane)
                # bottom = meta.time_to_row(bounding_box.max_x(), plane)

                # #r = QtGui.QGraphicsRectItem(bottom, left, (top - bottom), (right-left))
                # r = QtGui.QGraphicsRectItem(left, bottom, (right-left), (top - bottom))
                # r.setPen(pg.mkPen('r'))
                # r.setBrush(pg.mkColor((0,0,0,0)))
                # self._drawnObjects[plane].append(r)
                # view._plot.addItem(r)

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
