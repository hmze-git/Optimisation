from TSPWorld import TspWorld
from Baseline import nearestNeighbour,randomSerach,twoOpt
from config import trailConfig,GAConfigs

from GeneticAlgo import TSPGA
tWorld=TspWorld(r'data\eil101.tsp',629)


nnarrayOrdr,nndist=nearestNeighbour(tWorld.distanceMatrix,5)
randarrayOrder,randdistCount=randomSerach(tWorld.distanceMatrix)

arrayOrder,dsit=twoOpt(tWorld.distanceMatrix)

print('Two Opt')
print(dsit)
print('Random')
print(randdistCount)
print('NN')
print(nndist)


tWorld=TspWorld(r'data\eil101.tsp',629)

#configs
prob=trailConfig()

ga=GAConfigs()




GA=TSPGA(tWorld,ga,17,None)



bestTours,bestTourLen,hist=GA.run()


print(bestTours)
print(bestTourLen)
print(hist)