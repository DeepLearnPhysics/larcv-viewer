from .database import recoBase
from pyqtgraph.Qt import QtWidgets, QtCore
import pyqtgraph as pg

class bbox2d(recoBase):

    """docstring for cluster"""

    def __init__(self):
        super(bbox2d, self).__init__()
        self._product_name = 'bbox2d'

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):


        event_bbox2d = io_manager.get_data(self._product_name, str(self._producerName))


        upper_offsets = [0,0,0]
        lower_offsets = [0.6,.5,0.7]

        self._drawnObjects = []
        for plane, view in view_manager.getViewPorts().items():
            # get the plane
            # thisPlane = view.plane()
            self._drawnObjects.append([])

            collection = event_bbox2d.at(plane)



            for bbox2d in collection.as_vector():
                
                # A QRect can be constructed with a set of left, top, width and height integers, 
                # or from a QPoint and a QSize.

                c  = bbox2d.centroid()
                hl = bbox2d.half_length()


                # if 0.0 in hl: continue
                # print(c)
                # print(hl)
                # Augment the widths if 0 to make it visible:
                if hl[0] == 0:
                    hl[0] += 1
                if hl[1] == 0:
                    hl[1] += 1

                # We need to subtract a little if the vertex is below the cathode:
                # if c[1] < meta.height(plane) / 2:
                #     c[1] -= lower_offsets[plane]
                #     pass
                # else:
                #     c[1] -= upper_offsets[plane]
                # print(f"P{plane}: {c[1]}")
                # Convert everything with the meta from absolute location to
                # pixel location (expected in QT)
                c[0]  = meta.wire_to_col(c[0],  plane)
                hl[0] = hl[0]*meta.comp_x(plane)
                c[1]  = meta.time_to_row(c[1],  plane)
                hl[1] = hl[1]*meta.comp_y(plane)
                    



                r = QtWidgets.QGraphicsRectItem(c[0] - hl[0], c[1] - hl[1], 2*hl[0], 2*hl[1])


                # particle = event_bbox2d.at(i)
                # bounding_box = particle.boundingbox_2d(plane)

                # left = meta.wire_to_col(bounding_box.min_y(), plane)
                # right = meta.wire_to_col(bounding_box.max_y(), plane)
                # top = meta.time_to_row(bounding_box.min_x(), plane)
                # bottom = meta.time_to_row(bounding_box.max_x(), plane)

                # #r = QtWidgets.QGraphicsRectItem(bottom, left, (top - bottom), (right-left))
                # r = QtWidgets.QGraphicsRectItem(left, bottom, (right-left), (top - bottom))
                r.setPen(pg.mkPen('r', width=2))
                r.setBrush(pg.mkColor((0,0,0,0)))
                self._drawnObjects[plane].append(r)
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
