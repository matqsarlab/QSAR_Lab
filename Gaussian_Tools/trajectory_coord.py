#!/usr/bin/env python3

import sys


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
    def standar_orientation(self):

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

        uklad = {"6":"C", "8":"O", "1":"H", "16":"S","7":"N"}

        so = self.standar_orientation
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
                xxx = list(uklad[s[1]]) + s[3:]

                # new_coor.append(f'{xxx[0]}      {xxx[1]}   {xxx[2]}   {xxx[3]}')
                new_coor.append('{}{:>20}{:>13}{:>13}'.format(xxx[0], xxx[1], xxx[2], xxx[3]))
                # print('{}{:>20}{:>13}{:>13}'.format(xxx[0], xxx[1], xxx[2], xxx[3]))
                    
        return new_coor



try:
    fname = sys.argv[1]
except:
    print("Can't find an argument (Gaussian log file).")
else:
    ins = Read(fname)
    ins.standar_orientation
    x = ins.make_xyz

    for i in x:
        print(i)
    # x = ins.standar_orientation
    # for i in x:
    #     print(i)
    # print(ins.make_xyz)
