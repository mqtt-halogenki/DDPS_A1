#!/usr/bin/env python3
"""reducer.py"""
import sys
import numpy as np


def cholesky_solution_linear_regression(x_t_x, x_t_y):
    """
    Finds parameters of regression through Cholesky decomposition,
    given sample covariance of explanatory variables and covariance
    between explanatory variable and dependent variable.

    Paramaters:
    -----------
    x_t_x    - numpy array of size 'm x m', represents sample covariance of explanatory variables
    x_t_y    - numpy array of size 'm x 1', represent covariance between expalanatory and dependent variable

    Output:
    -------
    Theta   - list of size m, represents values of coefficients

    """
    # L*L.T*Theta = x_t_y
    L = np.linalg.cholesky(x_t_x)
    #  solve L*z = x_t_y
    z = np.linalg.solve(L, x_t_y)
    #  solve L.T*Theta = z
    theta = np.linalg.solve(np.transpose(L), z)
    return theta


for line in sys.stdin:
    line_value = line.strip().split(",")
    dimentsion = len(line_value[1])

    x_t_x, x_t_y = np.zero([dimentsion, dimentsion]), np.zeros(dimentsion)

    try:
        x_t_x += np.array(line_value[1])
        x_t_y += np.array(line_value[0])
    except ValueError:
        continue

    betas = cholesky_solution_linear_regression(x_t_x, x_t_y)
    print("%s\t%s" % ([e for e in betas]))
