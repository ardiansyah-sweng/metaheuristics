
class Balancer:
    def calcBalancer(absoluteErrors, actualEfforts, estimatedEfforts):
        sumMBRE, sumMIBRE = 0, 0
        for i in range(len(absoluteErrors)):
            if (actualEfforts[i] < estimatedEfforts[i]):
                minAE = actualEfforts[i]
                maxAE = estimatedEfforts[i]
            else:
                minAE = estimatedEfforts[i]
                maxAE = actualEfforts[i]
            sumMBRE += (absoluteErrors[i] / minAE)
            sumMIBRE += (absoluteErrors[i] / maxAE)
            
        mbre = sumMBRE / len(absoluteErrors)
        mibre = sumMIBRE / len(absoluteErrors)
        return {'mbre':mbre, 'mibre':mibre}