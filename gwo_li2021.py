import random, copy, sys, math
from ChaoticMaps import ChaoticMaps

# Y. Li, X. Lin, and J. Liu, “An improved gray wolf optimization algorithm to solve engineering problems,” Sustain., vol. 13, no. 6, pp. 1–23, 2021, doi: 10.3390/su13063208.
class IGreyWolfOptimizerLi2021:

    def __init__(self, variableRanges, objFunction, popSize=100):
        self.variableRanges = variableRanges
        self.objFunction = objFunction
        self.popSize = popSize
        
    def createInitialPopulation(self, popSize, variableRanges, objFunction, tupleData=None):
        population = []
        chaosVar = 0.7
        #chaosVar = random.uniform(0,1)
        
        for _ in range(popSize):
            randomVars = []
            #chaosVar = (2 * chaosVar) % 1   
            chaosVar = ChaoticMaps(None).chebyshev(chaosVar)

            for i in range(len(variableRanges)):
                randomVar = chaosVar * (variableRanges[i][1] - variableRanges[i][0]) + variableRanges[i][0]
                
                while(randomVar < variableRanges[i][0] or randomVar > variableRanges[i][1]):
                    randomVar = chaosVar * (variableRanges[i][1] - variableRanges[i][0]) + variableRanges[i][0]
                    
                randomVars.append(randomVar)
            
            objValue = self.objFunction.estimatingEffort(tupleData, randomVars)
            
            population.append({'objValue':objValue, 'variables':randomVars, 'absError':abs(objValue-tupleData['actualEffort'])})
        
        return population
    
    def preyHunting(self, population, wolfType, C, A, variableRanges, objFunction, tupleData, B):
        
        for idx, wolf in enumerate(population):
            newVars = []
            
            for i in range(len(wolfType)):
                D = abs(C * wolfType[i] - wolf['variables'][i])
                print(C, wolfType[i], wolf['variables'][i])
                
                newVar = wolfType[i] - B * A * D

                if newVar < variableRanges[i][0]:
                    newVar = variableRanges[i][0]
                if newVar > variableRanges[i][1]:
                    newVar = variableRanges[i][1]
                
                newVars.append(newVar)
            
            objValue = self.objFunction.estimatingEffort(tupleData, newVars)
            
            population[idx] = {'objValue': objValue, 'variables': newVars, 'absError': abs(objValue - tupleData['actualEffort'])}
        
        return sorted(population, key=lambda x: x['absError'], reverse=False)
        
    def runGWO(self, variableRanges, objFunction, tupleData, maxIter=20, popSize=100):
        
        bestWolf = {'objValue':None, 'absError':10000}
        
        population = self.createInitialPopulation(popSize, variableRanges, objFunction, tupleData)
        population = sorted(population, key=lambda x: x['absError'], reverse=False)        

        bestConvergences = []

        for iter in range(maxIter):
                       
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
            alphaIndex = 0; betaIndex = 1; deltaIndex = 2
            
            alphaWolf = population[alphaIndex]        
            alphaPopulation = self.preyHunting(population, alphaWolf['variables'], alphaC, alphaA, variableRanges, objFunction, tupleData, B)
            
            betaWolf = population[betaIndex]
            betaPopulation = self.preyHunting(
                population, betaWolf['variables'], betaC, betaA, variableRanges, objFunction, tupleData, B)
            
            deltaWolf = population[deltaIndex]
            deltaPopulation = self.preyHunting(
                population, deltaWolf['variables'], deltaC, deltaA, variableRanges, objFunction, tupleData, B)
                       
            for i in range(popSize):
                positions = []
                
                for j in range(len(variableRanges)):
                    
                    position = (alphaPopulation[i]['variables'][j] + betaPopulation[i]['variables'][j] + deltaPopulation[i]['variables'][j]) / len(variableRanges)
                    
                    positions.append(position)
                
                objValue = self.objFunction.estimatingEffort(tupleData, positions)
                
                population[i] = {'objValue': objValue, 'variables': [
                    positions], 'absError': abs(objValue-tupleData['actualEffort'])}
            
            if alphaWolf['absError'] < bestWolf['absError']:
                bestWolf = copy.deepcopy(alphaWolf)
            
            print(bestWolf['absError'])
        sys.exit()
        return bestWolf
