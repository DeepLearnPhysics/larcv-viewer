from image2d import image2d
from pixel2d import pixel2d
from particle2d import particle2d
from cluster2d import cluster2d

# This is the class that maintains the list of drawable items.
# If your class isn't here, it can't be drawn
import collections


class drawableItems(object):

    """This class exists to enumerate the drawableItems"""
    # If you make a new drawing class, add it here

    def __init__(self):
        super(drawableItems, self).__init__()
        # items are stored as pointers to the classes (not instances)
        self._drawableClasses = collections.OrderedDict()
        self._drawableClasses.update({'Image2D': [image2d, 'image2d']})
        self._drawableClasses.update({'Cluster2D': [cluster2d, 'cluster2d']})
        self._drawableClasses.update({'Particle 2D': [particle2d, 'particle']})

    def getListOfTitles(self):
        return self._drawableClasses.keys()

    def getListOfItems(self):
        return zip(*self._drawableClasses.values())[1]

    def getDict(self):
        return self._drawableClasses


try:
    import pyqtgraph.opengl as gl
    from voxel3d import voxel3d
    from cluster3d import cluster3d
    class drawableItems3D(object):

        """This class exists to enumerate the drawableItems in 3D"""
        # If you make a new drawing class, add it here

        def __init__(self):
            super(drawableItems3D, self).__init__()
            # items are stored as pointers to the classes (not instances)
            self._drawableClasses = collections.OrderedDict()
            self._drawableClasses.update({'Voxel3d': [voxel3d,"voxel3d"]})
            self._drawableClasses.update({'Cluster3d': [cluster3d,"cluster3d"]})

        def getListOfTitles(self):
            return self._drawableClasses.keys()

        def getListOfItems(self):
            return zip(*self._drawableClasses.values())[1]

        def getDict(self):
            return self._drawableClasses



except:
    pass

