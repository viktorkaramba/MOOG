from functools import lru_cache

from open3d.cpu.pybind.geometry import PointCloud
from open3d.cpu.pybind.io import read_point_cloud, write_point_cloud
from open3d.cpu.pybind.utility import Vector3dVector
from open3d.cpu.pybind.visualization import draw_geometries
from tqdm import tqdm

import points_parser as pp
import numpy as np


class NurbsSurface:
    p = pp.PointsParser()
    degree = 3
    x = []
    y = []
    z = []
    result_points = []
    knot_vector = []
    controls = []
    delta_t = 0.1

    def __init__(self):
        self.p.parse3d()
        self.p.parse_indices()
        self.p.parse_grid_size()
        self.get_knot_vector()
        self.get_controls()

    def get_knot_vector(self):
        self.knot_vector = tuple(range(self.p.get_grid_size()[0] + self.degree + 1))
        return self.knot_vector

    def get_controls(self):
        self.controls = np.arange(max(self.knot_vector), step=self.delta_t)
        return self.controls

    def get_x(self):
        for u in tqdm(self.controls):
            for v in self.controls:
                result = 0
                for i in range(self.p.get_grid_size()[0]):
                    for j in range(self.p.get_grid_size()[1]):
                        result += self.p.points_3d[self.get_index(i, j)][0] * self.getR([i, j], u, v)
                self.x.append(result)
        return self.x

    def get_y(self):
        for u in tqdm(self.controls):
            for v in self.controls:
                result = 0
                for i in range(self.p.get_grid_size()[0]):
                    for j in range(self.p.get_grid_size()[1]):
                        result += self.p.points_3d[self.get_index(i, j)][1] * self.getR([i, j], u, v)
                self.y.append(result)
        return self.y

    def get_z(self):
        for u in tqdm(self.controls):
            for v in self.controls:
                result = 0
                for i in range(self.p.get_grid_size()[0]):
                    for j in range(self.p.get_grid_size()[1]):
                        result += self.p.points_3d[self.get_index(i, j)][2] * self.getR([i, j], u, v)
                self.z.append(result)
        return self.z

    def getR(self, index, u, v):
        if not self.get_numerator(index, u, v):
            return self.get_numerator(index, u, v)
        return self.get_numerator(index, u, v) / self.get_dominator(u, v)

    def get_numerator(self, index, u, v):
        return self.get_n_i_k(u)[index[0]] * self.get_n_j_l(v)[index[1]]

    def get_dominator(self, u, v):
        result = 0
        for i in range(0, self.p.get_grid_size()[0]):
            for j in range(0, self.p.get_grid_size()[1]):
                result += self.get_n_i_k(u)[i] * self.get_n_j_l(v)[j]
        return result

    @lru_cache
    def get_n_i_k(self, u):
        return [self.get_n(u, i, self.degree) for i in range(self.p.get_grid_size()[0])]

    @lru_cache
    def get_n_j_l(self, v):
        return [self.get_n(v, j, self.degree) for j in range(self.p.get_grid_size()[1])]

    def get_index(self, i, j):
        return self.p.indices.index([i, j])

    @lru_cache
    def get_n(self, u, i, k):
        if k == 1:
            if self.knot_vector[i] <= u < self.knot_vector[i + 1]:
                return 1
            else:
                return 0
        else:
            first = (u - self.knot_vector[i]) / (self.knot_vector[i + k - 1] - self.knot_vector[i])
            second = (self.knot_vector[i + k] - u) / (self.knot_vector[i + k] - self.knot_vector[i + 1])
            return first * self.get_n(u, i, k - 1) + second * self.get_n(u, i + 1, k - 1)

    def show(self):
        pcd = PointCloud()
        pcd.points = Vector3dVector(self.get_result_points())
        write_point_cloud("surface.ply", pcd)
        pcd = read_point_cloud("surface.ply")
        draw_geometries([pcd])

    def get_result_points(self):
        X = self.get_x()
        Y = self.get_y()
        Z = self.get_z()
        for i in range(0, len(X)):
            if X[i] != 0 and Y[i] != 0 and Z[i] != 0:
                self.result_points.append([X[i], Y[i], Z[i]])
        return self.result_points


if __name__ == '__main__':
    surface = NurbsSurface()
    surface.show()