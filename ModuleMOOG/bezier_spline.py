import math
import matplotlib.pyplot as plt

import numpy as np
import points_parser as pp


def get_value(j, a, i):
    return (math.pow(1 - j, 3) * a[i]) \
           + (3 * j * (math.pow(1 - j, 2)) * a[i + 1]) \
           + (3 * (math.pow(j, 2)) * (1 - j) * a[i + 2]) \
           + (math.pow(j, 3) * a[i + 3])


class SplineBezier:
    t = 1
    delta_t = 0.01
    x = []
    y = []
    points = pp.PointsParser()

    def __init__(self):
        self.points.parse2d()

    def get_x(self):
        index = 0
        print(self.points.get_points_2d())
        for i in range(0, 3):
            for j in np.arange(0, self.t, self.delta_t):
                self.x.append(get_value(j, self.points.get_x_2d(), index))
            index += 3
        return self.x

    def get_y(self):
        index = 0
        for i in range(0, 3):
            for j in np.arange(0, self.t, self.delta_t):
                self.y.append(get_value(j, self.points.get_y_2d(), index))
            index += 3
        return self.y

    def show_graphic(self):
        plt.plot(self.points.get_x_2d(), self.points.get_y_2d(), marker='o')
        plt.plot(self.get_x(), self.get_y())
        plt.show()


if __name__ == '__main__':
    spline = SplineBezier()
    spline.show_graphic()