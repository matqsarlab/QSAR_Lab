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


def saver(template: str, start: int, stop: int, step: int, name: str) -> None:
    for i in range(start, stop, step):
        x = reader(
            template,
            f"EPS={i}\n\n",
            checkpoint=f"%chk=CNT_COO-_high_dipole{(i)}\n",
        )

        with open(f"{name}_{(i)}.com", "w") as f:
            f.writelines(x)


saver("./template", 50, 190, 10, "CNT_COO-_high_dipole")
