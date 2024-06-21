import random
from testfunctions.multimodal import MultimodalFunctionsFactory
from helper import MetaheuristicHelper as metaHelper
import sys
import copy


class GreyWolfOptimizer:

    def __init__(self, optimizerParameters, testFunctionParameters, testFunctionID):
        self.maxIter = optimizerParameters['maxIter']
        self.populationSize = optimizerParameters['populationSize']
        self.testFunctionParameters = testFunctionParameters
        self.testFunctionID = testFunctionID

    def isPositionOutOfRange(self, index, newPosition):
        for i in range(self.testFunctionParameters['dimension']):
            if i == index and (newPosition < self.testFunctionParameters['ranges'][0] or newPosition > self.testFunctionParameters['ranges'][1]):
                return True

    def fitnessFunction(self, objectiveValue):
        smallNumber = 0.0001
        return 1 / (objectiveValue + smallNumber)

    def preyHunting(self, population, wolfType, C, A):
        """_summary_

        Args:
            population (_type_): _description_
            wolfType (_type_): _description_
            C (_type_): _description_
            A (_type_): _description_

        Returns:
            _type_: _description_ \n
            output: \n
            [{'positions': [5.753280577089415, 8.771653487287988, 14.210280795690014], \n
            'estimatedEffort': 4686.4649751245925, \n
            'absoluteError': 3283.5350248754075, \n
            'fitnessValue': 0.0003045498104844986}, \n
            ...
        """
        for wolf in population:
            for i in range(len(wolfType['positions'])):
                D = abs(C * wolfType['positions'][i] - wolf['positions'][i])
                newPosition = wolfType['positions'][i] - A * D

                if self.isPositionOutOfRange(i, newPosition):
                    newPosition = wolfType['positions'][i]

                wolf['positions'][i] = newPosition
                objectiveValue = MultimodalFunctionsFactory.initializingMultimodalFunctions(self.testFunctionID, wolf['positions'])
                wolf['objectiveValue'] = objectiveValue
                wolf['fitnessValue'] = metaHelper(
                    None,None,None,None,None
                    ).fitnessFunction(objectiveValue)
        return population

    def runGWO(self, population):
        column = {
            'fitnessValue': 'fitnessValue',
            'alphaIndex': 0,
            'betaIndex': 0,
            'deltaIndex': 2
        }
        bestWolf = {
            'wolfPositions': None,
            'estimatedEffort': None,
            'absoluteError': None,
            'fitnessValue': 0
        }
        bestConvergences = []
        for iter in range(self.maxIter):
            population = sorted(
                population, key=lambda x: x['fitnessValue'], reverse=True)

            # 4. Initializing a, A, and C
            coefficient = 2
            a = coefficient - (coefficient * iter) / self.maxIter
            A = (coefficient * a) * random.uniform(0, 1) - a
            C = coefficient * random.uniform(0, 1)

            # 5. Encircling Prey
            alphaWolf = population[column['alphaIndex']]
            alphaPopulation = self.preyHunting(population, alphaWolf, C, A)
            bestConvergences.append(bestWolf['fitnessValue'])
            if alphaWolf['fitnessValue'] > bestWolf['fitnessValue']:
                bestWolf = copy.deepcopy(alphaWolf)

            betaPopulation = self.preyHunting(
                population, population[column['betaIndex']], C, A)
            deltaPopulation = self.preyHunting(
                population, population[column['deltaIndex']], C, A)

            positions = []
            for i in range(self.populationSize):
                for j in range(self.testFunctionParameters['dimension']):
                    position = (
                        alphaPopulation[i]['positions'][j] +
                        betaPopulation[i]['positions'][j] +
                        deltaPopulation[i]['positions'][j]) / self.testFunctionParameters['dimension']
                    positions.append(position)
                population[i]['positions'] = positions
                positions = []
        return {
            'bestSolution': bestWolf,
            'bestConvergence': bestConvergences
        }
