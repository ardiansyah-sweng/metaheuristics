import sys
from data_processor import DataProcessor
from objective_function import CocomoEstimator
from gwo_origin import GreyWolfOptimizer
from gwo_li2021 import IGreyWolfOptimizerLi2021
from gwo_yang2023 import CGreyWolfOptimizerYang2023
from gwo_nadimi2021 import IGWONadimi2021
from gwo_ibrahim2018 import GreyWolfOptimizerIbrahim2018
from standard_pso import ParticleSwarmOptimizer
from performevaluation.SAES import SAES
import numpy as np

def calcAverage(bestSolutions):
    return sum(bestSolutions) / len(bestSolutions)

def writeResultToFile(fileName, resultType, dataToWrite):
    folder_path = "/metaheuristics/"
    file_path = folder_path + fileName
    with open(file_path, "a") as file:
        file.write(resultType + "\n")
        for item in dataToWrite:
            file.write(str(item) + "\n")
        file.write("======================" + "\n")

cocomoCode = 0
datasetNames = ['nasa10.txt', 'cocomo_nasa93.txt', 'cocomo81.txt', 'cocomo_nasa60.txt']
ranges = [
    [[0, 10], [0.3, 2]],
    [[0, 10], [0.3, 2]],
    [[0, 10], [1.05, 1.20]]
]

fileName = datasetNames[cocomoCode]
dataset = DataProcessor.processingData(fileName, cocomoCode)
variableRanges = ranges[cocomoCode]

cocomo = CocomoEstimator(cocomoCode)
#gwo = GreyWolfOptimizer(variableRanges, cocomo)
#gwo = IGreyWolfOptimizerLi2021(variableRanges, cocomo)
#gwo = CGreyWolfOptimizerYang2023(variableRanges, cocomo) #CGWO
#gwo = GreyWolfOptimizerIbrahim2018(variableRanges, cocomo) #COGWO2D
gwo = IGWONadimi2021(variableRanges, cocomo) #CUGWO
#pso = ParticleSwarmOptimizer(variableRanges, cocomo)


bestSolutions = []
numOfRuns = 30
bestOfRunSolutions = []

maes = []
convergences = []
avgBestconvergences = []

for _ in range(numOfRuns):
    actualEfforts = []
    
    for i in range(len(dataset)):
        if i == 3:
        #khusus cocomo tanpa optimasi
        # estimatedEffort = cocomo.estimatingEffort(dataset[i])
        # print(estimatedEffort)
        # ae = abs(dataset[i]['actualEffort'] - estimatedEffort)
        # bestSolutions.append(ae)
        
            bestSolution = gwo.runGWO(variableRanges, cocomo, dataset[i]); sys.exit()
        #bestSolution = pso.runPSO(dataset[i])
        #bestSolutions.append(bestSolution['bestWolf']['absError'])
        #bestSolutions.append(bestSolution['absError'])

        #actualEfforts.append(dataset[i]['actualEffort'])
        #convergences.append(bestSolution['bestConvergences'])
    mae = calcAverage(bestSolutions)
    # print('mae',mae)
    # print(convergences)
    # sys.exit()

    # for convergence in convergences:
    #     bestWolves = []
    #     for bestWolf in convergence:
    #         bestWolves.append(bestWolf)
    #     avgBestconvergence = sum(bestWolves) / len(bestWolves)
    #     avgBestconvergences.append(avgBestconvergence)
    
    # print(bestSolutions)
    #mae = calcAverage(bestSolutions)
    #maes.append(mae)
    
    # saes = SAES(mae, actualEfforts).calcSAES()
    # print(saes, 'mae',mae)

    # print('stdev',np.std(bestSolutions))
    # sys.exit()

    #print(mae)
#     bestOfRunSolutions.append(mae)

# algo = "CGWO Yang2023 COCOMO81"
# writeResultToFile("results_gwo.txt", algo, bestOfRunSolutions, )
# print('mean '+ algo, sum(bestOfRunSolutions)/numOfRuns)
