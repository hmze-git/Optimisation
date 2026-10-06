from dataclasses import dataclass,field

@dataclass
class trailConfig:
    #Configurations for the trail
    #use tsp lib for simplicity 
    dataPath:str='data/eil51.tsp'
    optimalSolution:float=426.0


@dataclass
#CONSIDER USING ELITISM
class GAConfigs:
    popSize: int=50 #how many different arrangements to check each time
    generations:int=50000
    tournamentSel: int=5 # take a groups of  5 tours select the best to be used for eveolution
    crossOverRate: float=0.8 #explore vs exploit partially controlled here
    crossover:str='order1x'  # normal crossover will break the ordering so use this to pick a point 
                            # works by selecting points in par one take those 2 
                            # then take remainder of other parent nor present and place in the child
    
    elitism: int=2 #keep the best 2 tours each generation (if wnat to exploint faster raise this)
    mutationRate: float=0.10
    mutationType:str='swap' # swap units in the child around and see if it improves





