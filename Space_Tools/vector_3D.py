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
