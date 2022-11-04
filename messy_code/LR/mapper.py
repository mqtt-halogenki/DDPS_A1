#!/usr/bin/env python3
"""mapper.py"""
import sys
import numpy as np


for line in sys.stdin:
    values = line.strip().split(",")

    dimension = len(values) - 1
    x_t_x, x_t_y = np.zero([dimension, dimension]), np.zeros(dimension)

    row = [float(e) for e in values]
    features, y = row[0:10], row[10]
    x = np.array(features)
    x_t_x += np.outer(x, x)
    x_t_y += y * x  # x_y
    print("%s\t%s" % ([list(row) for row in x_t_x], [xy for xy in x_t_y]))

sys.exit(0)
