import pandas as pd


def readFile(path):
    index = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            index.append(line.strip())
    return index


result = pd.DataFrame(columns=['feature', 'Score', 'Related Feature1', 'Related Feature2', 'Related Feature3', 'Related Feature4', 'Related Feature5'])

preText = readFile("../Lasso/outputLasso500")

remainNum=None
eachAcc=None
AccAll=None
for preLine in preText:
    if preLine.startswith("|"):
        if preLine.startswith("| Order"):
            continue
        preMsg=preLine.split('|')
        preNum=preMsg[1].strip()
        feature=preMsg[2].strip()
        score=preMsg[4].strip()
        top=[]
        top.append(preMsg[5])
        top.append(preMsg[6].split(',')[-1])
        top.append(preMsg[7].split(',')[-1])
        top.append(preMsg[8].split(',')[-1])
        top.append(preMsg[9].split(',')[-1])
        result.loc[preNum] = [feature, score, top[0],top[1],top[2],top[3],top[4]]

result=result.sort_values("Score",ascending=False)
result.to_csv("resultLasso.csv", encoding="utf_8_sig")
