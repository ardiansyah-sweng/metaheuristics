
class UseCasePoints:
    def estimatingUCP(dataPoints, simpleUC, averageUC, complexUC):
        simple=0; average=1; complex=2; uaw=3; tcf=4; ecf=5
        simpleUCW = dataPoints[simple] * simpleUC
        averageUCW = dataPoints[average] * averageUC
        complexUCW = dataPoints[complex] * complexUC
        UUCW = simpleUCW + averageUCW + complexUCW
        UUCP = UUCW + dataPoints[uaw]
        UCP = UUCP * dataPoints[tcf] * dataPoints[ecf]
        estimatedEffort = UCP * 20
        return estimatedEffort