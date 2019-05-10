from .database import recoBase3D
from pyqtgraph.Qt import QtGui, QtCore
import numpy
import pyqtgraph as pg
import pyqtgraph.opengl as gl

class particle3d(recoBase3D):

    """docstring for cluster"""

    def __init__(self):
        super(particle3d, self).__init__()
        self._product_name = 'particle'


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


        event_particle = io_manager.get_data(self._product_name, str(self._producerName))

        # # This section draws voxels onto the environment:
        for particle in event_particle.as_vector():
            box = particle.boundingbox_3d()

            # Can create a 3D box using line plots.


            pts = self._box_template.copy()

            pts[:,0] *= box.width()
            pts[:,1] *= box.height()
            pts[:,2] *= box.depth()

            pts[:,0] += box.center_x() - meta.min_x() - 0.5*box.width()
            pts[:,1] += box.center_y() - meta.min_y() - 0.5*box.height()
            pts[:,2] += box.center_z() - meta.min_z() - 0.5*box.depth()


            line = gl.GLLinePlotItem(pos=pts,color=(1.0,1.0,1.0,1.0), width=3)
            view_manager.getView().addItem(line)
            self._drawnObjects.append(line)
            # break

#             min_x
# min_y
# min_z
# max_x
# max_y
# max_z

        # self.redraw(view_manager)



    def redraw(self, view_manager):


        if self._gl_voxel_mesh is not None:
            view_manager.getView().removeItem(self._gl_voxel_mesh)
            self._gl_voxel_mesh = None

        verts, faces, colors = self.buildTriangleArray(self._id_summed_charge,
                                                       self._assigned_colors,
                                                       view_manager)


        #make a mesh item: 
        mesh = gl.GLMeshItem(vertexes=verts,
                             faces=faces,
                             faceColors=colors,
                             smooth=False)
        # mesh.setGLOptions("additive")        
        self._gl_voxel_mesh = mesh
        view_manager.getView().addItem(self._gl_voxel_mesh)

    #     self._drawnObjects = []
    #     for plane, view in view_manager.getViewPorts().iteritems():
    #         # get the plane
    #         # thisPlane = view.plane()
    #         self._drawnObjects.append([])

    #         for particle in event_particle.as_vector():

    #             # particle = event_particle.at(i)
    #             bounding_box = particle.boundingbox_2d(plane)

    #             left = meta.wire_to_col(bounding_box.min_x(), plane)
    #             right = meta.wire_to_col(bounding_box.max_x(), plane)
    #             top = meta.time_to_row(bounding_box.min_y(), plane)
    #             bottom = meta.time_to_row(bounding_box.max_y(), plane)

    #             r = QtGui.QGraphicsRectItem(left, bottom, (right-left), (top - bottom))
    #             r.setPen(pg.mkPen('r'))
    #             r.setBrush(pg.mkColor((0,0,0,0)))
    #             self._drawnObjects[plane].append(r)
    #             view._plot.addItem(r)

    #     return

    # # def clearDrawnObjects(self, view_manager):
    # #     i_plane = 0
    # #     # erase the clusters
    # #     for plane in self._listOfClusters:
    # #         view = view_manager.getViewPorts()[i_plane]
    # #         i_plane += 1
    # #         for cluster in plane:
    # #             cluster.clearHits(view)


    # #     self._listOfClusters = []
