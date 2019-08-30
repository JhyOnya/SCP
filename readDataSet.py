import pandas as pd
import os


def createDataSet(path):
    dataList = []
    for maindir, subdir, file_name_list in os.walk(path):
        for filename in file_name_list:
            if not str(filename).endswith('.txt'):
                continue
            apath = os.path.join(maindir, filename)
            dataList.append(apath)
    dataList.sort()
    for apath in dataList:
        print(' ' + apath)
        readFile(apath)

    # change index
    index = []
    with open(path + "gene_symbol_list_exceptSLC35E2", 'r') as f:
        lines = f.readlines()
        for line in lines:
            index.append(line.strip())
    data.typeNum = len(data.trainDataFrames)
    for i in range(data.typeNum):
        data.trainDataFrames[i].index = index
        data.predictDataFrames[i].index = index


def readFile(path):
    dataSet = pd.read_table(path)
    data.trainDataFrames.append(dataSet)
    data.predictDataFrames.append(dataSet.copy())
    return


def readDataRun(dataCache, dataPath):
    global data
    data = dataCache
    print("\n0 read data")
    createDataSet(dataPath)
    return
