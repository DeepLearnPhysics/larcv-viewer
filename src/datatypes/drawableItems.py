from .image2d    import image2d
from .pixel2d    import pixel2d
from .particle2d import particle2d
from .cluster2d  import cluster2d
from .sparse2d   import sparse2d
from .bbox2d     import bbox2d
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
        self._drawableClasses.update({'Image2D':     [image2d, 'image2d']})
        self._drawableClasses.update({'Cluster2D':   [cluster2d, 'cluster2d']})
        self._drawableClasses.update({'Sparse2D':    [sparse2d, 'sparse2d']})
        # self._drawableClasses.update({'Particle 2D': [particle2d, 'particle']})
        self._drawableClasses.update({'BBox 2D':     [bbox2d, 'bbox2d']})

    def getListOfTitles(self):
        return self._drawableClasses.keys()

    def getListOfItems(self):
        return zip(*self._drawableClasses.values())[1]

    def getDict(self):
        return self._drawableClasses


from .sparse3d import sparse3d
from .cluster3d import cluster3d
from .particle3d import particle3d
class drawableItems3D(object):

    """This class exists to enumerate the drawableItems in 3D"""
    # If you make a new drawing class, add it here

    def __init__(self):
        super(drawableItems3D, self).__init__()
        # items are stored as pointers to the classes (not instances)
        self._drawableClasses = collections.OrderedDict()
        self._drawableClasses.update({'Voxel3d': [sparse3d,"sparse3d"]})
        self._drawableClasses.update({'Cluster3d': [cluster3d,"cluster3d"]})
        # self._drawableClasses.update({'Particle3D': [particle3d,"particle"]})

    def getListOfTitles(self):
        return self._drawableClasses.keys()

    def getListOfItems(self):
        return zip(*self._drawableClasses.values())[1]

    def getDict(self):
        return self._drawableClasses



