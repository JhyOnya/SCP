import numpy as np
import pandas as pd

import spearmonR as sprm


# 2 get all similarity matrix
def trainByType():
    for trainDataFrame in data.trainDataFrames:
        scc = sprm.getSimilar(trainDataFrame)
        sccDF = pd.DataFrame(scc, index=trainDataFrame.index, columns=trainDataFrame.index)
        data.edges.append(sccDF)
    print(data.trainDataFrames[0].shape)


def findMax(remainNum):
    maxData = None
    maxLocate = None
    secondData = None
    secondLocate = None
    # most large
    for i in range(data.typeNum):
        edgesPre = data.edges[i].values
        if maxData is None:
            maxData = data.edges[i].values
            maxLocate = np.zeros(maxData.shape)
            secondData = maxLocate.copy()
            secondLocate = maxLocate.copy()
        else:
            maxLocate = np.where(abs(edgesPre) < abs(maxData), maxLocate, i)
            maxData = np.where(maxLocate == i, edgesPre, maxData)
    # second large
    for i in range(data.typeNum):
        edgesPre = data.edges[i].values
        secondLocate = np.where(
            ((abs(edgesPre) < abs(secondData)) | (abs(edgesPre) == abs(maxData))), secondLocate, i)
        if i == 0:
            secondData = np.where(((secondLocate == i) & (maxLocate != i)), edgesPre, secondData)
        else:
            secondData = np.where(secondLocate == i, edgesPre, secondData)
    # calculate delta and sort it
    deltaMax = abs(maxData) - abs(secondData)
    deltaMaxSortList = []
    relateEdgesPre = np.ones(deltaMax.shape) * -1
    for i in range(data.typeNum):
        deltaMaxByType = np.where(maxLocate == i, deltaMax, 0)
        numSort = np.sort(deltaMaxByType, axis=None)
        remainMin = numSort[-remainNum]
        deltaMaxSortList.append(remainMin)
        relateEdgesPre = np.where(((maxLocate == i) & (deltaMax >= remainMin)), maxLocate, relateEdgesPre)

    data.relateEdges = pd.DataFrame(relateEdgesPre)
    data.relateEdges.index = data.edges[0].index
    data.relateEdges.columns = data.edges[0].columns
    data.relateEdges = data.relateEdges[data.relateEdges != -1]
    print("  delta remain top", remainNum, "is larger than", deltaMaxSortList)


def delEgdes():
    nanIndex = data.relateEdges[data.relateEdges.isnull().T.all()].index
    nanCol = data.relateEdges[data.relateEdges.isnull().all()].index
    data.relateEdges = data.relateEdges.drop(index=(nanIndex & nanCol))
    data.relateEdges = data.relateEdges.drop(columns=(nanIndex & nanCol))
    data.remainIndex = data.relateEdges.index
    data.relateEdges = data.relateEdges.values

    for i in range(data.typeNum):
        data.edges[i] = data.edges[i].loc[data.remainIndex, data.remainIndex].values
        data.trainDataFrames[i] = data.trainDataFrames[i].loc[data.remainIndex]
    print("the relation network's shape", data.relateEdges.shape)


def outRelations(dataSave):
    relationEdge = np.where(~np.isnan(data.relateEdges))
    indexs = data.remainIndex
    relationEdgesA = indexs[relationEdge[0].tolist()]
    relationEdgesB = indexs[relationEdge[1].tolist()]

    datas = []
    group = np.ones(len(relationEdgesA))
    group = group * data.typeNum
    for i in range(data.typeNum):
        dataPre = []
        for a, b, j in zip(relationEdge[0], relationEdge[1], range(len(relationEdgesA))):
            dataPre.append(data.edges[i][a][b])
            group[j] = data.relateEdges[a][b]
        datas.append(data)

    # output the file
    edges = pd.DataFrame({"type": group,
                          "edgesA": relationEdgesA,
                          "edgesB": relationEdgesB, }, )
    for i in range(data.typeNum):
        edges[str(i)] = datas[i]

    edges.to_csv(dataSave + "topEdges.csv")
    print("  output the last remain edges to the file topEdges.csv")


def calculateRun(dataCache, remainNum, cachePath):
    global data
    data = dataCache
    print("2 calculate the similarity matrix")
    trainByType()

    print("3 find", remainNum, "most difference feature pairs")
    findMax(remainNum)

    print("4 delete edges")
    delEgdes()

    outRelations(cachePath)
    return data
