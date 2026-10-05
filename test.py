from TSPWorld import TspWorld
from Baseline import nearestNeighbour,randomSerach,twoOpt

tWorld=TspWorld(r'data\eil51.tsp',426)


nnarrayOrdr,nndist=nearestNeighbour(tWorld.distanceMatrix,5)
randarrayOrder,randdistCount=randomSerach(tWorld.distanceMatrix)

arrayOrder,dsit=twoOpt(tWorld.distanceMatrix)

print('Two Opt')
print(dsit)
print('Random')
print(randdistCount)
print('NN')
print(nndist)