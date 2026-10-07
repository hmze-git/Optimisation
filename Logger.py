import numpy as np
import json
class Logger:

    def __init__(self,tspProblem,config,logWhen=100,solutionType='GA'):
        
        self.problem=tspProblem
        self.logWhen=logWhen
        self.solutionType=solutionType
        self.rows=[]
        self.config=config
    #get array of all the edges in the tour as tuples
    def getEdges(self,tour):

        allEdges = []


        for i in range(len(tour)):
                currentCity = tour[i] #tour stores city numbers remember 

                # the city after the current city
                # for the last city return to the first city
                if i == len(tour) - 1:
                    nextCity = tour[0]
                else:
                    nextCity = tour[i + 1]

                edge=tuple(sorted((currentCity,nextCity))) #small to big      
                allEdges.append(edge)

        return allEdges
    def record(self,gen,population,distances,bestDistance,bestTour):

        bestEdges = self.getEdges(bestTour)

        similarityToBestVals = []

        for tour in population:
            tourEdges = self.getEdges(tour)

            sharedCount = 0

            for edge in tourEdges: #check what portion of edges in best tour can be found in rest of the population
                                    #tells us how well the thing is convering
                if edge in bestEdges:
                    sharedCount += 1

            similarityToBest=(sharedCount / len(tourEdges))

            similarityToBestVals.append(similarityToBest)

            

       

        popSim=sum(similarityToBestVals)/len(similarityToBestVals)
        row = {
            'gen': gen,                         
            'best': bestDistance,                            
            'diffPercent': self.problem.differenceToBest(bestDistance),           # how different is GA to best
            'tourMean': float(distances.mean()), # what is the mean distance
            'tourWorst': float(distances.max()), #what is the worst distance seen
            'tourStd': float(distances.std()), #what is the deviation from the mean across the tours
            'similarity': popSim,     
            }

        self.rows.append(row)


        if gen%self.logWhen==0 or gen==self.config.generations-1:

                print(f'Generation:{gen}| bestDist:{bestDistance} | diffrence%:{self.problem.differenceToBest(bestDistance)}| tourMean: {float(distances.mean())}|tourWorst: {float(distances.max())}|tourStd: {float(distances.std())}|Similarity: {popSim}')


    def getRows(self):

         return self.rows
            