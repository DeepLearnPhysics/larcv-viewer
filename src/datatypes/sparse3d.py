from .database import recoBase
from pyqtgraph.Qt import QtGui, QtCore
import numpy
try:
    import pyqtgraph.opengl as gl
except:
    print("Error, must have open gl to use this viewer.")
    exit(-1)

import larcv

class sparse3d(recoBase):

    """docstring for sparse3d"""

    def __init__(self):
        super(sparse3d, self).__init__()
        self._product_name = 'sparse3d'
        self._gl_voxel_mesh = None
        self._id_summed_charge = dict()
        self._meta = None

        self._box_template = numpy.array([[ 0 , 0, 0],
                                          [ 1 , 0, 0],
                                          [ 1 , 1, 0],
                                          [ 0 , 1, 0],
                                          [ 0 , 0, 1],
                                          [ 1 , 0, 1],
                                          [ 1 , 1, 1],
                                          [ 0 , 1, 1]],
                                         dtype=float)


        self._faces_template = numpy.array([[0, 1, 2],
                                            [0, 2, 3],
                                            [0, 1, 4],
                                            [1, 5, 4],
                                            [1, 2, 5],
                                            [2, 5, 6],
                                            [2, 3, 6],
                                            [3, 6, 7],
                                            [0, 3, 7],
                                            [0, 4, 7],
                                            [4, 5, 7],
                                            [5, 6, 7]])


    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):

        #Get the list of sparse3d sets:
        event_voxel3d = io_manager.get_data(self._product_name, str(self._producerName))
        # event_voxel3d = larcv.EventSparseTensor3D.to_sparse_tensor(event_voxel3d)


        voxels = event_voxel3d.as_vector()[0]
        self._meta = voxels.meta() 

        # view_manager.getView().updateMeta(self._meta)



        self._id_summed_charge = dict()
        # # This section draws voxels onto the environment:
        for voxel in voxels.as_vector():

            if voxel.id() >= self._meta.total_voxels():
                continue
            if voxel.id() in self._id_summed_charge:
                self._id_summed_charge[voxel.id()] += voxel.value()
            else:
                self._id_summed_charge.update({voxel.id() : voxel.value()})
        self.redraw(view_manager)



        # self.setColors(view_manager.getLookupTable(), view_manager.getLevels())
        # self.redraw(view_manager)

    def redraw(self, view_manager):


        if self._gl_voxel_mesh is not None:
            view_manager.getView().removeItem(self._gl_voxel_mesh)
            self._gl_voxel_mesh = None


        verts, faces, colors = self.buildTriangleArray(self._id_summed_charge,
                                                       view_manager)

        #make a mesh item: 
        mesh = gl.GLMeshItem(vertexes=verts,
                             faces=faces,
                             faceColors=colors,
                             smooth=False)

        # mesh.setGLOptions("additive")        
        mesh.setGLOptions("translucent")        
        self._gl_voxel_mesh = mesh
        view_manager.getView().addItem(self._gl_voxel_mesh)

    def buildTriangleArray(self, id_summed_charge, view_manager):


        n_voxels = len(id_summed_charge)
        # # # Allocate enough memory for all 3 numpy arrays upfront:

        verts = numpy.zeros((n_voxels*8,3))
        faces = numpy.zeros((n_voxels*12,3), dtype=numpy.int)
        colors = numpy.zeros((n_voxels*12,4))

        i = 0
        for voxel_id in id_summed_charge:
            # Don't draw this pixel if it's below the threshold:
            if id_summed_charge[voxel_id] < view_manager.getLevels()[0]:
                continue


            this_color = self.getColor(view_manager.getLookupTable(),
                                       view_manager.getLevels(),
                                       id_summed_charge[voxel_id])


            colors[12*i: 12*(i+1)] = this_color

            this_verts = self.makeBox(voxel_id, self._meta)
            faces[12*i:12*(i+1)] = self._faces_template + 8*i
            verts[8*i:8*(i+1)] = this_verts


            i += 1

        colors = colors[0:i*12]
        faces  = faces[0:i*12]
        verts  = verts[0:i*8]


        return verts, faces, colors

    def makeBox(self, voxel_id, meta):
        verts_box = numpy.copy(self._box_template)
        #Scale all the points of the box to the right voxel size:
        verts_box[:,0] *= meta.voxel_dimensions(0)
        verts_box[:,1] *= meta.voxel_dimensions(1)
        verts_box[:,2] *= meta.voxel_dimensions(2)


        #Shift the points to put the center of the cube at (0,0,0)
        verts_box[:,0] -= 0.5*meta.voxel_dimensions(0)
        verts_box[:,1] -= 0.5*meta.voxel_dimensions(1)
        verts_box[:,2] -= 0.5*meta.voxel_dimensions(2)
        
        #Move the points to the right coordinate in this space
        verts_box[:,0] += meta.position(voxel_id, 0) - meta.origin(0)
        verts_box[:,1] += meta.position(voxel_id, 1) - meta.origin(1)
        verts_box[:,2] += meta.position(voxel_id, 2) - meta.origin(2)


        # color_arr = numpy.ndarray((12, 4))
        # color_arr[:] = [1,1,1,1]

        return verts_box


    def getColor(self, _lookupTable, _levels, _voxel_value ):
        _min = _levels[0]
        _max = _levels[1]

        if _voxel_value >= _max:
            # print "Max " + str(_voxel_value)
            return _lookupTable[-1]
        elif _voxel_value < _min:
            # print "Min "  + str(_voxel_value)
            return (0,0,0,0)
        else:
            index = 255*(_voxel_value - _min) / (_max - _min)
            return _lookupTable[int(index)]


    def clearDrawnObjects(self, view_manager):
        if self._gl_voxel_mesh is not None:
            view_manager.getView().removeItem(self._gl_voxel_mesh)

        self._gl_voxel_mesh = None
        self._meta = None
        self._id_summed_charge = dict()

    def refresh(self, view_manager):
        self.redraw(view_manager)