import random
from DatasetReader import readSilhavy71
from helper import MetaheuristicHelper
from use_case_points import UseCasePoint
import sys
import copy


class GreyWolfOptimizer:

    def __init__(self, optimizerParameters, objectiveFunctions, singleTupleDataset):
        self.designVariableRanges = objectiveFunctions['designVariableRanges']
        self.singleTupleDataset = singleTupleDataset
        self.productivityFactor = objectiveFunctions['pf']
        self.maxIter = optimizerParameters['maxIter']
        self.populationSize = optimizerParameters['populationSize']

    def isPositionOutOfRange(self, index, newPosition):
        for i in range(len(self.designVariableRanges)):
            if i == index and (newPosition < self.designVariableRanges[i]['lowerBound'] or newPosition > self.designVariableRanges[i]['upperBound']):
                return True

    def fitnessFunction(self, objectiveValue):
        smallNumber = 0.0001
        return 1 / (objectiveValue + smallNumber)

    def preyHunting(self, population, wolfType, C, A):

        for wolf in population:
            for i in range(len(wolfType['positions'])):
                D = abs(C * wolfType['positions'][i] - wolf['positions'][i])
                newPosition = wolfType['positions'][i] - A * D

                if self.isPositionOutOfRange(i, newPosition):
                    newPosition = wolfType['positions'][i]

                wolf['positions'][i] = newPosition
                objectiveValues = UseCasePoint.estimatingUCP(
                    self.singleTupleDataset, self.productivityFactor, wolf['positions'])
                wolf['estimatedEffort'] = objectiveValues['estimatedEffort']
                wolf['absoluteError'] = objectiveValues['absoluteError']
                wolf['fitnessValue'] = self.fitnessFunction(
                    objectiveValues['absoluteError'])
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
                for j in range(len(self.designVariableRanges)):
                    position = (
                        alphaPopulation[i]['positions'][j] +
                        betaPopulation[i]['positions'][j] +
                        deltaPopulation[i]['positions'][j]) / len(self.designVariableRanges)
                    positions.append(position)
                population[i]['positions'] = positions
                positions = []
            
        return {
            'bestSolution': bestWolf,
            'bestConvergence': bestConvergences
        }