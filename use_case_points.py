import sys

class UseCasePoint:
    def estimatingUCP(singleTupleTestData, productivityFactor, useCaseWeights):
        """_summary_

        Args:
            singleTupleTestData (_type_): _description_
            productivityFactor (_type_): _description_
            useCaseWeights (_type_): _description_

        Returns:
            _type_: _description_ \n
            output: {'estimatedEffort':6752.52, 'absoluteError':977.52}
        """
        simpleTestData = singleTupleTestData[0]
        averageTestData = singleTupleTestData[1]
        complexTestData = singleTupleTestData[2]
        uawTestData = singleTupleTestData[3]
        tcfTestData = singleTupleTestData[4]
        ecfTestData = singleTupleTestData[5]
        actualEffortTestData = singleTupleTestData[6]
        simpleWeight = useCaseWeights[0]
        averageWeight = useCaseWeights[1]
        complexWeight = useCaseWeights[2]
        
        uucw = (simpleTestData * simpleWeight) + (averageTestData * averageWeight) + (complexTestData * complexWeight)
        
        uucp = uawTestData + uucw
        
        ucp = uucp * tcfTestData * ecfTestData
        
        estimatedEffort = ucp * productivityFactor
        
        absoluteError = abs(actualEffortTestData - estimatedEffort)
      
        absoluteErrorUUCW = abs(singleTupleTestData[7] - uucw)
        
        return {
            'estimatedEffort':estimatedEffort, 
            'absoluteError':absoluteError,
            'estimatedUUCW': uucw,
            'absoluteErrorUUCW': absoluteErrorUUCW
        } 
