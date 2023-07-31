import numpy as np


def ellipse(xy: tuple, a, b, rotate_angle):
    theta = np.arange(0, 2 * np.pi, 0.01)

    xpos = a * np.cos(theta) + xy[0]
    ypos = b * np.sin(theta + xy[1])

    rotate_angle = 90

    new_xpos = xpos * np.cos(np.deg2rad(rotate_angle)) + ypos * np.sin(
        np.deg2rad(rotate_angle)
    )
    new_ypos = -xpos * np.sin(np.deg2rad(rotate_angle)) + ypos * np.cos(
        np.deg2rad(rotate_angle)
    )
    return new_xpos, new_ypos
