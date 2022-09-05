#!/usr/bin/env python3

import argparse
import os


class Read:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.counter = 0

    @property
    def gen(self):
        with open(self.filename, "r") as f:
            for i in f:
                yield i

    @property
    def standard_orientation(self):

        xyz = []
        x = self.gen

        for i in x:
            if "Standard orientation" in i:
                self.counter = 0
                xyz.append("line with atom numbers")

                _ = [next(x) for _ in range(4)]

                # xyz = []
                for j in x:

                    if "-\n" in j:
                        break

                    xyz.append(j)
                    self.counter += 1
        return xyz

    @property
    def make_xyz(self):

        uklad = {
            "6": "C",
            "8": "O",
            "1": "H",
            "16": "S",
            "7": "N",
            "14": "Si",
            "47": "Ag",
            "79": "Au",
        }

        so = self.standard_orientation
        new_coor = []
        step = 0
        time = 0

        for i in so:
            s = i.split()

            if "line with atom numbers" in i:
                new_coor.append(self.counter)
                new_coor.append("i = {}, time = {}".format(step, time))
                step += 1
                time += 2

            if s[1] in uklad.keys():
                xxx = [uklad[s[1]]] + s[3:]

                # new_coor.append(f'{xxx[0]}      {xxx[1]}   {xxx[2]}   {xxx[3]}')
                new_coor.append(
                    "{}{:>20}{:>13}{:>13}".format(xxx[0], xxx[1], xxx[2], xxx[3])
                )

        return new_coor


parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="+")
parser.add_argument("-all", action="store_true")

options = parser.parse_args()

if options.all:

    fc = "Final_Trajectories"

    if not os.path.isdir(fc):
        os.mkdir(fc)

    for i in options.filename:
        ins = Read(i)
        # ins.standard_orientation

        x = ins.make_xyz

        if "/" in i:
            s = i.split("/")[-1]
            s = s.replace(".log", ".xyz")

        else:
            s = i.replace(".log", ".xyz")

        with open(os.path.join(fc, s), "w") as f:
            for line in x:
                f.write(str(line) + "\n")
else:
    try:
        fname = options.filename[0]
        # fname = sys.argv[1]
    except:
        print("Can't find an argument (Gaussian log file).")
    else:
        ins = Read(fname)
        # ins.standard_orientation
        x = ins.make_xyz

        for i in x:
            print(i)
