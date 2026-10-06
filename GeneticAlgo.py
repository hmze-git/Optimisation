import numpy as np
from Operators import Operator
class TSPGA:


    def __init__(self,problem,config,seed,logger=None):
        self.tspProblem=problem
        self.config=config
        self.seed=seed
        self.rng=np.random.default_rng(seed)


        #Breeding
        self.operators=Operator(self.rng)


        #logging
        self.numEvals=0
        self.logger=logger


    def initialisePop(self):
        numcities=self.tspProblem.numCities
        populationSize=self.config.popSize

        initialisedPop=np.array([self.rng.permutation(numcities) for _ in range(populationSize)]) #create an array of possible populations


        return initialisedPop

    def tournamentSelection(self,tourDistance):
        miniTourney=self.rng.integers(0,len(tourDistance),size=self.config.tournamentSel)


        top1Tourney=np.argmin(tourDistance[miniTourney]) #get the shortest tour

        return top1Tourney

    def createChild(self,tourPop,tourDistances):

        parent1=tourPop[self.tournamentSelection(tourDistances)]
        parent2=tourPop[self.tournamentSelection(tourDistances)]

        child=None
        if self.config.crossover is not None and self.rng.random()<self.config.crossOverRate:
            child=self.operators.orderCrossOver(parent1,parent2)
        else:
            child=parent1.copy() #no crossover means just copy one parent as the child

        if self.rng.random()<self.config.mutationRate:
            child=self.operators.inversionMutation(child)


        return child


    def run(self):
        population=self.initialisePop() #create random initial pop

        tourDistances=self.tspProblem.computePopLen(population)

        self.numEvals=len(population) # compute the tour distnace for every single candidate in the population at first


        bestTourLen=float('inf')
        bestTour=None
        history=[]

        for gen in range(self.config.generations):
            i=int(np.argmin(tourDistances))

            if tourDistances[i]<bestTourLen:
                bestTourLen=tourDistances[i]
                bestTour=population[i].copy()  #copy to be safe
                history.append(bestTourLen) #keep track of the best lengths foudn each generation to observe if it eventually converges

            if self.logger is not None:
                self.logger.record(gen,self.numEvals,population,tourDistances,bestTourLen,bestTour)

            if gen == self.config.generations-1:
                break


            order=np.argsort(tourDistances) #shortest tours first and only the indices dont care about distances

            newPop=[]
            #take top n and keep them to next gen
            for p in order[:self.config.elitism]:
                newPop=[population[p].copy()]


            while len(newPop)<self.config.popSize:
                newPop.append(self.createChild(population,tourDistances))

            population=np.array(newPop)
            tourDistances=self.tspProblem.computePopLen(population)
            self.numEvals+=self.config.popSize-self.config.elitism

    

    
        return bestTour,bestTourLen,history