#!/usr/bin/env python3

import argparse
import os

import numpy as np

# from QSAR_Lab.Gaussian_Tools import final_coord


class Charge:
    def __init__(self, filename) -> None:
        self.filename = filename

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

                if "Sum of" in j:
                    break

                charges_list.append(j)
            return charges_list

        mulliken_ = []
        esp_ = []

        for i in x:

            if "Mulliken charges:" in i:
                mulliken_ = selector()
            if "ESP charges:" in i:
                esp_ = selector()

        return mulliken_, esp_

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

        return mulliken_, esp_

    @property
    def specific_atoms_charge(self):

        mulliken_atoms = []
        esp_atoms = []

        mulliken_specific_atoms = []
        esp_specific_atoms = []

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
        with open("./atom_specification", "r") as atom_spec:

            for line in atom_spec:

                if "mulliken" in line.lower():
                    mulliken_specific_atoms = spec_number(mulliken_specific_atoms)

                if "esp" in line.lower():
                    esp_specific_atoms = spec_number(esp_specific_atoms)

        # tworzenie listy z ladunkami mullikena dla wybranych atomow
        if mulliken_specific_atoms and mulliken_specific_atoms[0].lower() != "all":

            for i in mulliken_specific_atoms:
                for j in self.charges_table[0]:
                    if i == j.split()[0]:
                        mulliken_atoms.append(j)

            arthmetic("Mulliken charges", mulliken_atoms)

        elif mulliken_specific_atoms[0].lower() == "all":

            for i in self.charges_table[0]:
                mulliken_atoms.append(i)

            arthmetic("Mulliken charges", mulliken_atoms)

        # tworzenie listy z ladunkami ESP dla wybranych atomow
        if esp_specific_atoms and esp_specific_atoms[0].lower() != "all":

            for i in esp_specific_atoms:
                for j in self.charges_table[1]:
                    if i == j.split()[0]:
                        esp_atoms.append(j)

            arthmetic("ESP charges", esp_atoms)

        elif esp_specific_atoms[0].lower() == "all":

            for i in self.charges_table[1]:
                esp_atoms.append(i)

            arthmetic("ESP charges", esp_atoms)

        return mulliken_atoms, esp_atoms

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

    @property
    def area(self):

        spec_atoms = self.specific_atoms_charge
        sum_mulliken = float(spec_atoms[0][-2].split(":")[1])
        sum_esp = float(spec_atoms[1][-2].split(":")[1])

        xyz = self.standard_orientation
        a = None
        b = None
        r0 = None
        with open("./atom_specification", "r") as atom_spec:
            for line in atom_spec:
                if "a = " in line:
                    a = line.replace("a = ", "").replace("\n", "").replace(" ", "")
                if "b = " in line:
                    b = line.replace("b = ", "").replace("\n", "").replace(" ", "")
                if "r0 = " in line:
                    r0 = line.replace("r0 = ", "").replace("\n", "").replace(" ", "")

        for i in xyz:
            line = i.split()
            if a == line[0]:
                a = line[3:]
            if b == line[0]:
                b = line[3:]
            if r0 == line[0]:
                r0 = line[3:]

        a = np.array(a).astype(float)
        b = np.array(b).astype(float)
        r0 = np.array(r0).astype(float)
        area = np.linalg.norm(np.subtract(a, r0)) * np.linalg.norm(np.subtract(b, r0))
        return area, sum_mulliken / area, sum_esp / area


parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="+")
parser.add_argument("-all", action="store_true")
parser.add_argument("-area", action="store_true")
parser.add_argument("-esp", action="store_true")
parser.add_argument("-mulliken", action="store_true")

options = parser.parse_args()

if options.all:

    fc = "Charges_Results"

    if not os.path.isdir(fc):
        os.mkdir(fc)

    for i in options.filename:
        ins = Charge(i)

        if "/" in i:
            s = i.split("/")[-1]
            s = s.replace(".log", ".charge")

        else:
            s = i.replace(".log", ".charge")

        print(f"{s} is processing...")
        with open(os.path.join(fc, s), "w") as f:
            if options.esp or options.mulliken:
                x = ins.specific_atoms_charge

                if options.mulliken:
                    for line in x[0]:
                        f.write(str(line) + "\n")
                if options.esp:
                    for line in x[1]:
                        f.write(str(line) + "\n")
            if options.area:
                area = ins.area
                f.write("-" * 88)
                f.write("\n")
                f.write(f"Area = {area[0]}\n")
                f.write(f"Sum_Mulliken / A^2 = {area[1]}\n")
                f.write(f"Sum_ESP / A^2 = {area[2]}\n")
            pass

else:
    try:
        fname = options.filename[0]
        # fname = sys.argv[1]
    except:
        print("Can't find an argument (Gaussian log file).")
    else:
        ins = Charge(fname)
        # x = ins.specific_atoms_charge()
        if options.esp or options.mulliken:
            x = ins.specific_atoms_charge

            if options.mulliken:
                for i in x[0]:
                    print(i)
            if options.esp:
                for i in x[1]:
                    print(i)

        if options.area:
            area = ins.area
            print("-" * 88)
            print(f"Area = {area[0]}")
            print(f"Sum_Mulliken / A^2 = {area[1]}")
            print(f"Sum_ESP / A^2 = {area[2]}")

        # for i in x:
        #     print(i)

        # for i in x:
        #     print(i)
