from database import recoBase
from pyqtgraph.Qt import QtGui, QtCore
import numpy
try:
    import pyqtgraph.opengl as gl
except:
    print "Error, must have open gl to use this viewer."
    exit(-1)

class voxel3d(recoBase):

    """docstring for voxel3d"""

    def __init__(self):
        super(voxel3d, self).__init__()
        self._productName = 'voxel3d'
        self._product_id = 5
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

        #Get the list of voxel3d sets:
        event_voxel3d = io_manager.get_data(self._product_id, str(self._producerName))

        voxels = event_voxel3d.GetVoxelSet()
        self._meta = event_voxel3d.GetVoxelMeta() 

        view_manager.getView().updateMeta(self._meta)

        self._id_summed_charge = dict()
        # # This section draws voxels onto the environment:
        for voxel in voxels:
            if voxel.ID() in self._id_summed_charge:
                self._id_summed_charge[voxel.ID()] += voxel.Value()
            else:
                self._id_summed_charge.update({voxel.ID() : voxel.Value()})

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
        self._gl_voxel_mesh = mesh
        view_manager.getView().addItem(mesh)

    def buildTriangleArray(self, id_summed_charge, view_manager):
        verts = None
        faces = None
        colors = None

        i = 0
        for voxel_id in id_summed_charge:

            # Don't draw this pixel if it's below the threshold:
            if id_summed_charge[voxel_id] < view_manager.getLevels()[0]:
                continue


            this_color = self.getColor(view_manager.getLookupTable(),
                                       view_manager.getLevels(),
                                       id_summed_charge[voxel_id])

            if colors is None:
                colors = numpy.asarray([this_color]*12)
            else:
                colors = numpy.append(colors,
                                      numpy.asarray([this_color]*12),
                                      axis=0)

            # print "({}, {}, {})".format(_pos[0], _pos[1], _pos[2])
            this_verts = self.makeBox(voxel_id, self._meta)

            if faces is None:
                faces = self._faces_template
            else:
                faces = numpy.append(faces, 
                                     self._faces_template + 8*i, 
                                     axis=0)
            if verts is None:
                verts = this_verts
            else:
                verts = numpy.append(verts, 
                                     this_verts, axis=0)

            i += 1

        return verts, faces, colors

    def makeBox(self, voxel_id, meta):
        verts_box = numpy.copy(self._box_template)
        #Scale all the points of the box to the right voxel size:
        verts_box[:,0] *= meta.SizeVoxelX()
        verts_box[:,1] *= meta.SizeVoxelY()
        verts_box[:,2] *= meta.SizeVoxelZ()

        #Shift the points to put the center of the cube at (0,0,0)
        verts_box[:,0] -= 0.5*meta.SizeVoxelX()
        verts_box[:,1] -= 0.5*meta.SizeVoxelY()
        verts_box[:,2] -= 0.5*meta.SizeVoxelZ()
        
        #Move the points to the right coordinate in this space

        verts_box[:,0] += meta.X(voxel_id) - meta.MinX()
        verts_box[:,1] += meta.Y(voxel_id) - meta.MinY()
        verts_box[:,2] += meta.Z(voxel_id) - meta.MinZ()


        # color_arr = numpy.ndarray((12, 4))
        # color_arr[:] = [1,1,1,1]

        return verts_box

    def getColor(self, _lookupTable, _levels, _voxel_value ):
        _min = _levels[0]
        _max = _levels[1]

        if _voxel_value > _max:
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