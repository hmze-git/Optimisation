import numpy as np

class Operator:

    def __init__(self,rng):
        self.rng=rng# used to generate seeded random values for reporduce ability

        

    def cutPoints(self,numCities):

        p1,p2=self.rng.choice(numCities,size=2,replace=False)
        arrTemp=[p1,p2]
        arrTemp=sorted(arrTemp)
        return int(arrTemp[0]),int(arrTemp[1])        

    def orderCrossOver(self,parent1,parent2):
        numCities=len(parent1)

        #find indicies that define the window to pass from p1 to the child
        a,b=self.cutPoints(numCities)

        child=parent2.copy()

        visted=np.zeros(numCities,dtype=bool) #this is like a true false map telling you which cities have been visted already
        visted[parent1[a:b+1]]=True # start at the beginning of slice end at the end of it and mark those postions as visited

        child[a:b+1]=parent1[a: b+1]


        childIndex=(b+1)%numCities
        parentIndex=(b+1)%numCities

        for _ in range(numCities):

            city=parent2[parentIndex]
            if not visted[city]:
                child[childIndex]=city
                visted[city]=True

                childIndex=(childIndex+1)%numCities
            
            parentIndex=(parentIndex+1)%numCities
        return child

    def swapMutation(self,tour): #randomly swap two cities
        torucCopy=tour.copy()
        numCities=len(tour)
        i,j=self.rng.choice(numCities,size=2,replace=False)


        torucCopy[i],torucCopy[j]=torucCopy[j],torucCopy[i] #swap the two points

        return torucCopy

    def inversionMutation(self,tour):
        torucCopy=tour.copy()
        numCities=len(tour)

        p1,p2=self.cutPoints(numCities)

        torucCopy[p1:p2+1]=torucCopy[p1:p2+1][::-1].copy()  #same logic as two opt but instead reverse the points selected

        return torucCopy