import random
import copy
import sys
import math
from ChaoticMaps import ChaoticMaps
import numpy as np

# R. A. Ibrahim, M. A. Elaziz, and S. Lu, “Chaotic opposition-based grey-wolf optimization algorithm based on differential evolution and disruption operator for global optimization,” Expert Syst. Appl., vol. 108, pp. 1–27, 2018, doi: 10.1016/j.eswa.2018.04.028.


class GreyWolfOptimizerIbrahim2018:

    def __init__(self, variableRanges, objFunction, popSize=100):
        self.variableRanges = variableRanges
        self.objFunction = objFunction
        self.popSize = popSize

    def createInitialPopulation(self, popSize, variableRanges, objFunction, tupleData=None):
        initialPopulation = []
        chaosPopulation = []
        chaosVar = 0.7
        chaosVar = random.uniform(0, 1)

        # create chaos population using Logistic
        for _ in range(popSize):
            randomVars = []
            chaosVar = ChaoticMaps(None).logistic(chaosVar) #sine

            for i in range(len(variableRanges)):
                randomVar = chaosVar * \
                    (variableRanges[i][1] - variableRanges[i]
                     [0]) + variableRanges[i][0]

                while (randomVar < variableRanges[i][0] or randomVar > variableRanges[i][1]):
                    randomVar = chaosVar * \
                        (variableRanges[i][1] - variableRanges[i]
                         [0]) + variableRanges[i][0]

                randomVars.append(randomVar)

            objValue = self.objFunction.estimatingEffort(
                tupleData, randomVars)

            chaosPopulation.append({'objValue': objValue, 'variables': randomVars, 'absError': abs(
                objValue-tupleData['actualEffort'])})

        # create opposition-based initial population
        for i in range(popSize):
            oppositionVariables = []
            for j in range(len(variableRanges)):
                xOpposition = variableRanges[j][1] + \
                    variableRanges[j][0] - chaosPopulation[i]['variables'][j]
                oppositionVariables.append(xOpposition)

            # calc obj function
            objValue = self.objFunction.estimatingEffort(
                tupleData, oppositionVariables)
            absError = abs(objValue - tupleData['actualEffort'])

            if chaosPopulation[i]['absError'] < absError:
                initialPopulation.append(chaosPopulation[i])
            else:
                initialPopulation.append(
                    {'objValue': objValue, 'variables': oppositionVariables, 'absError': absError})

        return initialPopulation

    def preyHunting(self, population, wolfType, C, A, variableRanges, objFunction, tupleData, B):

        for idx, wolf in enumerate(population):
            newVars = []

            for i in range(len(wolfType)):
                D = abs(C * wolfType[i] - wolf['variables'][i])
                newVar = wolfType[i] - B * A * D

                if newVar < variableRanges[i][0]:
                    newVar = variableRanges[i][0]
                if newVar > variableRanges[i][1]:
                    newVar = variableRanges[i][1]

                newVars.append(newVar)

            objValue = self.objFunction.estimatingEffort(
                tupleData, newVars)

            population[idx] = {'objValue': objValue, 'variables': newVars, 'absError': abs(
                objValue - tupleData['actualEffort'])}

        return sorted(population, key=lambda x: x['absError'], reverse=False)

    def diversity(self, varValues):
        data = np.array(varValues)
        colsSum = np.sum(data, axis=0)
        allResults = []
        
        for i in range(self.popSize):
            varResults = []
            for j in range(len(self.variableRanges)):
                avg_j = colsSum[j] / self.popSize
                res = (varValues[i][j] - avg_j)**2
                varResults.append(res)
            allResults.append(math.sqrt(sum(varResults)))
        
        return sum(allResults) / self.popSize

    def runGWO(self, variableRanges, objFunction, tupleData, maxIter=20, popSize=100):

        bestWolf = {'objValue': None, 'absError': 10000}
        
        varValues = []
        population = self.createInitialPopulation(
            popSize, variableRanges, objFunction, tupleData)
        for val in population:
            varValues.append(val['variables'])
            
        diversityRate = self.diversity(varValues)
        print(diversityRate)
            
        population = sorted(
            population, key=lambda x: x['absError'], reverse=False)
        
        bestConvergences = []

        for iter in range(maxIter):
            varValues = []
            
            # Initializing a, A, and C
            coefficient = 2
            a = 2 * math.cos((math.pi/2) * (iter/maxIter))

            alphaA = (coefficient * a) * random.uniform(0, 1) - a
            betaA = (coefficient * a) * random.uniform(0, 1) - a
            deltaA = (coefficient * a) * random.uniform(0, 1) - a

            B = math.cos((math.pi/2) * (iter/maxIter))

            alphaC = random.gauss(0, 1)
            betaC = random.gauss(0, 1)
            deltaC = random.gauss(0, 1)

            # 5. Encircling Prey
            alphaIndex = 0
            betaIndex = 1
            deltaIndex = 2

            alphaWolf = population[alphaIndex]
            alphaPopulation = self.preyHunting(
                population, alphaWolf['variables'], alphaC, alphaA, variableRanges, objFunction, tupleData, B)

            betaWolf = population[betaIndex]
            betaPopulation = self.preyHunting(
                population, betaWolf['variables'], betaC, betaA, variableRanges, objFunction, tupleData, B)

            deltaWolf = population[deltaIndex]
            deltaPopulation = self.preyHunting(
                population, deltaWolf['variables'], deltaC, deltaA, variableRanges, objFunction, tupleData, B)

            for i in range(popSize):
                positions = []

                for j in range(len(variableRanges)):

                    position = (alphaPopulation[i]['variables'][j] + betaPopulation[i]['variables']
                                [j] + deltaPopulation[i]['variables'][j]) / len(variableRanges)

                    positions.append(position)

                objValue = self.objFunction.estimatingEffort(
                    tupleData, positions)

                population[i] = {'objValue': objValue, 'variables': [
                    positions[0], positions[1]], 'absError': abs(objValue-tupleData['actualEffort'])}
                
                varValues.append([positions[0], positions[1]])

            if alphaWolf['absError'] < bestWolf['absError']:
                bestWolf = copy.deepcopy(alphaWolf)
            
            diversityRate = self.diversity(varValues)
            print(diversityRate)
            
            # print(bestWolf['absError'])
            bestConvergences.append(bestWolf['absError'])
        
        # for data in bestConvergences:
        #     print(data)
        sys.exit()
    
        return bestWolf
