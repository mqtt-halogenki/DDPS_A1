#!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep
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


##########################Mapreduce jon ################


class LR(MRJob):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        # n = self._passthru_arg_dests.get('--dimension')
        # n = self.options._get_args()
        # n = self.options.dimension
        n=self.options.dimension
        self.x_t_x = np.zeros([n, n])
        self.x_t_y = np.zeros(n)
        self.counts = 0

    # ---------------------------preprocess data --------------------------------#

    def inputData(self, line):
        """feature1,...,feature 10, label"""
        # row = line.strip().split(',')
        row = [float(e) for e in line.strip().split(",")]
        features, y = row[0:10], row[10]
        # print(features)
        return (y, features)

    # -------------------------------------------options -------------------#
    def configure_args(self):
        super().configure_args()
        self.add_passthru_arg("--dimension", type=int, help="numer of dimentions of fratures")

    def mapper_lr(self, _, line):
        """
        Calculates x_t_x and x_t_y for data processed by each mapper
        """
        y, features = self.inputData(line)
        x = np.array(features)
        self.x_t_x += np.outer(x, x)
        self.x_t_y += y * x
        self.counts += 1

    def mapper_lr_final(self):
        """
        Transforms numpy arrays x_t_x and x_t_y into json-encodable list format
        and sends to reducer
        """
        yield 1, ("x_t_x", [list(row) for row in self.x_t_x])
        yield 1, ("x_t_y", [xy for xy in self.x_t_y])
        yield 1, ("counts", self.counts)

    def reducer_lr(self, key, values):
        """
        Aggregates results produced by each mapper and obtains x_t_x and x_t_y
        for all data, then using cholesky decomposition obtains parameters of
        linear regression.
        """
        n = self.options.dimension
        observations = 0
        x_t_x = np.zeros([n, n])
        x_t_y = np.zeros(n)
        for val in values:
            if val[0] == "x_t_x":
                x_t_x += np.array(val[1])
            elif val[0] == "x_t_y":
                x_t_y += np.array(val[1])
            elif val[0] == "counts":
                observations += val[1]
        betas = cholesky_solution_linear_regression(x_t_x, x_t_y)
        yield None, [e for e in betas]

    def steps(self):
        """Defines map-reduce steps"""
        return [
            MRStep(
                mapper=self.mapper_lr,
                mapper_final=self.mapper_lr_final,
                reducer=self.reducer_lr,
            )
        ]


if __name__ == "__main__":
    LR.run()
