import numpy as np
import pandas as pd
from sklearn import metrics
import spearmonR as sprm


def predict(coNum, mult):

    typeTrue = []
    typePred = []
    for preTime in range(coNum):
        trainAll = []
        predictAll = []
        edgesByType = []
        p = 0
        for predictDataPre in data.predictDataFrames:
            predict = predictDataPre.sample(random_state=preTime, frac=1 / coNum, axis=1)
            train = predictDataPre.loc[:, ~predictDataPre.columns.isin(predict.columns)]
            predictAll.append(predict)

            trainPre = train.ix[data.remainIndex]  # dimensionality reduction
            trainPre = np.log(trainPre + 1)
            trainAll.append(trainPre)

            edgesPre = sprm.getSimilarByList(trainPre, p, data)  # get spearman
            edgesByType.append(edgesPre)
            p += 1

        # test by type
        for pre in range(data.typeNum):
            typeTruePre = []
            typePredPre = []
            for index, row in predictAll[pre].iteritems():  # predict each sample
                predictType = predictSmpling(edgesByType, trainAll, row, mult)
                typeTruePre.append(pre)
                typePredPre.append(predictType)
            typePred.extend(typePredPre)
            typeTrue.extend(typeTruePre)
    print(metrics.classification_report(typeTrue, typePred, digits=5))
    return


def predictSmpling(edgesByType, trainAll, sampleData, mult):
    # pretreat the sample
    sampleData = sampleData.ix[data.remainIndex]
    sampleData = np.log(sampleData + 1)
    preSimiList = []
    for preType in range(data.typeNum):
        # add the sample to each type
        newData = pd.concat([trainAll[preType], sampleData], axis=1)
        preSimiliar = sprm.getSimilarByList(newData, preType, data)

        # get delta
        deltaChange = abs((edgesByType[preType] - preSimiliar) * (newData.shape[1] ** mult))

        preSimi = deltaChange.sum().sum()
        preSimiList.append(preSimi)
    predictType = preSimiList.index(min(preSimiList))
    return predictType


def predictRun(dataCache, coNum, mult):
    global data
    data = dataCache
    print("5 test")
    predict(coNum=coNum, mult=mult)
