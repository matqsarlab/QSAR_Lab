#!/usr/bin/env python
import numpy as np
import pandas as pd
from QSAR_Lab.Space_Tools.rotation_matrix import quaternion_rotation_matrix


class NM_translate:
    def __init__(self, object: str) -> None:
        self.object = object
        pass

    @property
    def load_xyz(self) -> pd.DataFrame:
        d = {"name": [], "x": [], "y": [], "z": []}

        with open(self.object, "r") as f:
            next(f)
            next(f)
            for i in f:
                s = i.split()

                d["name"].append(s[0])
                d["x"].append(s[1])
                d["y"].append(s[2])
                d["z"].append(s[3])
        return pd.DataFrame(d)

    @property
    def get_coordinate(self):
        return np.array(self.load_xyz[["x", "y", "z"]].astype(float))

    @property
    def get_name(self):
        return np.array(self.load_xyz["name"])

    @property
    def translate_center_to_zero(self):
        return self.get_coordinate - np.mean(self.get_coordinate, axis=0)

    @property
    def max_dist(self):
        data = self.translate_center_to_zero
        r0 = np.mean(data, axis=0)
        d = np.linalg.norm(
            np.subtract(data[0, :], r0)
        )  # Distance between coordinate and origin
        dist_index = 0  # Index number
        dist_coor = 0  # Coordinate

        for i, ri in enumerate(data):
            if np.linalg.norm(ri - r0) > d:
                d = np.linalg.norm(ri - r0)
                dist_index = i
                dist_coor = ri

        return {"index": dist_index, "coordinate": dist_coor, "distance_from_center": d}

    @property
    def vec_direct(self):
        mmin = np.min(self.translate_center_to_zero, axis=0)
        return np.array([0, mmin[1], 0])


class AA_add_transpose(NM_translate):
    def __init__(self, object: str, object2: str) -> None:
        self.object = object
        self.object2 = object2

    @property
    def rotate_object(self):
        v = super().vec_direct
        super().__init__(self.object2)
        new_xyz_obj2 = super().translate_center_to_zero
        u = super().max_dist["coordinate"]
        angle = np.arccos((u @ v) / (np.linalg.norm(u) * np.linalg.norm(v)))
        axis = np.cross(u, v) / np.linalg.norm(np.cross(u, v))
        q = np.append(np.cos(angle / 2), np.sin(angle / 2) * axis)
        rot_matrix = -quaternion_rotation_matrix(q)
        u_rotated = rot_matrix @ u
        new_xyz_obj2 = (rot_matrix @ new_xyz_obj2.T).T
        return new_xyz_obj2 + 1.5 * v - u_rotated
