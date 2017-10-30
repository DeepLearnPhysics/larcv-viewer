
class event_meta(object):

    def __init__(self):
        super(event_meta, self).__init__()
    
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



    def range(self, plane):
        if plane >= 0 and plane < self._n_views:
            return ((self._x_min[plane], self._x_min[plane] ),
                    (self._x_min[plane], self._x_min[plane]))
        else:
            print "ERROR: plane {} not available.".format(plane)
            return ((-1, 1), (-1, 1))

class event_meta3D(object):
    def __init__(self):
        super(event_meta3D, self).__init__()

    def refresh(self, _larcv_meta):

        self._x_min   = _larcv_meta.get_double('x_min')
        self._y_min   = _larcv_meta.get_double('y_min')
        self._z_min   = _larcv_meta.get_double('z_min')
        self._x_max   = _larcv_meta.get_double('x_max')
        self._y_max   = _larcv_meta.get_double('y_max')
        self._z_max   = _larcv_meta.get_double('z_max')
        self._y_n_pixels = _larcv_meta.get_double("y_n_pixels")
        self._x_n_pixels = _larcv_meta.get_double("x_n_pixels")
        self._z_n_pixels = _larcv_meta.get_double("z_n_pixels")


    def n_voxels_x(self):
        return self._x_n_pixels

    def n_voxels_y(self):
        return self._y_n_pixels

    def n_voxels_z(self):
        return self._y_n_pixels

    def dim_x(self):
        return self._x_max

    def dim_y(self):
        return self._y_max

    def dim_z(self):
        return self._z_max

    def width(self):
        return self.dim_x()

    def height(self):
        return self.dim_y()

    def length(self):
        return self.dim_z()

    def min_y(self):
        return self._y_min

    def max_y(self):
        return self._y_max

    def min_x(self):
        return self._x_min

    def max_x(self):
        return self._x_max

    def min_z(self):
        return self._z_min    

    def max_z(self):
        return self._z_max
