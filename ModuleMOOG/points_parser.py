import json


class PointsParser:
    x_2d = []
    x_3d = []
    y_2d = []
    y_3d = []
    z_3d = []
    points_2d = []
    points_3d = []
    indices = []
    grid_size = []
    def parse2d(self):
        f = open('resources/23.json')
        data = json.load(f)
        for i in data['curve']:
            print(i)
            self.points_2d.append(i)
            self.x_2d.append(i[0])
            self.y_2d.append(i[1])
        f.close()

    def parse3d(self):
        f = open('resources/23.json')
        data = json.load(f)
        for i in data['surface']['points']:
            self.points_3d.append(i)
            self.x_3d.append(i[0])
            self.y_3d.append(i[1])
            self.z_3d.append(i[2])
        f.close()

    def parse_grid_size(self):
        f = open('resources/23.json')
        data = json.load(f)
        self.grid_size.append(data['surface']['gridSize'][0])
        self.grid_size.append(data['surface']['gridSize'][1])
        f.close()

    def parse_indices(self):
        f = open('resources/23.json')
        data = json.load(f)
        for i in data['surface']['indices']:
            self.indices.append(i)
        f.close()

    def get_points_2d(self):
        return self.points_2d

    def get_points_3d(self):
        return self.points_3d

    def get_grid_size(self):
        return self.grid_size

    def get_indices(self):
        return self.indices

    def get_x_2d(self):
        return self.x_2d

    def get_y_2d(self):
        return self.y_2d

    def get_x_3d(self):
        return self.x_3d

    def get_y_3d(self):
        return self.y_3d

    def get_z_3d(self):
        return self.z_3d
