from turtle import position
import numpy as np
from numpy.random import seed
from numpy.random import rand
import sys
from ChaoticMaps import ChaoticMaps
from Estimator import UseCasePoints

class CPSO:

    def initializingPopulation(dataPoints, popSize):
        # Define input range
        xMin1, xMax1 = 5, 7.49
        xMin2, xMax2 = 7.5, 12.49
        xMin3, xMax3 = 12.5, 15
        
        # Initial particles
        x1Initial = xMin1 + rand(popSize) * (xMax1 - xMin1)
        x2Initial = xMin2 + rand(popSize) * (xMax2 - xMin2)
        x3Initial = xMin3 + rand(popSize) * (xMax3 - xMin3)

        ret = []
        for i in range(popSize):
            ret.append(np.array([x1Initial[i], x2Initial[i], x3Initial[i]]))
        return ret

    def updateVelocity(particles, r1, r2, popSize):
        c1 = 2
        c2 = 2 
        w = 0.8
        ret = []
        for i in range(popSize):
            simpleUC = particles[0][i][0]
            averageUC = particles[0][i][1]
            complexUC = particles[0][i][2]
            pbestSimple = particles[2][i][0]
            pbestAverage = particles[2][i][1]
            pbestComplex = particles[2][i][2]
            gbestSimple = particles[3][0]
            gbestAverage = particles[3][1]
            gbestComplex = particles[3][2]
            vSimple = particles[1][i][0]
            vAverage = particles[1][i][1]
            vComplex = particles[1][i][2]
            
            vSimple = w * vSimple + c1 * r1 * (pbestSimple - simpleUC) + c2 * r2 * (gbestSimple - simpleUC)
            vAverage = w * vAverage + c1 * r1 * (pbestAverage - averageUC) + c2 * r2 * (gbestAverage - averageUC)
            vComplex = w * vComplex + c1 * r1 * (pbestComplex - complexUC) + c2 * r2 * (gbestComplex - complexUC)
            ret.append(np.array([vSimple, vAverage, vComplex]))
        return ret

    def updateParticles(particles, velocities, popSize):
        ret = []
        for i in range(popSize):
            simpleUC = particles[i][0] + velocities[i][0]
            averageUC = particles[i][1] + velocities[i][1]
            complexUC = particles[i][2] + velocities[i][2]
            ret.append(np.array([simpleUC, averageUC, complexUC]))
        return ret
    
    def checkLimit(particles):
        # Define input range
        xMin1, xMax1 = 5, 7.49
        xMin2, xMax2 = 7.5, 12.49
        xMin3, xMax3 = 12.5, 15
        for i in range(len(particles)):
            if (particles[i][0] < xMin1):
                particles[i][0] = float(xMin1)
            if (particles[i][0] > xMax1):
                particles[i][0] = float(xMax1)
            if (particles[i][1] < xMin2):
                particles[i][1] = float(xMin2)
            if (particles[i][1] > xMax2):
                particles[i][1] = float(xMax2)    
            if (particles[i][2] < xMin3):
                particles[i][2] = float(xMin3)
            if (particles[i][2] > xMax3):
                particles[i][2] = float(xMax3)                           
        return particles
    
    def checkPbest(currPbest, currAbsoluteErrors, positions, absoluteErrors):
        ret = []
        for i in range(len(currPbest)):
            if (absoluteErrors[i] < currAbsoluteErrors[i]):
                ret.append(positions[i])
            else:
                ret.append(currPbest[i])   
        return ret
    
    def processingEstimated(popSize, dataPoints, positions):
        absoluteErrors = []; estimatedEfforts = []; actualEffortIndex = 6   
        for i in range(popSize):
            estimatedEffort = UseCasePoints.estimatingUCP(dataPoints, positions[i][0], positions[i][1], positions[i][2])
            ae = abs(estimatedEffort-dataPoints[actualEffortIndex])
            absoluteErrors.append(ae)
            estimatedEfforts.append(estimatedEffort)
        return [estimatedEfforts, absoluteErrors]
       
    def optimizing(dataPoints, popSize, seeds, maxIter):
        estimatedEfforts = [] 
        bestPosition = []
        absoluteErrors = [] 
        actualEffortIndex = 6
        velocities = []
        bests = []; improvements = []
        
        #initialPopulation = CPSO.initializingPopulation(dataPoints, popSize)
        initialPopulation = seeds

        for l in range(popSize):
            estimatedEffort = UseCasePoints.estimatingUCP(dataPoints, initialPopulation[l][0], initialPopulation[l][1], initialPopulation[l][2])
            estimatedEfforts.append(estimatedEffort)
            absoluteErrors.append(abs(estimatedEffort-dataPoints[actualEffortIndex]))
        
        pbest = initialPopulation
        gbestIndex = absoluteErrors.index(min(absoluteErrors))
        gbest = initialPopulation[gbestIndex]
        
        for i in range(maxIter):
            r1 = np.random.rand(1)
            if (i==0):
                r2 =  0.7
                vSimple = np.random.random(popSize)
                vAverage = np.random.random(popSize)
                vComplex = np.random.random(popSize)
                
                for k in range(popSize):
                    velocities.append(np.array([vSimple[k], vAverage[k], vComplex[k] ]))
                        
                particles = np.array([initialPopulation, velocities, pbest, gbest, absoluteErrors])
                
            if (i > 0):
                r2 = ChaoticMaps(i).bernoulli(r2)
                
                vels = CPSO.updateVelocity(particles, r1, r2, popSize)
                positions = CPSO.updateParticles(particles[0], vels, popSize)
                positions = CPSO.checkLimit(positions)
                
                fitness = CPSO.processingEstimated(popSize, dataPoints, positions)
                pbest = CPSO.checkPbest(particles[2], particles[4], positions, fitness[1])
                fitness = CPSO.processingEstimated(popSize, dataPoints, pbest)
                    
                minAE = min(fitness[1])
                gbestIndex = fitness[1].index(minAE)
                gbest = pbest[gbestIndex]
                particles = np.array([positions, vels, pbest, gbest, absoluteErrors])
                
                bests.append(minAE)
                bestPosition.append(gbest)

            improvements = bests

            if (len(improvements) > 10):
                del improvements[0]
                if (len(np.unique(improvements)) == 1):
                    return [improvements[1], bestPosition[0]]
                
        globalBestAE = min(bests)
        indexGlobalBest = bests.index(min(bests))
        globalBestPosition = bestPosition[indexGlobalBest]
        return [globalBestAE, globalBestPosition]