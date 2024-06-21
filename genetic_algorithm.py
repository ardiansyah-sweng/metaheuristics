import random
from DatasetReader import readSilhavy71
from use_case_points import UseCasePoint
import sys, copy
from helper import MetaheuristicHelper

class GeneticAlgorithm:
    
    def __init__(self, optimizerParameters, objectiveFunctions, singleTupleDataset):
        self.designVariableRanges = objectiveFunctions['designVariableRanges']
        self.singleTupleDataset = singleTupleDataset
        self.productivityFactor = objectiveFunctions['pf']
        self.crossoverRate = optimizerParameters['crossoverRate']
        self.maxIter = optimizerParameters['maxIter']
        self.mutationRate = optimizerParameters['mutationRate']
        
    def createNewChromosome(self, positions):
        objectiveValue = UseCasePoint.estimatingUCP(
                self.singleTupleDataset,
                self.productivityFactor,
                positions
        )
        return {
            'positions': positions,
            'estimatedEffort': objectiveValue['estimatedEffort'],
            'absoluteError': objectiveValue['absoluteError'],
            'fitnessValue': MetaheuristicHelper(
                self.designVariableRanges,
                self.singleTupleDataset,
                self.productivityFactor,
                self.maxIter
            ).fitnessFunction(objectiveValue['absoluteError'])
        }
    
    def oneCutPointCrossover(self, population):
        """_summary_

        Args:
            population (_type_): _description_
        
        Output: membentuk chromosome anak \n
            [{'positions': [6.4812846164094005, 8.233009406814505, 14.625707390446175], 'estimatedEffort': 4757.403238977785, 'absoluteError': 3212.596761022215, 'fitnessValue': 0.0003112746613597233}, {'positions': [6.4812846164094005, 8.233009406814505, 14.625707390446175], 'estimatedEffort': 4757.403238977785, 'absoluteError': 3212.596761022215, 'fitnessValue': 0.0003112746613597233}]
        """
        selectedChromosomes = []
        while len(selectedChromosomes) <= 1:
            for i in range(len(population)):
                if random.uniform(0,1) < self.crossoverRate:
                    selectedChromosomes.append({'chromosome':population[i], 'replacedIndex':i})

        parents = []
        for i in range(len(selectedChromosomes)):
            for j in range(len(selectedChromosomes)):
                if i != j:
                    parents.append([selectedChromosomes[i]['chromosome'], selectedChromosomes[j]['chromosome']])
                    # output harus satu pasang chromosome berlainan:
                    # [{'positions': [6.596363404268636, 10.935389580377029, 13.526427803409742], 'velocities': [1.5202536762163128, 9.590500412193261, 4.372146926371975], 'estimatedEffort': 4910.1541365614285, 'absoluteError': 3059.8458634385715, 'fitnessValue': 0.0003268138370195038}, {'positions': [6.456309886821895, 11.63496900155566, 14.520813304630629], 'velocities': [2.3598422912473795, 2.0789412542731824, 0.4588583637989641], 'estimatedEffort': 5196.8917831121325, 'absoluteError': 2773.1082168878675, 'fitnessValue': 0.000360606181125393}]
        
        cutPointIndex = random.randint(0, len(self.designVariableRanges)-1)
        offSpringPositions = []; leftParentIndex = 0; rightParentIndex = 1
        for i in range(len(selectedChromosomes)):
            for j in range(len(self.designVariableRanges)):
                if j <= cutPointIndex:
                    offSpringPositions.append(parents[i][leftParentIndex]['positions'][j])
                if j > cutPointIndex:
                    offSpringPositions.append(parents[i][rightParentIndex]['positions'][j])
            
            chromosome = self.createNewChromosome(offSpringPositions)
            if chromosome['fitnessValue'] > population[selectedChromosomes[i]['replacedIndex']]['fitnessValue']:
                population[selectedChromosomes[i]['replacedIndex']] = copy.deepcopy(chromosome)
        return population
    
    def rouletteWheelSelection(self, population):
        """_summary_

        Args:
            population (_type_): _description_
        
        Output: \n
            [{'positions': [6.7733221491638576, 11.566710785879692, 13.159885587824594], \n
             'estimatedEffort': 4935.694056764195, \n
             'absoluteError': 3034.305943235805, \n
             'fitnessValue': 0.0003295646469904509}
        """
        sumFitnessValue = 0
        for chromosome in population:
            sumFitnessValue = sumFitnessValue + chromosome['fitnessValue']
        
        probabilities = []        
        probabilityCummulative = 0
        for chromosome in population:
            probabilityCummulative += (chromosome['fitnessValue'] / sumFitnessValue)
            probabilities.append(probabilityCummulative)

        for i in range(len(population)):
            for j in range(len(probabilities)):
                if random.uniform(0,1) <= probabilities[j]:
                    population[i] = copy.deepcopy(population[j])
                    break
        return population
    
    #TODO: buat riset/kaji mendalam apakah beda hasilnya menggabungkan seluruh gen atau acak tiap kromosom dan gen
    def mutation(self, population):
        ret = False
        mutatedValue = 0
        mutationRate = 1 / len(self.designVariableRanges)
        numMutation = round(mutationRate * len(population))
        if numMutation:
            for _ in range(numMutation):
                randomChromosomeIndex = random.randint(0, len(population)-1)
                selectedGenIndex = random.randint(0, len(self.designVariableRanges)-1)
                while mutatedValue < self.designVariableRanges[selectedGenIndex]['lowerBound'] or mutatedValue > self.designVariableRanges[selectedGenIndex]['upperBound']:
                    mutatedValue = random.uniform(
                        self.designVariableRanges[selectedGenIndex]['lowerBound'], 
                        self.designVariableRanges[selectedGenIndex]['upperBound']
                    )
                population[randomChromosomeIndex]['positions'][selectedGenIndex] = mutatedValue
                chromosome = self.createNewChromosome(population[randomChromosomeIndex]['positions'])
                population[randomChromosomeIndex] = copy.deepcopy(chromosome)
            ret = population
        return ret
    
    def runGA(self, population):
        bestChromosome = {
            'positions':None,
            'estimatedEffort':None,
            'absoluteError': None,
            'fitnessValue': 0
        }
        bestID = 0
        bestConvergences = []
        for _ in range(self.maxIter):
            population = copy.deepcopy(self.rouletteWheelSelection(population))
            population = copy.deepcopy(self.oneCutPointCrossover(population))
            population = copy.deepcopy(self.mutation(population))
            population = sorted(population, key=lambda x: x['fitnessValue'], reverse=True)
            bestConvergences.append(bestChromosome['fitnessValue'])
            #untuk analisis konvergensi
            if population[bestID]['fitnessValue'] > bestChromosome['fitnessValue']:
                bestChromosome = copy.deepcopy(population[bestID])
        return {
            'bestSolution':bestChromosome, 
            'bestConvergence':bestConvergences
        }