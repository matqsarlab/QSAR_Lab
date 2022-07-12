#!/usr/bin/env python

import numpy as np


def align_vectors(u, v):
    """
    Wyrownywanie dwoch wektorow w przestrzeni 3D za pomoca kwaternionow.
    Obrot wektora o kat.
    """
    theta = np.arccos(
        (u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))
    )  # Kat miedzy wektorami u, v
    axis = np.cross(u, v) / np.linalg.norm(
        np.cross(u, v)
    )  # obliczenie osi obrotu za pomoca iloczynu wektorowego
    norm_u = np.linalg.norm(u)  # obliczenie normy wektora
    u = np.append([0], u / norm_u)
    q = np.append(np.cos(theta / 2), np.sin(theta / 2) * axis)
    q_ = np.append(np.cos(theta / 2), np.sin(theta / 2) * -axis)

    def mult_quat(q1, q2):
        """
        Quaternion multiplication.
        """
        q3 = np.copy(q1)
        q3[0] = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]
        q3[1] = q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2]
        q3[2] = q1[0] * q2[2] - q1[1] * q2[3] + q1[2] * q2[0] + q1[3] * q2[1]
        q3[3] = q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1] + q1[3] * q2[0]
        return q3

    return mult_quat(q, mult_quat(u, q_))[1:] * norm_u
