from audioop import avg
from DatasetReader import readSilhavy71
import sys

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

def calGRC(min, max, x0, constants = 0.5):
    return (min + (constants * max)) / (x0 + max)

def GRC(datasetDelta0is):
    simple=0; average=1; complex=2; uaw=3; tcf=4; ecf=5; datasetDelta0i=6
    min = 0; max = 1; grcs = []; ret = []
    
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
        
        grcs.append(calGRC(minSimple, maxSimple, datasetDelta0is[datasetDelta0i][l][simple]))
        grcs.append(calGRC(minAverage, maxAverage, datasetDelta0is[datasetDelta0i][l][average]))
        grcs.append(calGRC(minComplex, maxComplex, datasetDelta0is[datasetDelta0i][l][complex]))
        grcs.append(calGRC(minUAW, maxUAW, datasetDelta0is[datasetDelta0i][l][uaw]))
        grcs.append(calGRC(minTCF, maxTCF, datasetDelta0is[datasetDelta0i][l][tcf]))
        grcs.append(calGRC(minECF, maxECF, datasetDelta0is[datasetDelta0i][l][ecf]))
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
    weight = k1 / (k2 + k1)
    
    indexK1 = calcGRG(grc).index(k1)
    indexK2 = calcGRG(grc).index(k2)
    estimatedEffort = (weight * readSilhavy71()[indexK1][actualEffort]) + (weight * readSilhavy71()[indexK2][actualEffort])
    # print(estimatedEffort, abs(estimatedEffort-readSilhavy71()[x0][actualEffort]))
    print(estimatedEffort)

for x0 in range(len(readSilhavy71())):    
    GRG(GRC(calcDeltaOi(x0)), x0)