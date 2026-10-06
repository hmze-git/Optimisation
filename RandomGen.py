import numpy as np
from Operators import Operator
from Baseline import randomSerach
class RandomGen:


    def __init__(self,problem,config,seed):
        self.tspProblem=problem
        self.config=config
        self.seed=seed
        self.rng=np.random.default_rng(seed)

 
    def run(self):

        bestTourLen=float('inf')
        bestTour=None
        history=[]

        for g in range(self.config.generations):

            randTours=[]
            randTourDist=[]
            for p in range(self.config.popSize):
                    randTour,randDist=randomSerach(self.tspProblem.distanceMatrix,self.rng)

                    randTours.append(randTour)
                    randTourDist.append(randDist)
            index=np.argmin(np.asarray(randTourDist))

            randBesttour=randTours[index]
            randBestDist=randTourDist[index]

            if randBestDist<bestTourLen:
                        
                        bestTour=randBesttour
                        bestTourLen=randBestDist
            history.append(bestTourLen) #append the best tour seen up to this point if it stagnates from oen btach to another we know why
                

        return bestTour,bestTourLen,history