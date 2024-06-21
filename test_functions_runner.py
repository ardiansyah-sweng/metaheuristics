from firefly_test_function import FireflyOptimizer
from particle_swarm_optimizer_test_function import ParticleSwarmOptimizer
from genetic_algorithm_test_functions import GeneticAlgorithm
from grey_wolf_optimizer_test_function import GreyWolfOptimizer
from reptile_search_algorithm_test_function import ReptileSearchAlgorithm
from helper import MetaheuristicHelper as metaHelper
from optimizers import getOptimizerParameter
from test_functions import getTestFunctionParameters
import sys, random
import numpy as np

class OptimizersInterface:
    def optimizer(self):
        pass

class FAExecutor(OptimizersInterface):
    def optimizer(self, optimizerParameters, testFunctionParameter, testFunctionID):
        initialPopulation = []
        runInitialPop = metaHelper(
            testFunctionParameter['ranges'],
            None,
            None,
            optimizerParameters['maxIter'],
            testFunctionParameter['dimension']
        )
        initialPopulation = runInitialPop.generateTestFunctionInitialPopulation(optimizerParameters['populationSize'], testFunctionID)
        optimizer = FireflyOptimizer(
            optimizerParameters,
            testFunctionParameter,
            testFunctionID
        )
        return optimizer.runFirefly(initialPopulation)

class GAExecutor(OptimizersInterface):
    def optimizer(self, optimizerParameters, testFunctionParameter, testFunctionID):
        initialPopulation = []
        runInitialPop = metaHelper(
            testFunctionParameter['ranges'],
            None,
            None,
            optimizerParameters['maxIter'],
            testFunctionParameter['dimension']
        )
        initialPopulation = runInitialPop.generateTestFunctionInitialPopulation(optimizerParameters['populationSize'], testFunctionID)
        optimizer = GeneticAlgorithm(
            optimizerParameters,
            testFunctionParameter,
            testFunctionID
        )
        return optimizer.runGA(initialPopulation)

class RSAExecutor(OptimizersInterface):
    def optimizer(self, optimizerParameters, testFunctionParameter, testFunctionID):
        initialPopulation = []
        runInitialPop = metaHelper(
            testFunctionParameter['ranges'],
            None,
            None,
            optimizerParameters['maxIter'],
            testFunctionParameter['dimension']
        )
        initialPopulation = runInitialPop.generateTestFunctionInitialPopulation(optimizerParameters['populationSize'], testFunctionID)
        optimizer = ReptileSearchAlgorithm(
            optimizerParameters,
            testFunctionParameter,
            testFunctionID
        )
        return optimizer.runRSA(initialPopulation)

class PSOExecutor(OptimizersInterface):
    def createInitialVelocities(self, positions):
        rets = []
        for positionValue in positions:
            rets.append(positionValue * random.uniform(0,1))
        return rets
    
    def optimizer(self, optimizerParameters, testFunctionParameter, testFunctionID):
        initialPopulation = []
        runInitialPop = metaHelper(
            testFunctionParameter['ranges'],
            None,
            None,
            optimizerParameters['maxIter'],
            testFunctionParameter['dimension']
        )
        initialPopulation = runInitialPop.generateTestFunctionInitialPopulation(optimizerParameters['populationSize'], testFunctionID)
        for i in range(len(initialPopulation)):
            velocities = self.createInitialVelocities(initialPopulation[i]['positions'])
            initialPopulation[i]['velocities'] = velocities
        optimizer = ParticleSwarmOptimizer(
            optimizerParameters,
            testFunctionParameter,
            testFunctionID
        )
        return optimizer.runPSO(initialPopulation, optimizerParameters['maxIter'])

class GWOExecutor(OptimizersInterface):
    def optimizer(self, optimizerParameters, testFunctionParameter, testFunctionID):
        initialPopulation = []
        runInitialPop = metaHelper(
            testFunctionParameter['ranges'],
            None,
            None,
            optimizerParameters['maxIter'],
            testFunctionParameter['dimension']
        )
        initialPopulation = runInitialPop.generateTestFunctionInitialPopulation(optimizerParameters['populationSize'], testFunctionID)
        optimizer = GreyWolfOptimizer(
            optimizerParameters,
            testFunctionParameter,
            testFunctionID
        )
        return optimizer.runGWO(initialPopulation)

class OptimizationExecutorFactory:
    def initializingOptimizationExecutor(optimizerID, optimizerParameters, testFunctionParameter, testFunctionID):
        optimizers = [
            # {'optimizer': 'fa', 'select':FAExecutor().optimizer(optimizerParameters, testFunctionParameter, testFunctionID)},
            # {'optimizer': 'ga', 'select':GAExecutor().optimizer(optimizerParameters, testFunctionParameter, testFunctionID)},
            {'optimizer': 'gwo', 'select':GWOExecutor().optimizer(optimizerParameters, testFunctionParameter, testFunctionID)},
            #{'optimizer': 'pso', 'select':PSOExecutor().optimizer(optimizerParameters, testFunctionParameter, testFunctionID)},
            # {'optimizer': 'rsa', 'select':RSAExecutor().optimizer(optimizerParameters, testFunctionParameter, testFunctionID)}
        ]
        index = next((i for i, item in enumerate(optimizers) if item["optimizer"] == optimizerID), None)
        return optimizers[index]['select']

def writeResultToFile(fileName, resultType, dataToWrite):
    folder_path = "/metaheuristics/performevaluation/results/"
    file_path = folder_path + fileName
    with open(file_path, "a") as file:
        file.write(resultType + "\n")
        for item in dataToWrite:
            file.write(str(item) + "\n")
        file.write("======================" + "\n")


testFunctionIDs = [
    #'f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11',
    'f12'
]
optimizerID = 'gwo'
runs = 30
for id in range(len(testFunctionIDs)):
    print(optimizerID, testFunctionIDs[id])  
    results = []  
    for _ in range(runs):
        result = OptimizationExecutorFactory.initializingOptimizationExecutor(
            optimizerID, 
            getOptimizerParameter(optimizerID), 
            getTestFunctionParameters(testFunctionIDs[id]),
            testFunctionIDs[id]
        )
        print(result['bestSolution']['objectiveValue'])
        results.append(result['bestSolution']['objectiveValue'])
        
    writeResultToFile(optimizerID+".txt", testFunctionIDs[id], results)

        # print(optimizerID, testFunctionIDs[id], result)
        # print()
    # meanResult = sum(results) / runs
    # print(optimizerID, testFunctionIDs[id], meanResult)
    print()
    