
class event_meta(object):

    def __init__(self):
        super(event_meta, self).__init__()
        self._image_metas = dict()
    
    def n_views(self):
        return max(len(self._image_metas), 1)

    def refresh(self, larcv_event_image2d):

        for image2d in larcv_event_image2d.Image2DArray():
            _meta = image2d.meta()
            self._image_metas[_meta.plane()] = _meta

    def meta(self, plane):
        return self._image_metas[plane]

    def row_to_wire(self, row, plane):
        return self._image_metas[plane].pos_x(row)

    def col_to_time(self, col, plane):
        return self._image_metas[plane].pos_y(col)

    def wire_to_col(self, wire, plane):
        return  (wire - self._image_metas[plane].tl().x) / self._image_metas[plane].pixel_width()

    def time_to_row(self, time, plane):
        return  (self._image_metas[plane].tl().y - time) / self._image_metas[plane].pixel_height()
        # return self._image_metas[plane].row(time)

    def range(self, plane):
        if plane in self._image_metas.keys():
            _this_meta = self._image_metas[plane]
            return ((_this_meta.tl().x, _this_meta.tr().x ),
                    (_this_meta.bl().y, _this_meta.tl().y))
        else:
            print "ERROR: plane {} not available.".format(plane)
            return ((-1, 1), (-1, 1))