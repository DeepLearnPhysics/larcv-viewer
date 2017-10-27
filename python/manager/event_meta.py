
class event_meta(object):

    def __init__(self):
        super(event_meta, self).__init__()
        self._image_metas = dict()
    
    def n_views(self):
        return max(self._n_views, 1)

    def refresh(self, _larcv_meta):

        self._n_views = _larcv_meta.get_int("n_planes")
        self._x_min   = _larcv_meta.get_darray('x_min')
        self._y_min   = _larcv_meta.get_darray('y_min')
        self._x_max   = _larcv_meta.get_darray('x_max')
        self._y_max   = _larcv_meta.get_darray('y_max')
        self._y_n_pixels = _larcv_meta.get_darray("y_n_pixels")
        self._x_n_pixels = _larcv_meta.get_darray("x_n_pixels")

    def cols(self, plane):
        return self._x_n_pixels[plane]

    def width(self, plane):
        return self._x_max[plane] - self._x_min[plane]

    def comp_x(self, plane):
        return self.width(plane) / self.cols(plane)
    
    def rows(self, plane):
        return self._y_n_pixels[plane]

    def height(self, plane):
        return self._y_max[plane] - self._y_min[plane]

    def comp_y(self, plane):
        return self.height(plane) / self.rows(plane)

    def wire_to_col(self, wire, plane):
        return self.cols(plane) * (1.0*(wire - self.min_x(plane)) / self.width(plane))

    def time_to_row(self, time, plane):
        return self.rows(plane) * (1.0*(time - self.min_y(plane)) / self.height(plane))


    def min_y(self, plane):
        return self._y_min[plane]

    def max_y(self, plane):
        return self._y_max[plane]

    def min_x(self, plane):
        return self._x_min[plane]

    def max_x(self, plane):
        return self._x_max[plane]




    # def meta(self, plane):
    #     return self._image_metas[plane]

    # def row_to_wire(self, row, plane):
    #     return self._image_metas[plane].pos_x(row)

    # def col_to_time(self, col, plane):
    #     return self._image_metas[plane].pos_y(col)

    # def wire_to_col(self, wire, plane):
    #     return  (wire - self._image_metas[plane].tl().x) / self._image_metas[plane].pixel_width()

    # def time_to_row(self, time, plane):
    #     return  (self._image_metas[plane].tl().y - time) / self._image_metas[plane].pixel_height()
    #     # return self._image_metas[plane].row(time)

    def range(self, plane):
        if plane >= 0 and plane < self._n_views:
            return ((self._x_min[plane], self._x_min[plane] ),
                    (self._x_min[plane], self._x_min[plane]))
        else:
            print "ERROR: plane {} not available.".format(plane)
            return ((-1, 1), (-1, 1))
