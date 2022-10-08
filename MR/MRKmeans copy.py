from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np


class MRKmeans(MRJob):
    def __init__(self, *args, **kwargs):
        super(MRKmeans, self).__init__(*args, **kwargs)
        self.ndim = 3
        self.nclass = 2

    def inputData(self, line):
        """feature1,...,feature 10, label"""
        # row = line.strip().split(',')
        row = line.split(',')
        # row = [float(e) for e in line.strip().split(",")]
        data_id = row[0]
        # data_id, cor= row[0], [row[1:4]]
        cor = [row[1:4]]
        return (data_id, np.array(cor, dtype=float).reshape(1, 3))

    # def inputData(self, line):
    #     # data = [str(e) for e in line.strip().split(" ")]
    #     # for data in line.split(','):
    #     #     data_id, cor= data[0], [data[1:4]]
    #     data = [float(e) for e in line.split(",")]
    #     # # data_id, cor = float(data[0]), [
    #     # #     data[1].split(":")[1],
    #     # #     data[2].split(":")[1],
    #     # #     data[3].split(":")[1],
    #     # # ]
    #     data_id, cor= data[0], [data[1:4]]
    #     return (data_id, np.array(cor, dtype=float).reshape(1, 3))

    def mapperKM(self,_, line):
        """
        data format: corr: shape is 1*3; centroid shape is 2*3
        output: eg: "2"     [2.0,[[0.2,0.2,0.2]]]
        """
        # print(type(line))
        row = line.split(',')
        # row = [float(e) for e in line.strip().split(",")]
        data_id = row[0]
        # data_id, cor= row[0], [row[1:4]]
        corr = np.array([row[1:4]], dtype=float).reshape(1, 3)
        # data_id, corr= row[0], np.array([row[1:4]], dtype=float).reshape(1, 3)
        # data_id, corr = self.inputData(line)
        global centroids
        centroids = np.random.rand(self.nclass, self.ndim) * 10

        dis = ((corr - centroids) ** 2).sum(axis=1)
        k_id = str(dis.argmin() + 1)
        yield k_id, (data_id, corr)

    def reducerKM(self, k_id, values):
        '''
        combine all values with same k_Id and calculate the mean as the next centroid
        but calculate directly only counts one node, so need to acumulate from each machine
        '''
        points = []
        corr_sum = np.zeros(self.ndim)
        for data_id, corr in values:
            corr = np.reshape(corr,self.ndim)
            # corr = np.array(corr,dtype=np.float)
            points.append(data_id)
            corr_sum += corr
    
        n_points = len(points)

        centroids = centroids[self.ndim*(int(k_id)+1):self.ndim*(int(k_id))]  / n_points
        yield None, centroids

    def steps(self):
        return [MRStep(
            mapper=self.mapperKM,
            reducer=self.reducerKM
        )]

if __name__ == '__main__':
    MRKmeans.run()

# corr = []
# with open("./sample_kmeans_data.txt", "r") as f:
#     for line in f:
#         data = line.strip().split(" ")
#         # print(data)
#         data_id, cor = float(data[0]), [
#             data[1].split(":")[1],
#             data[2].split(":")[1],
#             data[3].split(":")[1]
#         ]
#         # print(corr)
#         corr.append(cor)

# corr = np.array(corr,dtype=float)
# # print(corr)
# # generate random centroids
# ndim=3
# nclass = 2
# centroid = np.random.rand(nclass,ndim)*10
# # print(centroid)
# dis = np.linalg.norm((corr-centroid)).sum(axis=1)
# k_id = str(dis.argmin()+1)
# print(k_id,[data_id,[k_id]])
