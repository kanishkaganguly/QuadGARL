import inspect
import math

import numpy as np


def rotation_matrix(angles):
    ct = math.cos(angles[0])
    cp = math.cos(angles[1])
    cg = math.cos(angles[2])
    st = math.sin(angles[0])
    sp = math.sin(angles[1])
    sg = math.sin(angles[2])
    R_x = np.array([[1, 0, 0], [0, ct, -st], [0, st, ct]])
    R_y = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
    R_z = np.array([[cg, -sg, 0], [sg, cg, 0], [0, 0, 1]])
    R = np.dot(R_z, np.dot(R_y, R_x))
    return R


def wrap_angle(val):
    return (val + np.pi) % (2 * np.pi) - np.pi


def quad_logger(log_data: str):
    frame_records = inspect.stack()[1]
    calling_module = inspect.getmodulename(frame_records[1])

    if log_data is not None:
        print("[{}::{}] {}".format(calling_module, inspect.stack()[1][3], log_data))
    else:
        print('\n')
