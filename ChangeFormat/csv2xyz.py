import os

import numpy as np
import pandas as pd

path = "../<Name-To-Directory>"
list_paths = []
for (dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
        if filename.endswith(".csv"):
            list_paths.append(os.sep.join([dirpath, filename]))


def writer_xyz(func):
    def wrapper(*args):
        name = os.path.split(*args)[1]
        name = name.replace(".csv", ".xyz")
        inside = func(*args)

        with open(name, "w") as f:
            f.write(f"{inside.shape[0]}\n")
            f.write("Generated by Script\n")

        with open(name, "a") as f:
            for line in inside:
                f.write(f"{line[0]:<8} {line[1]:>10} {line[2]:>10} {line[3]:>10}\n")
        return 0

    return wrapper


@writer_xyz
def convert_csv2xyz(filename):
    df = pd.read_csv(filename)
    matrix = np.array(df)[:, [2, 3, 4, 5]]
    atom = matrix[:, 0]
    xyz = np.around(10 * matrix[:, 1:].astype(float), 4)  # convert from nm -> angstrem
    return np.vstack((atom, xyz.T)).T
