import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri

pandas2ri.activate()


def getSimilar(sampleDataFrame):
    # python's spearman is too slow to stand
    # the matrix is symmetric matrix, so remain its triangular matrix
    simiR = '''
    simi <- function(dataframe){
      data=cor(t(dataframe), method='spearman')
      data=data*lower.tri(data, diag = FALSE)
      return(data)
    }
    '''
    robjects.r(simiR)
    simi = robjects.r['simi'](sampleDataFrame)
    return simi


def getSimilarByList(sampleDataFrame, type, data):
    relationEdge = np.where(data.relateEdges == type)
    dataA = sampleDataFrame.iloc[relationEdge[0]].values
    dataB = sampleDataFrame.iloc[relationEdge[1]].values
    simiR = '''
    simi <- function(x,y){
     data=diag(cor(t(x),t(y), method='spearman'))
      return(data)
    }
    '''
    robjects.r(simiR)
    simi = robjects.r['simi'](dataA, dataB)

    return simi
