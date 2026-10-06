from TSPWorld import TspWorld
from Baseline import nearestNeighbour,randomSerach,twoOpt
from config import trailConfig,GAConfigs
from Logger import Logger
from RandomGen import RandomGen
from GeneticAlgo import TSPGA
from plots import pltoSeeds
import json
import numpy as np


seeds=[27,37,47,57,67]
gaConf=GAConfigs()
trailConf=trailConfig()
tWorld=TspWorld(trailConf.dataPath,trailConf.optimalSolution)
def run():

    results={'optimalSln':tWorld.optimal,'ga':{},'random':{}}
    for seed in seeds:

        logger=Logger(tWorld,gaConf,1000,'GA')
        rng=np.random.default_rng(seed)
        baseNN=nearestNeighbour(tWorld.distanceMatrix,5) #start from city 5
        based2Opt=twoOpt(tWorld.distanceMatrix,rng)

        geneticTSP=TSPGA(tWorld,gaConf,seed,logger)

        geneticTSP.run()

        results['ga'][str(seed)]=logger.getRows() # reset logger each iteration so this doesnt hold stae info


    with open('results.json','w') as f:
        json.dump(results,f)


run()
with open('results.json') as file:
    results = json.load(file)

pltoSeeds(results['ga'], 'best', 'GA: best so far', 'ga_best.png')
#         ^^^^^^^^^^^^^ this is `runs`
