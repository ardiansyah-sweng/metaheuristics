from firefly import FireflyOptimizer
from particle_swarm_optimizer import ParticleSwarmOptimizer
from genetic_algorithm import GeneticAlgorithm
from grey_wolf_optimizer import GreyWolfOptimizer
from reptile_search_algorithm import ReptileSearchAlgorithm
from DatasetReader import readSilhavy71, readUCPSeeds, getActualEfforts, getKarnerMAE
from helper import MetaheuristicHelper as metaHelper
import sys
import numpy as np
from performevaluation.SAES import SAES
from performevaluation.Balancer import Balancer

class RunningByDataset:
    def __init__(self, optimizerParameters, objectiveFunctions, dataSet, seeds):
        self.optimizerParameters = optimizerParameters
        self.objectiveFunctions = objectiveFunctions
        self.dataSet = dataSet
        self.seeds = seeds

    def createRandomInitialPopulation(self):
        initialPopulations = []
        for singleTupleTestData in self.dataSet:
            initialPopulation = metaHelper(
                self.objectiveFunctions['designVariableRanges'],
                singleTupleTestData,
                self.objectiveFunctions['pf'],
                self.optimizerParameters['maxIter']
            ).generateInitialPopulation(self.optimizerParameters['populationSize'])
            initialPopulations.append(initialPopulation)
        return initialPopulations

    def executeRSA(self):
        results = []
        initialPopulation = self.createRandomInitialPopulation()
        for i in range(len(self.dataSet)):
            print(self.dataSet[i])
            optimizer = ReptileSearchAlgorithm(
                self.optimizerParameters,
                self.objectiveFunctions,
                self.dataSet[i],
            )
            result = optimizer.runRSA(initialPopulation[i])
            results.append(result)
            sys.exit()
        return results

    def executeFF(self):
        results = []
        initialPopulation = self.createRandomInitialPopulation()
        for i in range(len(self.dataSet)):
            optimizer = FireflyOptimizer(
                self.optimizerParameters,
                self.objectiveFunctions,
                self.dataSet[i],
            )
            results.append(optimizer.runFirefly(initialPopulation[i]))
        return results

    def executePSO(self):
        results = []
        initialPopulation = self.createRandomInitialPopulation()
        for i in range(len(self.dataSet)):
            optimizer = ParticleSwarmOptimizer(
                self.optimizerParameters,
                self.objectiveFunctions,
                self.dataSet[i],
            )
            for j in range(len(initialPopulation)):
                for k in range(len(initialPopulation[j])):
                    initialPopulation[j][k]['velocities'] = optimizer.createInitialVelocities(
                        initialPopulation[j][k]['positions'])
            results.append(optimizer.runPSO(
                initialPopulation[i], self.optimizerParameters['maxIter']))
        return results

    def executeGA(self):
        results = []
        initialPopulation = self.createRandomInitialPopulation()
        for i in range(len(self.dataSet)):
            optimizer = GeneticAlgorithm(
                self.optimizerParameters,
                self.objectiveFunctions,
                self.dataSet[i],
            )
            results.append(optimizer.runGA(initialPopulation[i]))
        return results

    def executeGWO(self):
        results = []
        initialPopulation = self.createRandomInitialPopulation()
        for i in range(len(self.dataSet)):
            optimizer = GreyWolfOptimizer(
                self.optimizerParameters,
                self.objectiveFunctions,
                self.dataSet[i],
            )
            results.append(optimizer.runGWO(initialPopulation[i]))
        return results


class PerformanceEvaluator:
    def __init__(self, results):
        self.results = results

    def calcMAE(self):
        aes = []
        for i in range(len(self.results)):
            aes.append(self.results[i]['bestSolution']['absoluteError'])
        return sum(aes) / len(aes)

    def getBestConvergenceByTupleID(self, tupleID):
        return self.results[tupleID]['bestConvergence']

    def getAbsoluteErrorValue(self):
        rets = []
        for i in range(len(self.results)):
            rets.append(self.results[i]['bestSolution']['absoluteError'])
        return rets

    def writeResultToFile(self, fileName, resultType, dataToWrite):
        folder_path = "/metaheuristics/performevaluation/results/"
        file_path = folder_path + fileName
        with open(file_path, "a") as file:
            file.write("\n" + resultType + "\n")
            for item in dataToWrite:
                file.write(str(item) + "," + "\n")
            file.write("==================================== \n")

    def getEstimatedEfforst(self):
        rets = []
        for i in range(len(self.results)):
            rets.append(self.results[i]['estimatedEffort'])
        return rets

    def getRunsEvaluation(self, maes):
        return {
            'mean': sum(maes) / len(maes),
            'worst': max(maes),
            'best': min(maes),
            'stdev': np.std(maes)
        }

    def getRunsAE(self, aes):
        num_cols = len(aes[0])

        column_sums = [0] * num_cols

        for row in aes:
            for col_index, value in enumerate(row):
                column_sums[col_index] += value

        # print("Jumlah tiap kolom:")
        rets = []
        for col_index, col_sum in enumerate(column_sums):
            rets.append(col_sum/len(aes))
        return rets
    
    def getRunsEstimated(self, runsAES, actualEfforts):
        rets = []
        for i in range(len(actualEfforts)):
            rets.append(actualEfforts[i] - runsAES[i])
        return rets

optimizerParameters = {
    # H. Peng, W. Zhu, C. Deng, and Z. Wu, “Enhancing firefly algorithm with courtship learning,” Inf. Sci. (Ny)., vol. 543, pp. 18–42, 2020, doi: 10.1016/j.ins.2020.05.111.
    'ff': {
        'alpha': 0.5,
        'betaMin': 0.2,
        'beta': 1,
        'gamma': 1,
        'minEpsilon': -5,
        'maxEpsilon': 5,
        'populationSize': 20,
        'maxIter': 20
    },
    'pso': {
        'inertiaMax': 0.9,
        'inertiaMin': 0.4,
        'c1': 2,
        'c2': 2,
        'populationSize': 70,
        'maxIter': 20
    },
    'ga': {
        'crossoverRate': 0.25,
        'mutationRate': 0.1,
        'populationSize': 20,
        'maxIter': 20
    },
    'gwo': {
        'populationSize': 100,
        'maxIter': 20
    },
    # [1] L. Abualigah, M. A. Elaziz, P. Sumari, Z. W. Geem, and A. H. Gandomi, “Reptile Search Algorithm (RSA): A nature-inspired meta-heuristic optimizer,” Expert Syst. Appl., vol. 191, no. November, p. 116158, Apr. 2022, doi: 10.1016/j.eswa.2021.116158.
    'rsa': {
        'alpha': 0.1,
        'beta': 0.1,
        'smallNumber': 0.0000001,
        'populationSize': 30,
        'maxIter': 20
    }
}

dataSet = {
    'ucp': readSilhavy71()
}

dataSeeds = {
    'ucpSeeds': readUCPSeeds()
}

objectiveFunctions = [
    {
        'name': 'ucp',
        'designVariableRanges': [
            {'lowerBound': 5.00, 'upperBound': 7.49},
            {'lowerBound': 7.50, 'upperBound': 12.49},
            {'lowerBound': 12.50, 'upperBound': 15.00}
        ],
        'pf': 20
    }
]

optimizers = [
    'ff', 'ga', 'gwo', 'pso', 'rsa'
]
optimizerID = 0
selector = {
    'optimizer': optimizers[optimizerID],
    'objectiveFunction': 0,
    'dataSet': 'ucp',
    'dataSeeds': 'ucpSeeds'
}

run = RunningByDataset(
    optimizerParameters[selector['optimizer']],
    objectiveFunctions[selector['objectiveFunction']],
    dataSet[selector['dataSet']],
    dataSeeds[selector['dataSeeds']]
)

runTypes = ['single', 'runs']
selectedRunTypeID = 1

if runTypes[selectedRunTypeID] == 'single':
    executors = [run.executeRSA()]
    evaluation = PerformanceEvaluator(executors[0])
    mae = evaluation.calcMAE()
    # print(evaluation.getBestConvergenceByTupleID(17))
    absoluteErrors = evaluation.getAbsoluteErrorValue()
    # evaluation.writeResultToFile(optimizers[optimizerID]+".txt", "Absolute Error", absoluteErrors)

    # saes = SAES(mae, getActualEfforts())
    # res = saes.calcSAES()
    SA = (1-(mae/getKarnerMAE()['mae']))*100
    ES = abs(mae - getKarnerMAE()['mae']) / getKarnerMAE()['stdev']
    print(optimizers[optimizerID], SA, ES)
if runTypes[selectedRunTypeID == 'runs']:
    runs = 30
    maes = []; aes = []
    for _ in range(runs):
        executors = [run.executeRSA()]
        evaluation = PerformanceEvaluator(executors[0])
        mae = evaluation.calcMAE()
        maes.append(mae)
        absoluteErrors = evaluation.getAbsoluteErrorValue()
        aes.append(absoluteErrors)
        # evaluation.writeResultToFile(optimizers[optimizerID]+".txt", "Absolute Error", absoluteErrors)
        # saes = SAES(mae, getActualEfforts())
        # res = saes.calcSAES()
        # SA = (1-(mae/getKarnerMAE()['mae']))*100
        # ES = abs(mae - getKarnerMAE()['mae']) / getKarnerMAE()['stdev']
        # print(optimizers[optimizerID], SA, ES)
    # print(optimizers[optimizerID], evaluation.getRunsEvaluation(maes))
    print(optimizers[optimizerID])
    print()
    runsAE = evaluation.getRunsAE(aes)
    evaluation.writeResultToFile(optimizers[optimizerID]+".txt", "Absolute Error", runsAE)
    runsMAE = sum(runsAE) / len(runsAE)
    runsEstimated = evaluation.getRunsEstimated(runsAE, getActualEfforts())
    balancers = Balancer.calcBalancer(runsAE, getActualEfforts(), runsEstimated)
    # print(runsMAE, balancers)