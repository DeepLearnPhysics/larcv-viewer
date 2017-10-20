from database import recoBase
from ROOT import larcv

class image2d(recoBase):

    """docstring for cluster"""

    def __init__(self):
        super(image2d, self).__init__()
        self._productName = 'image2d'
        self._product_id = 0
        larcv.load_pyutil()

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):


        image2d_data = io_manager.get_data(self._product_id, str(self._producerName))

        for image2d_plane in image2d_data.Image2DArray():
            thisView = view_manager.getViewPorts()[image2d_plane.meta().plane()]

            image_as_ndarray = larcv.as_ndarray(image2d_plane)
            thisView._item.setImage(image_as_ndarray)

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
