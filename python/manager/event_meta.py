
class event_meta(object):

    def __init__(self):
        super(event_meta, self).__init__()

    def n_views(self):
        return max(self._n_views, 1)

    def refresh(self, meta_vec):


        self._n_views = len(meta_vec)

        self._x_min = []
        self._y_min = []
        self._x_max = []
        self._y_max = []
        self._y_n_pixels = []
        self._x_n_pixels = []
        x_ind = 0
        y_ind = 1
        for meta in meta_vec:
            self._x_min.append(meta.origin(0))
            self._y_min.append(meta.origin(1))
            self._x_max.append(meta.image_size(0) + meta.origin(0))
            self._y_max.append(meta.image_size(1) + meta.origin(1))
            self._x_n_pixels.append(meta.number_of_voxels(0))
            self._y_n_pixels.append(meta.number_of_voxels(1))

        for i in range(self._n_views):
            if self._x_min[i] == self._x_max[i]:
                self._x_max[i] = self._x_min[i] + self._x_n_pixels[i]
            if self._y_min[i] == self._y_max[i]:
                self._y_max[i] = self._y_min[i] + self._y_n_pixels[i]


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
            print("ERROR: plane {} not available.".format(plane))
            return ((-1, 1), (-1, 1))

class event_meta3D(object):
    def __init__(self):
        super(event_meta3D, self).__init__()

    def refresh(self, meta):


        x_ind = 0
        y_ind = 1
        z_ind = 2
        self._x_min = meta.origin(x_ind)
        self._y_min = meta.origin(y_ind)
        self._z_min = meta.origin(z_ind)
        self._x_max = meta.image_size(x_ind) + meta.origin(x_ind)
        self._y_max = meta.image_size(y_ind) + meta.origin(y_ind)
        self._z_max = meta.image_size(z_ind) + meta.origin(z_ind)
        self._y_n_pixels = meta.number_of_voxels(x_ind)
        self._x_n_pixels = meta.number_of_voxels(y_ind)
        self._z_n_pixels = meta.number_of_voxels(z_ind)



    def size_voxel_x(self):
        return (self._x_max - self._x_min) / self._x_n_pixels

    def size_voxel_y(self):
        return (self._y_max - self._y_min) / self._y_n_pixels

    def size_voxel_z(self):
        return (self._z_max - self._z_min) / self._z_n_pixels

    def n_voxels_x(self):
        return self._x_n_pixels

    def n_voxels_y(self):
        return self._y_n_pixels

    def n_voxels_z(self):
        return self._z_n_pixels

    def dim_x(self):
        return self._x_max - self._x_min

    def dim_y(self):
        return self._y_max - self._y_min

    def dim_z(self):
        return self._z_max - self._z_min

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
