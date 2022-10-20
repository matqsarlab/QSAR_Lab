#!/usr/bin/env python3.10


def reader(xyz, *args, **kwargs):
    # NOTE: create objects with coordinates for structures and dipol
    with open(xyz, "r") as c:
        xyz = c.readlines()

    if args:
        xyz.append(*args)
    if kwargs:
        xyz.insert(2, kwargs["checkpoint"])

    return xyz


def saver(template: str, number: int, name: str) -> None:
    for i in range(number):
        x = reader(
            template,
            f"EPS={(i+1)*5}\n\n",
            checkpoint=f"%chk=CNT_COO-_high_dipole{(i+1)*5}\n",
        )

        with open(f"{name}_{(i+1)*5}.com", "w") as f:
            f.writelines(x)


saver("./template", 15, "CNT_COO-_high_dipole")
