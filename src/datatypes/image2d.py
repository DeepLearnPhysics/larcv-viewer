from .database import recoBase

import larcv
import copy
import numpy
class image2d(recoBase):

    """docstring for cluster"""

    def __init__(self):
        super(image2d, self).__init__()
        self._product_name = 'image2d'

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):


        image2d_array = io_manager.get_data(self._product_name, str(self._producerName))
        # image2d_array = larcv.EventImage2D.to_image2d(image2d_array)

 
        self._data_arr = []

        for i, image2d_plane in enumerate(image2d_array.as_vector()):
            try:
                thisView = view_manager.getViewPorts()[image2d_plane.meta().id()]
            except:
                thisView = view_manager.getViewPorts()[i]

            thisView.drawPlane(image2d_plane.as_array())

        return

    def clearDrawnObjects(self, view_manager):

        for index, view in view_manager.getViewPorts().items():
            view.drawBlank()
