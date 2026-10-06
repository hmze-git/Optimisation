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
            
