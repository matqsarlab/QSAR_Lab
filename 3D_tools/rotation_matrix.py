#!/usr/bin/env python

import numpy as np


def rotation_matrix_from_vectors(u, v):
    """Find the rotation matrix that aligns u to v
    :param u: A 3d "source" vector
    :param v: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to u, aligns it with v.
    """
    a, b = (u / np.linalg.norm(u)).reshape(3), (v / np.linalg.norm(v)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat @ kmat * ((1 - c) / (s**2))
    return rotation_matrix
