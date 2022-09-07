#!/usr/bin/env python3

import argparse
import os
import time

import numpy as np

# from QSAR_Lab.Gaussian_Tools import final_coord


class Charge:
    def __init__(self, filename, path_to_atom_info) -> None:
        self.filename = filename
        self.mulliken_atoms = []
        self.esp_atoms = []
        self.nbo_atoms = []
        self.path_to_atom_info = path_to_atom_info

    @property
    def gen(self):
        with open(self.filename, "r") as f:
            for i in f:
                yield i

    @property
    def find_line(self) -> tuple:
        x = self.gen

        def selector():

            _ = [next(x) for _ in range(1)]

            charges_list = []
            for j in x:

                if "Sum of" in j or "====" in j:
                    break

                charges_list.append(j)
            return charges_list

        mulliken_ = []
        esp_ = []
        nbo_ = []

        for i in x:

            if "Mulliken charges:" in i:
                mulliken_ = selector()
            if "ESP charges:" in i:
                esp_ = selector()
            if "Charge         Core      Valence    Rydberg      Total" in i:
                nbo_ = selector()

        return mulliken_, esp_, nbo_

    @property
    def charges_table(self):
        def create_table(kind_charge):
            table = []
            for i in kind_charge:
                s = i.split()
                table.append("{:>3}{:>10}{:>13}".format(s[0], s[1], s[2]))
            return table

        mulliken_ = create_table(self.find_line[0])
        esp_ = create_table(self.find_line[1])
        nbo_ = create_table(self.find_line[2])

        return mulliken_, esp_, nbo_

    def specific_atoms_charge(self, switcher1=False, switcher2=False, switcher3=False):

        mulliken_specific_atoms = []
        esp_specific_atoms = []
        nbo_specific_atoms = []

        def arthmetic(name, list_with_atoms):
            mull_values = list(map(lambda x: float(x.split()[-1]), list_with_atoms))
            list_with_atoms.insert(0, "-" * 88)
            list_with_atoms.insert(1, name)
            list_with_atoms.insert(2, "-" * 88)
            list_with_atoms.append("Sum of {}: {:>5}".format(name, np.sum(mull_values)))
            list_with_atoms.append(
                "Mean of {}: {:>5}".format(name, np.mean(mull_values))
            )
            return mull_values

        def spec_number(list_spec_atoms):
            list_spec_atoms = line[line.index("{") + 1 : line.index("}")].split(",")
            list_spec_atoms = [s.replace(" ", "") for s in list_spec_atoms]
            return list_spec_atoms

        # tutaj funkcjonalnosc wczytywania pliku z specyfikacja atomow
        with open(self.path_to_atom_info, "r") as atom_spec:

            for line in atom_spec:

                if "mulliken" in line.lower() and switcher1 == True:
                    mulliken_specific_atoms = spec_number(mulliken_specific_atoms)

                if "esp" in line.lower() and switcher2 == True:
                    esp_specific_atoms = spec_number(esp_specific_atoms)

                if "nbo" in line.lower() and switcher3 == True:
                    nbo_specific_atoms = spec_number(nbo_specific_atoms)

        # tworzenie listy z ladunkami mullikena dla wybranych atomow
        if mulliken_specific_atoms and mulliken_specific_atoms[0].lower() != "all":

            for i in mulliken_specific_atoms:
                for j in self.charges_table[0]:
                    if i == j.split()[0]:
                        self.mulliken_atoms.append(j)

            arthmetic("Mulliken charges", self.mulliken_atoms)

        elif mulliken_specific_atoms and mulliken_specific_atoms[0].lower() == "all":

            for i in self.charges_table[0]:
                self.mulliken_atoms.append(i)

            arthmetic("Mulliken charges", self.mulliken_atoms)

        # tworzenie listy z ladunkami ESP dla wybranych atomow
        if esp_specific_atoms and esp_specific_atoms[0].lower() != "all":

            for i in esp_specific_atoms:
                for j in self.charges_table[1]:
                    if i == j.split()[0]:
                        self.esp_atoms.append(j)

            arthmetic("ESP charges", self.esp_atoms)

        elif esp_specific_atoms and esp_specific_atoms[0].lower() == "all":

            for i in self.charges_table[1]:
                self.esp_atoms.append(i)

            arthmetic("ESP charges", self.esp_atoms)

        # tworzenie listy z ladunkami NBO dla wybranych atomow
        if nbo_specific_atoms and nbo_specific_atoms[0].lower() != "all":

            for i in nbo_specific_atoms:
                for j in self.charges_table[2]:
                    if i == j.split()[1]:
                        self.nbo_atoms.append(j)

            arthmetic("NBO charges", self.nbo_atoms)

        elif nbo_specific_atoms and nbo_specific_atoms[0].lower() == "all":

            for i in self.charges_table[2]:
                self.nbo_atoms.append(i)

            arthmetic("NBO charges", self.nbo_atoms)

        return self.mulliken_atoms, self.esp_atoms, self.nbo_atoms

    @property
    def standard_orientation(self):

        xyz = []
        x = self.gen

        for i in x:
            if "Standard orientation" in i:

                _ = [next(x) for _ in range(4)]

                xyz = []
                for j in x:

                    if "-\n" in j:
                        break

                    xyz.append(j)
        return xyz

    def area(self, area1=False, area2=False, area3=False):

        sum_mulliken = 1
        sum_esp = 1
        sum_nbo = 1
        if self.mulliken_atoms:
            sum_mulliken = float(self.mulliken_atoms[-2].split(":")[1])
        elif area1 == True:
            spec_atoms = self.specific_atoms_charge(switcher1=True)
            sum_mulliken = float(spec_atoms[0][-2].split(":")[1])
        if self.esp_atoms:
            sum_esp = float(self.esp_atoms[-2].split(":")[1])
        elif area2 == True:
            spec_atoms = self.specific_atoms_charge(switcher2=True)
            sum_esp = float(spec_atoms[1][-2].split(":")[1])
        if self.nbo_atoms:
            sum_nbo = float(self.nbo_atoms[-2].split(":")[1])
        elif area3 == True:
            spec_atoms = self.specific_atoms_charge(switcher3=True)
            sum_nbo = float(spec_atoms[2][-2].split(":")[1])

        xyz = self.standard_orientation
        a1 = None
        a2 = None
        b1 = None
        b2 = None
        with open(self.path_to_atom_info, "r") as atom_spec:
            for line in atom_spec:
                if "a1 = " in line:
                    a1 = line.replace("a1 = ", "").replace("\n", "").replace(" ", "")
                if "b1 = " in line:
                    b1 = line.replace("b1 = ", "").replace("\n", "").replace(" ", "")
                if "a2 = " in line:
                    a2 = line.replace("a2 = ", "").replace("\n", "").replace(" ", "")
                if "b2 = " in line:
                    b2 = line.replace("b2 = ", "").replace("\n", "").replace(" ", "")

        for i in xyz:
            line = i.split()
            if a1 == line[0]:
                a1 = line[3:]
            if b1 == line[0]:
                b1 = line[3:]
            if a2 == line[0]:
                a2 = line[3:]
            if b2 == line[0]:
                b2 = line[3:]

        a1 = np.array(a1).astype(float)
        a2 = np.array(a2).astype(float)
        b1 = np.array(b1).astype(float)
        b2 = np.array(b2).astype(float)
        area = np.linalg.norm(np.subtract(a1, a2)) * np.linalg.norm(np.subtract(b1, b2))
        return area, sum_mulliken / area, sum_esp / area, sum_nbo / area


parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="+")
parser.add_argument("-all", action="store_true")
parser.add_argument("-area", action="store_true")
parser.add_argument("-esp", action="store_true")
parser.add_argument("-mulliken", action="store_true")
parser.add_argument("-nbo", action="store_true")

options = parser.parse_args()

start = time.time()
if options.all:

    fc = "Charges_Results"

    if not os.path.isdir(fc):
        os.mkdir(fc)

    for i in options.filename:
        dirname_ = os.path.dirname(i)
        path_ = os.path.join(dirname_, "atom_specification")

        if "/" in i:
            s = i.split("/")[-1]
            s = s.replace(".log", ".charge")

        else:
            s = i.replace(".log", ".charge")

        ins = Charge(i, path_)
        print(f"{s} is processing...")
        with open(os.path.join(fc, s), "w") as f:
            try:

                if options.mulliken:
                    x = ins.specific_atoms_charge(switcher1=True)
                    for line in x[0]:
                        f.write(str(line) + "\n")
                if options.esp:
                    x = ins.specific_atoms_charge(switcher2=True)
                    for line in x[1]:
                        f.write(str(line) + "\n")
                if options.nbo:
                    x = ins.specific_atoms_charge(switcher3=True)
                    for line in x[2]:
                        f.write(str(line) + "\n")

                if options.area:
                    area = ins.area(area1=False, area2=False, area3=False)
                    f.write("-" * 88)
                    f.write("\n")
                    f.write(f"Area = {area[0]}\n")
                elif options.area and options.mulliken and options.esp and options.nbo:
                    area = ins.area(area1=True, area2=True, area3=True)
                    f.write("-" * 88)
                    f.write("\n")
                    f.write(f"Area = {area[0]}\n")
                    f.write(f"Sum_Mulliken / A^2 = {area[1]}\n")
                    f.write(f"Sum_ESP / A^2 = {area[2]}\n")
                    f.write(f"Sum_NBO / A^2 = {area[3]}\n")
                elif options.area and options.mulliken:
                    area = ins.area(area1=True)
                    f.write("-" * 88)
                    f.write("\n")
                    f.write(f"Area = {area[0]}\n")
                    f.write(f"Sum_Mulliken / A^2 = {area[1]}\n")
                elif options.area and options.esp:
                    area = ins.area(area2=True)
                    f.write("-" * 88)
                    f.write("\n")
                    f.write(f"Area = {area[0]}\n")
                    f.write(f"Sum_ESP / A^2 = {area[2]}\n")
                elif options.area and options.nbo:
                    area = ins.area(area3=True)
                    f.write("-" * 88)
                    f.write("\n")
                    f.write(f"Area = {area[0]}\n")
                    f.write(f"Sum_NBO / A^2 = {area[3]}\n")
                elif options.area and options.mulliken and options.esp:
                    area = ins.area(area1=True, area2=True)
                    f.write("-" * 88)
                    f.write("\n")
                    f.write(f"Area = {area[0]}\n")
                    f.write(f"Sum_Mulliken / A^2 = {area[1]}\n")
                    f.write(f"Sum_ESP / A^2 = {area[2]}\n")
                elif options.area and options.mulliken and options.nbo:
                    area = ins.area(area1=True, area3=True)
                    f.write("-" * 88)
                    f.write("\n")
                    f.write(f"Area = {area[0]}\n")
                    f.write(f"Sum_Mulliken / A^2 = {area[1]}\n")
                    f.write(f"Sum_NBO / A^2 = {area[3]}\n")
                elif options.area and options.esp and options.nbo:
                    area = ins.area(area2=True, area3=True)
                    f.write("-" * 88)
                    f.write("\n")
                    f.write(f"Area = {area[0]}\n")
                    f.write(f"Sum_ESP / A^2 = {area[2]}\n")
                    f.write(f"Sum_NBO / A^2 = {area[3]}\n")

            except:
                print(
                    "Error - atom_specification not exist or problem with Gaussian log file!!!"
                )


else:
    try:
        fname = options.filename[0]
        # fname = sys.argv[1]
    except:
        print("Can't find an argument (Gaussian log file).")
    else:
        dirname_ = os.path.dirname(fname)
        path_ = os.path.join(dirname_, "atom_specification")
        ins = Charge(fname, path_)

        if options.mulliken:
            x = ins.specific_atoms_charge(switcher1=True)
            for i in x[0]:
                print(i)
        if options.esp:
            x = ins.specific_atoms_charge(switcher2=True)
            for i in x[1]:
                print(i)
        if options.nbo:
            x = ins.specific_atoms_charge(switcher3=True)
            for i in x[2]:
                print(i)

        if options.area:
            area = ins.area(area1=False, area2=False, area3=False)
            print("-" * 88)
            print(f"Area = {area[0]}")
        elif options.area and options.mulliken and options.esp and options.nbo:
            area = ins.area(area1=True, area2=True, area3=True)
            print("-" * 88)
            print(f"Area = {area[0]}")
            print(f"Sum_Mulliken / A^2 = {area[1]}")
            print(f"Sum_ESP / A^2 = {area[2]}")
            print(f"Sum_NBO / A^2 = {area[3]}")
        elif options.area and options.mulliken:
            area = ins.area(area1=True)
            print("-" * 88)
            print(f"Area = {area[0]}")
            print(f"Sum_Mulliken / A^2 = {area[1]}")
        elif options.area and options.esp:
            area = ins.area(area2=True)
            print("-" * 88)
            print(f"Area = {area[0]}")
            print(f"Sum_ESP / A^2 = {area[2]}")
        elif options.area and options.nbo:
            area = ins.area(area3=True)
            print("-" * 88)
            print(f"Area = {area[0]}")
            print(f"Sum_NBO / A^2 = {area[3]}")
        elif options.area and options.mulliken and options.esp:
            area = ins.area(area1=True, area2=True)
            print("-" * 88)
            print(f"Area = {area[0]}")
            print(f"Sum_Mulliken / A^2 = {area[1]}")
            print(f"Sum_ESP / A^2 = {area[2]}")
        elif options.area and options.mulliken and options.nbo:
            area = ins.area(area1=True, area3=True)
            print("-" * 88)
            print(f"Area = {area[0]}")
            print(f"Sum_Mulliken / A^2 = {area[1]}")
            print(f"Sum_NBO / A^2 = {area[3]}")
        elif options.area and options.esp and options.nbo:
            area = ins.area(area2=True, area3=True)
            print("-" * 88)
            print(f"Area = {area[0]}")
            print(f"Sum_ESP / A^2 = {area[2]}")
            print(f"Sum_NBO / A^2 = {area[3]}")

stop = time.time()
print(f"Process time = {stop - start}s")
