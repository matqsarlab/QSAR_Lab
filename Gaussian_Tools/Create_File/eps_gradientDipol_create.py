#!/usr/bin/env python3.10


def reader(xyz, dipol, *args, **kwargs):
    # NOTE: create objects with coordinates for structures and dipol
    with open(xyz, "r") as c, open(dipol, "r") as d:
        xyz = c.readlines()
        dipol = d.readlines()

    concated = xyz + dipol
    if args:
        concated.append(*args)
    if kwargs:
        concated.insert(2, kwargs["checkpoint"])

    return concated


def saver(
    template: str, dipol: str, start: int, stop: int, step: int, name: str
) -> None:
    for i in range(start, stop, step):
        x = reader(
            template,
            dipol,
            f"EPS={i}\n\n",
            checkpoint=f"%chk={name}_{i}\n",
        )

        with open(f"{name}_{i}.com", "w") as f:
            f.writelines(x)


saver("./template", "./dipol_template", 50, 190, 20, "CNT_COO-_high")
