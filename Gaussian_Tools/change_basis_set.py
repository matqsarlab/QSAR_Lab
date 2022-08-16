#!/usr/bin/env python
import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument("-ob", nargs="+")  # old basis set
parser.add_argument("-nb")  # new basis set

options = parser.parse_args()


def ch_basis_set():

    answer = input("Change basis set? y/N: ")

    list_dir = (i for i in options.ob if os.path.isfile(i))

    for path in list_dir:

        dir = os.path.dirname(path)
        with open(path, "r") as old_com, open(
            os.path.join(dir, "atom_info")
        ) as atom_info, open(options.nb, "r") as new_basis:
            lines = old_com.readlines()

            atom_info = atom_info.readlines()
            atom_1 = atom_info[0][1 + atom_info[0].index("=") :].replace("\n", "")

            idx_atom = [e for e, i in enumerate(lines) if atom_1 in i][0]

            new_input = lines[:idx_atom] + new_basis.readlines()

        if answer == "y" or "Y":
            with open(path, "w") as f:
                f.write("".join(new_input))
                f.write("\n")


ch_basis_set()
