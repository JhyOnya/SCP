import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def cutOffByMin(minNum):
    remainIndexs = None
    for i in range(data.typeNum):
        meanFt = data.trainDataFrames[i].mean(1)  # get mean
        remainIndex = meanFt[meanFt > minNum].index
        if remainIndexs is None:
            remainIndexs = remainIndex
        else:
            remainIndexs = remainIndexs & remainIndex
    for i in range(data.typeNum):
        data.trainDataFrames[i] = data.trainDataFrames[i].loc[remainIndexs]
    print(data.trainDataFrames[0].shape)
    return


def cutOffByMeanLog(remainRatio, cachePath):
    remainIndexs = None
    for i in range(data.typeNum):
        meanPre = data.trainDataFrames[i].mean(1)  # mean
        varPre = data.trainDataFrames[i].std(1) / meanPre  # std
        # draw
        varPre.plot(kind="kde", xlim=[0, 2])

        # all the features >remainRatio
        remainIndex = varPre[varPre < remainRatio].index
        if (remainIndexs is None):
            remainIndexs = remainIndex
        else:
            remainIndexs = remainIndexs & remainIndex
    plt.savefig(cachePath + "picDataDistribute.png", dpi=600)

    for i in range(data.typeNum):
        data.trainDataFrames[i] = data.trainDataFrames[i].loc[remainIndexs]
    print(data.trainDataFrames[0].shape)
    return


def toLog():
    for i in range(data.typeNum):
        data.trainDataFrames[i] = np.log(data.trainDataFrames[i] + 1)  # log(x+1)
    return


def preTreatRun(dataCache, minNum, remainRatio, cachePath):
    global data
    data = dataCache
    print("\n1_1 pretreat min by", minNum)
    cutOffByMin(minNum=minNum)

    print("1_2 remain std by", remainRatio)
    cutOffByMeanLog(remainRatio=remainRatio, cachePath=cachePath)

    print("1_3 pretreat std as log")
    toLog()
    return data
