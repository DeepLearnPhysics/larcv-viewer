from .database import recoBase3D
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy

class bbox3d(recoBase3D):

    """docstring for cluster"""

    def __init__(self):
        super(bbox3d, self).__init__()
        self._product_name = 'bbox3d'

        self._box_template = numpy.array([[ 0 , 0, 0],
                                          [ 1 , 0, 0],
                                          [ 1 , 1, 0],
                                          [ 0 , 1, 0],
                                          [ 0 , 0, 0],
                                          [ 0 , 0, 1],
                                          [ 1 , 0, 1],
                                          [ 1 , 1, 1],
                                          [ 0 , 1, 1],
                                          [ 0 , 0, 1],
                                          [ 1 , 0, 1],
                                          [ 1 , 0, 0],
                                          [ 1 , 1, 0],
                                          [ 1 , 1, 1],
                                          [ 0 , 1, 1],
                                          [ 0 , 1, 0]],
                                         dtype=float)

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):


        event_bbox3d = io_manager.get_data(self._product_name, str(self._producerName))


        upper_offsets = [0,0,0]
        lower_offsets = [0.6,.5,0.7]

        self._drawnObjects = []

        collection = event_bbox3d.at(0)

        for bbox3d in collection.as_vector():
                

            pts = self._box_template.copy()
            c  = bbox3d.centroid()
            hl = bbox3d.half_length()

            if hl[0] == 0:
                hl[0] += 1
            if hl[1] == 0:
                hl[1] += 1
            if hl[2] == 0:
                hl[2] += 1



            # pts[:,0] += c[0] - 2*meta.min_x() 
            # pts[:,1] += c[1] - 2*meta.min_y() 
            # pts[:,2] += c[2] - 2*meta.min_z() 


            #Scale all the points of the box to the right voxel size:
            pts[:,0] *= 2*hl[0]
            pts[:,1] *= 2*hl[1]
            pts[:,2] *= 2*hl[2]

            #Shift the points to put the center of the rectangles at (0,0,0)
            pts[:,0] -= hl[0]
            pts[:,1] -= hl[1]
            pts[:,2] -= hl[2]
        
            # #Move the points to the right coordinate in this space

            pts[:,0] += c[0] - collection.meta().origin(0)
            pts[:,1] += c[1] - collection.meta().origin(1)
            pts[:,2] += c[2] - collection.meta().origin(2)

            line = gl.GLLinePlotItem(pos=pts,color=(1.0,1.0,1.0,1.0), width=3)
            view_manager.getView().addItem(line)
            self._drawnObjects.append(line)


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
