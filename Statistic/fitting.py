#!/usr/bin/env python3
import numpy as np


def poly_eq(x, y, degree):
    return np.poly1d(np.polyfit(x, y, degree))
