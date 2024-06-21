import random, sys, copy

class ParticleSwarmOptimizer:

    def __init__(self, variableRanges, objFunction, popSize=20):
        self.variableRanges = variableRanges
        self.objFunction = objFunction
        self.popSize = popSize
    
    def createInitialPopulation(self, tupleData=None):
        population = []
        
        for _ in range(self.popSize):
            randomVars = []
            
            for i in range(len(self.variableRanges)):
                randomVar = random.gauss(0, 1) * (self.variableRanges[i][1] - self.variableRanges[i][0]) + self.variableRanges[i][0]
                
                while(randomVar < self.variableRanges[i][0] or randomVar > self.variableRanges[i][1]):
                    randomVar = random.gauss(0, 1) * (self.variableRanges[i][1] - self.variableRanges[i][0]) + self.variableRanges[i][0]
                
                randomVars.append(randomVar)

            objValue = self.objFunction.estimatingEffort(tupleData, randomVars)
            absError = abs(objValue-tupleData['actualEffort'])

            population.append({'objValue': objValue, 'variables': randomVars, 'absError': absError, 'velocity': [0,0]})

        return population
    
    def calcLDWInertia(self, iter, maxIter, maxInertia, minInertia):
        return (((maxInertia - minInertia) * (maxIter - iter)) / maxIter) + minInertia
    
    def updateVelocities(self, particle, pBests, gBest, inertia, c1, c2):
        
        velocity = []
        r1 = random.uniform(0,1)
        r2 = random.uniform(0,1)
        
        for i in range(len(particle['velocity'])):
            newVelocity = ( inertia * particle['velocity'][i] + c1 * r1 * (pBests['variables'][i] - particle['variables'][i]) + c2 * r2 * (gBest['variables'][i] - particle['variables'][i]))
            particle['velocity'][i] = newVelocity
            
            velocity.append(newVelocity)
            
        return velocity
    
    def updatingPositions(self, velocity, positions):
        
        newPositions = []
        
        for i in range(len(positions)):
            position = positions[i] + velocity[i]
            
            if position < self.variableRanges[i][0]:
                position = self.variableRanges[i][0]
            if position > self.variableRanges[i][1]:
                position = self.variableRanges[i][1]
            
            newPositions.append(position)
        
        return newPositions
    
    def isUpdatePbest(self, pbest, particle):
        return particle['absError'] < pbest['absError']
            
    def runPSO(self, tupleData, maxIter=20, maxInertia=0.94, minInertia=0.4, c1=2, c2=2):
        bestID = 0
        population = self.createInitialPopulation(tupleData)
        pBest = copy.deepcopy(population)
        gBest = sorted(population, key=lambda x: x['absError'], reverse=False)[bestID]
        tmpGbest = gBest
        bestConvergences = []
        
        for iter in range(maxIter):
            inertia = self.calcLDWInertia(iter, maxIter, maxInertia, minInertia)
            
            for particleID in range(len(population)):
                
                population[particleID]['velocity'] = self.updateVelocities(population[particleID], pBest[particleID], gBest, inertia, c1, c2)
                population[particleID]['variables'] = self.updatingPositions(population[particleID]['velocity'], population[particleID]['variables'])              
                population[particleID]['objValue'] = self.objFunction.estimatingEffort(tupleData, population[particleID]['variables'])
                population[particleID]['absError'] = abs(population[particleID]['objValue'] - tupleData['actualEffort'])
                
                if self.isUpdatePbest(pBest[particleID], population[particleID]):
                    pBest[particleID] = copy.deepcopy(population[particleID])
                
                bestConvergences.append(gBest['absError'])
                gBest = sorted(pBest, key=lambda x: x['absError'], reverse=False)[bestID]
                
                if gBest['absError'] > tmpGbest['absError']:
                    tmpGbest = gBest
        
        return gBest
