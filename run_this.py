import os
import sys

import preTreat as pt
import calculate as cclt
import predict as prdct
import readDataSet as rddt


def runAll(minNum, coNum, mult, remainNum, remainRatio, dataPath, cachePath):
    print("data:", dataPath)
    folder = os.path.exists(cachePath)
    if not folder:  # create directory
        os.makedirs(cachePath)

    dataCache = rddt.readDataRun(dataPath=dataPath)
    pt.preTreatRun(dataCache=dataCache, minNum=minNum, remainRatio=remainRatio, cachePath=cachePath)
    cclt.calculateRun(dataCache=dataCache, remainNum=remainNum, cachePath=cachePath)
    prdct.predictRun(dataCache=dataCache, coNum=coNum, mult=mult)


if __name__ == '__main__':

    preSet = [200, 0.7]

    for i in range(len(sys.argv) - 1):
        preSet[i] = sys.argv[i + 1]

    remainNum = int(preSet[0])
    remainRatio = float(preSet[1])

    testData = "BRCA_Subtypes"
    preName = os.path.basename(__file__).split(".")[0]
    cachePath = "./cache_" + testData + "_" + str(remainNum) + "/"

    # remainNum  each type remain edges
    # coNum      test by coNum-fold
    # mult       delta's power
    runAll(minNum=10,
           remainNum=remainNum,
           remainRatio=remainRatio,
           coNum=10,
           mult=0.66,
           dataPath=testData+'/',
           cachePath=cachePath)
