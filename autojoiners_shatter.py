import numpy as np
from scipy.spatial import Voronoi
from voronoi_region_plot import voronoi_finite_polygons_2d


class ShatterSource():
    def __init__(self, size, nregions):
        self.size = size
        self.nregions = nregions

    def shatter(self):
        raise NotImplementedError


class RegularSquareShatter(ShatterSource):
    def __init__(self, size, nregions,
                 sidelength=80, borderpc=0.1):
        self.size = size
        self.borderpc = borderpc
        self.sidelength = sidelength

    def shatter(self):
        all_shards = []

        y = self.sidelength
        while y < self.size[0]:
            x = self.sidelength

            while x < self.size[1]:
                coordinates = [(x, y),
                               (x - self.sidelength, y),
                               (x - self.sidelength, y - self.sidelength),
                               (x, y - self.sidelength)]
                all_shards.append(coordinates)
                x += (1 + self.borderpc) * self.sidelength

            y += (1 + self.borderpc) * self.sidelength

        return all_shards


class VoroiShatter(ShatterSource):
    def __init__(self, size, nregions):
        super().__init__(size, nregions)
        self.shatter_data = None

    def shatter(self):
        if self.shatter_data is None:
            self.shatter_data = self._create_shatter()

        return self.shatter_data

    def _create_shatter(self):
        centre_points = np.random.rand(self.nregions, 2) * np.array(self.size)
        voronoi_data = Voronoi(centre_points)
        regions, vertices = voronoi_finite_polygons_2d(voronoi_data)

        regions = [r for r in regions if len(r) > 2]
        polygons = [vertices[r] for r in regions]

        return polygons


class RandQuadrilateralShatter(ShatterSource):
    def shatter(self):
        all_shards = []
        for _ in range(self.nregions):
            coordinates = [(np.random.randint(self.size[0]),
                           np.random.randint(self.size[1]))
                           for _ in range(4)]
            all_shards.append(coordinates)
        self.shards = all_shards

        return self.shards


class RandRectangleShatter(ShatterSource):
    def shatter(self):
        all_shards = []
        all_sizes = []
        for _ in range(self.nregions):
            a, b = [np.random.randint(self.size[0]),
                    np.random.randint(self.size[0])]
            x0 = min(a, b)
            x1 = max(a, b)

            a, b = [np.random.randint(self.size[1]),
                    np.random.randint(self.size[1])]
            y0 = min(a, b)
            y1 = max(a, b)

            coordinates = [(x0, y0), (x0, y1), (x1, y1), (x1, y0)]
            size = (y1 - y0) * (x1 - x0)
            all_shards.append(coordinates)
            all_sizes.append(size)

        self.shards = [shard for (size, shard)
                       in sorted(zip(all_sizes, all_shards), reverse=True)]

        return self.shards
