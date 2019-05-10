from .database import recoBase
from larcv import larcv
import copy
# import numpy
class image2d(recoBase):

    """docstring for cluster"""

    def __init__(self):
        super(image2d, self).__init__()
        self._product_name = 'image2d'

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):


        image2d_array = io_manager.get_data(self._product_name, str(self._producerName))
        image2d_array = larcv.EventImage2D.to_image2d(image2d_array)

 
        self._data_arr = []

        for image2d_plane in image2d_array.image2d_array():
            thisView = view_manager.getViewPorts()[image2d_plane.meta().id()]
            self._data_arr.append(copy.copy(larcv.as_ndarray(image2d_plane).T))


            thisView.drawPlane(self._data_arr[-1])

        return

    def clearDrawnObjects(self, view_manager):

        for index, view in view_manager.getViewPorts().items():
            view.drawBlank()
