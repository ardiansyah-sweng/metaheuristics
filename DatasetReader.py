import sys

def readSilhavy71():
    ### TODO move hard .TXT filename into conf/setup filed
    with open("ucp_silhavy.txt", "r") as myfile:
        numCols = 7 ### TODO move variable into conf/setup file
        numDataPoint = 71 ### TODO move variable into conf/setup file
        datasetInString = myfile.read().replace("\n",",")
        datasetInList = datasetInString.split(",")    
        oneDataPoints, dataSet = [], []
        startIndex = 0

        for i in range(numDataPoint):   ## TODO find out why i,j unused?
            for j in range(numCols):
                oneDataPoints.append(float(datasetInList[startIndex]))
                startIndex += 1
            dataSet.append(oneDataPoints)
            oneDataPoints = []
    return dataSet