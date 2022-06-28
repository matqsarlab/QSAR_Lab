#!/usr/bin/env python3

import sys

filelist = sys.argv[1:]

atomic_num = {"C":6, "O":8, "H":1, "N":7, "S":16}

class Electrons:
    
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.elements_dict = {k:{"atomic_num":atomic_num[k], "count":0} for k in atomic_num}

    @property
    def electrons(self):

        # open *.xyz file
        with open(self.file_name, "r") as f:
            next(f) # leave first line
            next(f) # leave second line

            for i in f:
              
                # split and count
                i = i.split()[0]   # choose first element (atom name) from list
                self.elements_dict[i]['count'] += 1   # count specific atom in *.xyz 


        # calc type of atoms in *.xyz 
        e = 0
        for i in self.elements_dict:
            e += self.elements_dict[i]["atomic_num"] * self.elements_dict[i]["count"]
        return print(f"{self.file_name}: {e} elektronow")


# Create instances for every argument (file name) from list, and calc electrons
for i in filelist:
    ins = Electrons(i)
    ins.electrons
