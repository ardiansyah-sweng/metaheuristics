import sys
import os
import glob
import numpy as np

def readSilhavy71():
    """
    Output: \n
    [[6.0, 10.0, 15.0, 9.0, 0.81, 0.84, 7970.0], \n
    [4.0, 20.0, 15.0, 8.0, 0.99, 0.99, 7962.0],..., \n
    [5.0, 18.0, 17.0, 18.0, 0.85, 0.89, 5775.0]]
    """
    ### TODO move hard .TXT filename into conf/setup filed
    with open("ucp_silhavy.txt", "r") as myfile:
        numCols = 8 ### TODO move variable into conf/setup file
        numDataPoint = 71 ### TODO move variable into conf/setup file
        datasetInString = myfile.read().replace("\n",",")
        datasetInList = datasetInString.split(",")  
        oneDataPoints, dataSet = [], []
        startIndex = 0

        for _ in range(numDataPoint):
            for _ in range(numCols):
                oneDataPoints.append(float(datasetInList[startIndex]))
                startIndex += 1
            dataSet.append(oneDataPoints)
            oneDataPoints = []
    return dataSet

def readUCPSeeds():
    folderPath = "ucp"
    exstension = "*.txt"
    txtFiles = glob.glob(os.path.join(folderPath, exstension))
    dataSeeds = []
    for str, txtFile in enumerate(txtFiles):
        with open(txtFile, 'r') as myfile:            
            numCols = 3 ### TODO move variable into conf/setup file
            numDataPoint = 30 ### TODO move variable into conf/setup file
            datasetInString = myfile.read().replace("\n",",")
            datasetInList = datasetInString.split(",") 
            oneDataPoints, dataSet = [], []
            startIndex = 0
            for _ in range(numDataPoint):
                for _ in range(numCols):
                    oneDataPoints.append(float(datasetInList[startIndex]))
                    startIndex += 1
                dataSet.append(oneDataPoints)
                oneDataPoints = []
        dataSeeds.append(dataSet)
        dataSet = []
    return dataSeeds

def getActualEfforts():
    rets = []; dataset = readSilhavy71()
    for tuple in dataset:
        rets.append(tuple[6])
    return rets

def getKarnerMAE():
    aes = []
    karnerEstimateds = [
        4953.312, 8879.706, 5998.72, 5864.04, 5782.14, 6919.506, 8188.152, 5735.04,
        6577.368, 8477.98, 4922.736, 5113.94, 5066.55, 9119.208, 6928.065, 4779.216,
        4945.05, 5784.8855, 4635.696, 6443.85, 4115.302, 8897.868, 5323.04, 4546.308,
        4794.036, 7281.596, 2522.052, 5189.184, 7720.65, 4644.91, 6795.138, 5106.024,
        5695.272, 6310.28, 3598.608, 5714.448, 6108.12, 3026.872, 5913.18, 6058.944, 
        2283.372, 4729.76, 6458.4, 7198.53, 3426.3, 8553.12, 4997.664, 7837.34, 4021.734,
        7524.88, 13193.1826, 7674.48, 6172.2, 6912.864, 7686.04, 8856.32, 5057.192, 7519.61,
        8365.896, 3193.488, 6516.868, 6193.152, 5083.68, 10464.915, 7256.607, 9467.976, 9536.1,
        9591.36, 8635.12, 4710.4, 7232.14]
    for i in range(len(karnerEstimateds)):
        aes.append(abs(getActualEfforts()[i] - karnerEstimateds[i]))
    return {
        'mae':sum(aes) / len(karnerEstimateds),
        'stdev': np.std(aes)
    }