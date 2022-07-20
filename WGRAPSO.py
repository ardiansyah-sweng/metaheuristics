from random import random
from audioop import avg, reverse
from DatasetReader import readSilhavy71
import sys
import time

def createPopulation():
    numOfDims = 6; popSize = 20; particles = []; population = []
    for _ in range(popSize):
        for _ in range(numOfDims):
            particles.append(random())
        population.append(particles)
        particles = []
    return population

def getMinMaxEffortDrivers(dataset, effortDriver):
    simple=0; average=1; complex=2; uaw=3; tcf=4; ecf=5
    simpleEffortDrivers = []; averageEffortDrivers = []; complexEffortDrivers = []; uawEffortDrivers = []; tcfEffortDrivers = []; ecfEffortDrivers = []
    for l in range(len(dataset)):
        simpleEffortDrivers.append(dataset[l][simple])
        averageEffortDrivers.append(dataset[l][average])
        complexEffortDrivers.append(dataset[l][complex])
        uawEffortDrivers.append(dataset[l][uaw])
        tcfEffortDrivers.append(dataset[l][tcf])
        ecfEffortDrivers.append(dataset[l][ecf])

    if effortDriver == 'simple':
        return [min(simpleEffortDrivers), max(simpleEffortDrivers)]
    if effortDriver == 'average':
        return [min(averageEffortDrivers), max(averageEffortDrivers)]
    if effortDriver == 'complex':
        return [min(complexEffortDrivers), max(complexEffortDrivers)]
    if effortDriver == 'uaw':
        return [min(uawEffortDrivers), max(uawEffortDrivers)]
    if effortDriver == 'tcf':
        return [min(tcfEffortDrivers), max(tcfEffortDrivers)]
    if effortDriver == 'ecf':
        return [min(ecfEffortDrivers), max(ecfEffortDrivers)]
    
def calcDeltaOi(x0):
    simple=0; average=1; complex=2; uaw=3; tcf=4; ecf=5
    delta0is = []; datasetDelta0is = []; ret = []
    
    # print('x0 = ', readSilhavy71()[x0])
    x0Simple = readSilhavy71()[x0][simple]
    x0Average = readSilhavy71()[x0][average]
    x0Complex = readSilhavy71()[x0][complex]
    x0uaw = readSilhavy71()[x0][uaw]
    x0tcf = readSilhavy71()[x0][tcf]
    x0ecf = readSilhavy71()[x0][ecf]

    for m in range(len(readSilhavy71())):
        if (x0 != m):           
            delta0is.append(abs(x0Simple - readSilhavy71()[m][simple]))
            delta0is.append(abs(x0Average - readSilhavy71()[m][average]))
            delta0is.append(abs(x0Complex - readSilhavy71()[m][complex]))
            delta0is.append(abs(x0uaw - readSilhavy71()[m][uaw]))
            delta0is.append(abs(x0tcf - readSilhavy71()[m][tcf]))
            delta0is.append(abs(x0ecf - readSilhavy71()[m][ecf]))
            datasetDelta0is.append(delta0is)
            delta0is = []
    ret.append(getMinMaxEffortDrivers(datasetDelta0is, 'simple'))
    ret.append(getMinMaxEffortDrivers(datasetDelta0is, 'average'))
    ret.append(getMinMaxEffortDrivers(datasetDelta0is, 'complex'))
    ret.append(getMinMaxEffortDrivers(datasetDelta0is, 'uaw'))
    ret.append(getMinMaxEffortDrivers(datasetDelta0is, 'tcf'))
    ret.append(getMinMaxEffortDrivers(datasetDelta0is, 'ecf'))
    ret.append(datasetDelta0is)
    return ret

def calGRC(weight, min, max, x0, constants = 0.5):
    return weight * ((min + (constants * max)) / (x0 + max))

def GRC(datasetDelta0is, effortDriverWeights):
    simple=0; average=1; complex=2; uaw=3; tcf=4; ecf=5; datasetDelta0i=6
    min = 0; max = 1; grcs = []; ret = []
    weightSimple = effortDriverWeights[simple]
    weightAverage = effortDriverWeights[average]
    weightComplex = effortDriverWeights[complex]
    weightUAW = effortDriverWeights[uaw]
    weightTCF = effortDriverWeights[tcf]
    weightECF = effortDriverWeights[ecf]
    for l in range(len(datasetDelta0is[datasetDelta0i])):
        minSimple = datasetDelta0is[simple][min]
        maxSimple = datasetDelta0is[simple][max]
        minAverage = datasetDelta0is[average][min]
        maxAverage = datasetDelta0is[average][max]
        minComplex = datasetDelta0is[complex][min]
        maxComplex = datasetDelta0is[complex][max]
        minUAW = datasetDelta0is[uaw][min]
        maxUAW = datasetDelta0is[uaw][max]
        minTCF = datasetDelta0is[tcf][min]
        maxTCF = datasetDelta0is[tcf][max]
        minECF = datasetDelta0is[ecf][min]
        maxECF = datasetDelta0is[ecf][max]
        
        grcs.append(calGRC(weightSimple, minSimple, maxSimple, datasetDelta0is[datasetDelta0i][l][simple]))
        grcs.append(calGRC(weightAverage, minAverage, maxAverage, datasetDelta0is[datasetDelta0i][l][average]))
        grcs.append(calGRC(weightComplex, minComplex, maxComplex, datasetDelta0is[datasetDelta0i][l][complex]))
        grcs.append(calGRC(weightUAW, minUAW, maxUAW, datasetDelta0is[datasetDelta0i][l][uaw]))
        grcs.append(calGRC(weightTCF, minTCF, maxTCF, datasetDelta0is[datasetDelta0i][l][tcf]))
        grcs.append(calGRC(weightECF, minECF, maxECF, datasetDelta0is[datasetDelta0i][l][ecf]))
        ret.append(grcs)
        grcs = []
    return ret

def calcGRG(grc):
    averages = []
    for l in range(len(grc)):
        averages.append(sum(grc[l]) / len(grc[l]))
    return averages

def GRG(grc, x0):
    actualEffort = 6    
    grg = calcGRG(grc)
    grg.sort(reverse=1)
    k1 = grg[0]; k2 = grg[1]
    if (k1 == 0 and k2 == 0):
        weight = k1
    else:
        weight = k1 / (k2 + k1)
    
    indexK1 = calcGRG(grc).index(k1)
    indexK2 = calcGRG(grc).index(k2)
    estimatedEffort = (weight * readSilhavy71()[indexK1][actualEffort]) + (weight * readSilhavy71()[indexK2][actualEffort])
    # print(estimatedEffort, abs(estimatedEffort-readSilhavy71()[x0][actualEffort]))
    return estimatedEffort

def updateVelocity(particles, r1, r2, popSize = 20):
    c1 = c2 = 2; w = 0.8; ret = []; pop = 0; vel = 1; p_best= 2; g_best = 3; oneParticles = []; ret = []
    simple = 0; average=1; complex=2; uaw=3; tcf=4; ecf=5

    for i in range(popSize):
        simpleWeight = particles[pop][i][simple]
        averageWeight = particles[pop][i][average]
        complexWeight = particles[pop][i][complex]
        uawWeight = particles[pop][i][uaw]
        tcfWeight = particles[pop][i][tcf]
        ecfWeight = particles[pop][i][ecf]
        vSimple = particles[vel][i][simple]
        vAverage = particles[vel][i][average]
        vComplex = particles[vel][i][complex]
        vUAW = particles[vel][i][uaw]
        vTCF = particles[vel][i][tcf]
        vECF = particles[vel][i][ecf]
        pbestSimple = particles[p_best][i][simple]
        pbestAverage = particles[p_best][i][average]
        pbestComplex = particles[p_best][i][complex]
        pbestUAW = particles[p_best][i][uaw]
        pbestTCF = particles[p_best][i][tcf]
        pbestECF = particles[p_best][i][ecf]
        gbestSimple = particles[g_best][simple]
        gbestAverage = particles[g_best][average]
        gbestComplex = particles[g_best][complex]
        gbestUAW = particles[g_best][uaw]
        gbestTCF = particles[g_best][tcf]
        gbestECF = particles[g_best][ecf]
        
        vSimple = w * vSimple + c1 * r1 * (pbestSimple - simpleWeight) + c2 * r2 * (gbestSimple - simpleWeight)
        vAverage = w * vAverage + c1 * r1 * (pbestAverage - averageWeight) + c2 * r2 * (gbestAverage - averageWeight)
        vComplex = w * vComplex + c1 * r1 * (pbestComplex - complexWeight) + c2 * r2 * (gbestComplex - complexWeight)
        vUAW = w * vUAW + c1 * r1 * (pbestUAW - uawWeight) + c2 * r2 * (gbestUAW - uawWeight)
        vTCF = w * vTCF + c1 * r1 * (pbestTCF - tcfWeight) + c2 * r2 * (gbestTCF - tcfWeight)
        vECF = w * vECF + c1 * r1 * (pbestECF - ecfWeight) + c2 * r2 * (gbestECF - ecfWeight)
        oneParticles.append(vSimple)
        oneParticles.append(vAverage)
        oneParticles.append(vComplex)
        oneParticles.append(vUAW)
        oneParticles.append(vTCF)
        oneParticles.append(vECF)

        ret.append(oneParticles)
        oneParticles = []
    return ret

def updatePositions(currentPositions, velocities, popSize = 20):
    weights = []; ret = []
    for i in range(popSize):
        simpleWeight = currentPositions[i][0] + velocities[i][0]
        averageWeight = currentPositions[i][1] + velocities[i][1]
        complexWeight = currentPositions[i][2] + velocities[i][2]
        uawWeight = currentPositions[i][3] + velocities[i][3]
        tcfWeight = currentPositions[i][4] + velocities[i][4]
        ecfWeight = currentPositions[i][5] + velocities[i][5]
        weights.append(simpleWeight)
        weights.append(averageWeight)
        weights.append(complexWeight)
        weights.append(uawWeight)
        weights.append(tcfWeight)
        weights.append(ecfWeight)    
        ret.append(weights)
        weights = []
    return ret
    
def ascAEsort(AEs):
    AEs.sort()
    return AEs

def calcEffortEstimation(population, x0):
    AEs = []; dataset = readSilhavy71(); estimatedEfforts = []
    for l in range(len(population)):           
        estimatedEffort = GRG(GRC(calcDeltaOi(x0), population[l]), x0)
        ae = abs(estimatedEffort-dataset[x0][actualEffort])
        AEs.append(ae)
        estimatedEfforts.append(estimatedEffort)
    return [AEs, estimatedEfforts]

def checkLimit(particles):
    min = sim = 0; max = avg = 1; com=2;uaw=3;tcf=4;ecf=5
    for i in range(len(particles)):
        if (particles[i][sim] < min):
            particles[i][sim] = float(min)
        if (particles[i][sim] > max):
            particles[i][sim] = float(max)
            
        if (particles[i][avg] < min):
            particles[i][avg] = float(min)
        if (particles[i][avg] > max):
            particles[i][avg] = float(max)
            
        if (particles[i][com] < min):
            particles[i][com] = float(min)
        if (particles[i][com] > max):
            particles[i][com] = float(max)
            
        if (particles[i][uaw] < min):
            particles[i][uaw] = float(min)
        if (particles[i][uaw] > max):
            particles[i][uaw] = float(max)

        if (particles[i][tcf] < min):
            particles[i][tcf] = float(min)
        if (particles[i][tcf] > max):
            particles[i][tcf] = float(max)

        if (particles[i][ecf] < min):
            particles[i][ecf] = float(min)
        if (particles[i][ecf] > max):
            particles[i][ecf] = float(max)
    return particles

def checkPbest(currPbest, currAEs, positions, AEs):
    ret = []
    for i in range(len(currPbest)):
        if (AEs[i] < currAEs[i]):
            ret.append(positions[i])
        else:
            ret.append(currPbest[i])
    return ret

for x0 in range(len(readSilhavy71())):
    startTime = time.time()
    
    actualEffort = 6; maxIter = 30; popSize = 20; velocities = []; 
    ae = 0; bests = []; bestPosition = []
    for i in range(maxIter):
        r1 = random(); r2 = random()
        if (i==0):
            population = createPopulation()
            estimatedEfforts = calcEffortEstimation(population, x0)
            velocities = createPopulation()
            pbest = population
            gbestIndex = estimatedEfforts[ae].index(min(estimatedEfforts[ae]))
            gbest = population[gbestIndex]
            particles = [population, velocities, pbest, gbest, estimatedEfforts[ae]]

        if (i>0):
            vels = updateVelocity(particles, r1, r2)
            positions = updatePositions(particles[0], vels)
            positions = checkLimit(positions)

            fitness = calcEffortEstimation(positions, x0)
            pbest = checkPbest(particles[2], particles[4], positions, fitness[ae])
            fitness = calcEffortEstimation(pbest, x0)
            
            minAE = min(fitness[ae])
            gbestIndex = fitness[ae].index(minAE)
            gbest = pbest[gbestIndex]
            particles = [positions, vels, pbest, gbest, fitness[ae]]
            
            bests.append(minAE)
            bestPosition.append(gbest)
                
    globalBestAE = min(bests)
    indexGlobalBest = bests.index(min(bests))
    globalBestPosition = bestPosition[indexGlobalBest]
    print(x0, globalBestAE, globalBestPosition)
    #print('--- %s seconds ---' % (time.time() - startTime))
    bests = []; bestPosition = []