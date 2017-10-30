from database import recoBase
from pyqtgraph.Qt import QtGui, QtCore
import numpy
try:
    import pyqtgraph.opengl as gl
except:
    print "Error, must have open gl to use this viewer."
    exit(-1)

class cluster3d(recoBase):

    """docstring for cluster3d"""

    def __init__(self):
        super(cluster3d, self).__init__()
        self._product_name = 'cluster3d'

        self._listOfClusters = []

        self._gl_voxel_mesh = None
        self._id_summed_charge = []
        self._assigned_colors = []

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

        # Defining the cluster3d colors:
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

        #Get the list of cluster3d sets:
        event_cluster3d = io_manager.get_data(self._product_name, str(self._producerName))

        print event_cluster3d.size()

        self._meta = event_cluster3d.meta()

        self._id_summed_charge = dict()

        _color_index = 0

        # # This section draws voxels onto the environment:
        for cluster in event_cluster3d.as_vector():

            _this_id_summed_charge = dict()
            for voxel in cluster.as_vector():
                if voxel.ID() ==self._meta.invalid_voxel_id():
                    continue
                if voxel.ID() in _this_id_summed_charge:
                    _this_id_summed_charge[voxel.ID()] += voxel.Value()
                else:
                    _this_id_summed_charge.update({voxel.ID() : voxel.Value()})

            self._id_summed_charge.append(_this_id_summed_charge)
            self._assigned_colors.append(self._clusterColors[_color_index])

            _color_index += 1
            if _color_index >= len(self._clusterColors):
                _color_index = 0


        self.redraw(view_manager)



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
        view_manager.getView().addItem(self._gl_voxel_mesh)

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
        verts_box[:,0] *= meta.size_voxel_x()
        verts_box[:,1] *= meta.size_voxel_y()
        verts_box[:,2] *= meta.size_voxel_z()

        #Shift the points to put the center of the cube at (0,0,0)
        verts_box[:,0] -= 0.5*meta.size_voxel_x()
        verts_box[:,1] -= 0.5*meta.size_voxel_y()
        verts_box[:,2] -= 0.5*meta.size_voxel_z()
        
        #Move the points to the right coordinate in this space

        verts_box[:,0] += meta.pos_x(voxel_id) - meta.min_x()
        verts_box[:,1] += meta.pos_y(voxel_id) - meta.min_y()
        verts_box[:,2] += meta.pos_z(voxel_id) - meta.min_z()


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
        i_plane = 0
        # erase the clusters
        for plane in self._listOfClusters:
            view = view_manager.getViewPorts()[i_plane]
            i_plane += 1
            for cluster in plane:
                cluster.clearHits(view)


        self._listOfClusters = []
