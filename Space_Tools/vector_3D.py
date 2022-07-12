#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D, proj3d


class Arrow3D(FancyArrowPatch):
    """
    1) Wprowadz koordynaty wektora:
       -----------------------------------------
        [origin[0], end[0]],
        [origin[1], end[1]],
        [origin[2], end[2]],
       -----------------------------------------
        arrowstyle="->",   <--- styl strzalki
        color="purple",    <--- kolor strzalki
        lw=3,              <--- grubosc strzalki
        mutation_scale=25, <--- rozmiar grotu
       -----------------------------------------

     2) Dodaj wektor do rysunku
        ax.add_artist(arw)
    """

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


def load_xyz(file_name):
    d = {"name": [], "x": [], "y": [], "z": []}

    with open(file_name, "r") as f:
        next(f)
        next(f)
        for i in f:
            s = i.split()

            d["name"].append(s[0])
            d["x"].append(s[1])
            d["y"].append(s[2])
            d["z"].append(s[3])
    return pd.DataFrame(d)


df = load_xyz("./AA_samples/ALA.xyz")

name = np.array(df["name"])
coor = np.array(df[["x", "y", "z"]].astype(float))


def center_of_object(data: np.ndarray):
    return np.mean(data, axis=0)


def max_dist(data: np.ndarray, r0: np.ndarray):
    d = np.linalg.norm(
        np.subtract(data[0, :], r0)
    )  # Distance between coordinate and origin
    i = 0  # Index number
    ri = 0  # Coordinate

    for i, ri in enumerate(data):
        if np.linalg.norm(ri - r0) > d:
            d = np.linalg.norm(ri - r0)
    return {"index": i, "coordinate": ri, "distance_from_center": d}


x = max_dist(coor, center_of_object(coor))
O = center_of_object(coor)

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection="3d")

ax.scatter(coor[:, 0], coor[:, 1], coor[:, 2], s=24)
ax.scatter(x["coordinate"][0], x["coordinate"][1], x["coordinate"][2], s=100, c="green")
ax.scatter(O[0], O[1], O[2], s=100, c="red")

arw = Arrow3D(
    [O[0], x["coordinate"][0]],
    [O[1], x["coordinate"][1]],
    [O[2], x["coordinate"][2]],
    arrowstyle="->",
    color="purple",
    lw=3,
    mutation_scale=25,
)
ax.add_artist(arw)
plt.show()
