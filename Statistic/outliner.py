#!/usr/bin/env python3

import numpy as np


def zscore_outliers(data_y: list, threshold: int = 3) -> np.ndarray:
    """Find outlier point - bigger 3_sigma. Return boolean mask"""
    mean = np.mean(data_y)
    std = np.std(data_y)

    z = np.array([abs((i - mean) / std) for i in data_y])
    mask = np.where(z < threshold, True, False)
    return mask
