#!/usr/bin/env python
import argparse
import os

import numpy as np

from QSAR_Lab.Space_Tools.Align_two_3D_object import (AA_add_transpose,
                                                      NM_translate)

parser = argparse.ArgumentParser()
parser.add_argument("--f1", nargs="+")
parser.add_argument("--f2", nargs="+")
parser.add_argument("-all", action="store_true")

options = parser.parse_args()
zero = [0, 0, 0]

if options.all:

    dir = input("Wrpowadz nazwe katalogu lub wcisnij ENTER: ")

    if dir == "":
        dir = "New_XYZ_structers"

    path = str()

    if not os.path.isdir(dir):
        os.mkdir(dir)

    for i in options.f1:
        for j in options.f2:
            obj1 = NM_translate(i)
            xyz_obj1 = obj1.translate_center_to_zero

            obj2 = AA_add_transpose(i, j)
            xyz_obj2 = obj2.rotate_object
            name = np.append(obj1.get_name, obj2.get_name)

            xyz_str = np.append(xyz_obj1, xyz_obj2, axis=0).round(decimals=4)

            xyz_str = np.array(
                ["{:.5f}".format(line) for line in xyz_str.flatten()]
            ).reshape(xyz_str.shape)

            if "/" in i or j:
                path = j.split("/")[-1].replace(".xyz", "") + "_" + i.split("/")[-1]

            with open(os.path.join(dir, path), "w") as f:
                f.write(str(len(xyz_str)) + "\n")
                f.write("XYZ file generated by Script\n")
                for coor, n in zip(xyz_str, name):
                    f.write(
                        "{}{:>20}{:>13}{:>13}\n".format(n, coor[0], coor[1], coor[2])
                    )
else:
    try:
        fname1 = options.f1[0]
        fname2 = options.f2[0]
    except:
        print("Can't find an argument (Gaussian log file).")
    else:
        obj1 = NM_translate(fname1)
        xyz_obj1 = obj1.translate_center_to_zero

        obj2 = AA_add_transpose(fname1, fname2)
        xyz_obj2 = obj2.rotate_object
        name = np.append(obj1.get_name, obj2.get_name)

        xyz_str = np.append(xyz_obj1, xyz_obj2, axis=0).round(decimals=4)

        xyz_str = np.array(
            ["{:.5f}".format(line) for line in xyz_str.flatten()]
        ).reshape(xyz_str.shape)

        print(str(len(xyz_str)))
        print("XYZ file generated by Script")
        for coor, n in zip(xyz_str, name):
            print("{}{:>20}{:>13}{:>13}".format(n, coor[0], coor[1], coor[2]))