import os
import sys

import preTreat as pt
import calculate as cclt
import predict as prdct
import readDataSet as rddt


class data():
    edges = []
    relateEdges = None
    predictDataFrames = []
    trainDataFrames = []
    typeNum = None
    remainIndex = None


def runAll(minNum, remainNum, remainRatio, dataPath, cachePath):
    print()
    print("data:", dataPath)
    print("cache:", cachePath)
    folder = os.path.exists(cachePath)
    if not folder:  # create directory
        os.makedirs(cachePath)

    rddt.readDataRun(dataCache=data, dataPath=dataPath)
    pt.preTreatRun(dataCache=data, minNum=minNum, remainRatio=remainRatio, cachePath=cachePath)
    cclt.calculateRun(dataCache=data, remainNum=remainNum, cachePath=cachePath)
    prdct.predictRun(dataCache=data, coNum=10)  # coNum      test by coNum-fold


if __name__ == '__main__':
    preSet = ['LUSC_Stages', 0.8, 100, 10]
    # preSet = ['KIRC_Grades', 0.8, 100, 10]
    # preSet = ['BRCA_Subtypes', 0.7, 100, 10]

    runAll(
        remainRatio=float(preSet[1]),
        remainNum=int(preSet[2]),  # each type remain edges' count
        minNum=int(preSet[3]),  # pretreat remain data larger than
        dataPath=preSet[0] + '/',
        cachePath="./cache/cache_" + str(preSet[0]) + "_" + str(preSet[1]) + "/")
