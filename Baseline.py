import numpy as np
import random
#distance vector is the array of all the cities and co
def nearestNeighbour(distancematrix,startIndex):


    numCities=len(distancematrix)

    visited=np.zeros(numCities,dtype=bool)
    currentCityIndex=startIndex
    visited[startIndex]=True #visit first city
    distanceCount=0

    touringRoute=[currentCityIndex] #start at the current city
    for x in range(numCities-1):
        dMatCopy=distancematrix[currentCityIndex].copy() # retrieve vector of distances to all other cities from current city
        dMatCopy[visited]=np.inf # where visited is true set the distance to infity so can never chose that city to be visited again

        nextCity=int(np.argmin(dMatCopy)) #get index of next city to visit
        touringRoute.append(nextCity) #get order of visitation 
        
        distanceCount+=dMatCopy[nextCity] #add up with the distance of the next city
        visited[nextCity]=True #set city as visited

        currentCityIndex=nextCity #update the current city

    #dont forget the last city
    distanceCount+=distancematrix[currentCityIndex][startIndex] 
    return np.array(touringRoute),distanceCount


def randomSerach(distanceMatrix,rng):

    numCities=len(distanceMatrix)

    tour=rng.permutation(numCities)
    distanceCount=0

    for x in range(numCities-1):
        currentCity=tour[x]
        nextCity=tour[(x+1)%numCities]
        distanceCount+=distanceMatrix[currentCity][nextCity] 
    return tour,distanceCount


def computeDistance(tour,distanceMatrix):
    total = 0

    for i in range(len(tour)):

        #add the cost to travel from last city back to first
        if i+1==len(tour):
            current=tour[i]
            nextCity=tour[0]

            total += distanceMatrix[current][nextCity]
            return total

        current = tour[i]
        nextCity = tour[i+1]

        total += distanceMatrix[current][nextCity]

    return total

def twoOpt(distanceMatrix,rng):
    
    numCities=len(distanceMatrix)
    tour=rng.permutation(numCities)


    improved=True

    while improved:
        improved=False
        for i in range(1,numCities-1):
            for j in range(i+1,numCities):  

                newTour=tour.copy()
                # take the two points and reverse the arrangement between the two

                newTour[i:j]=newTour[i:j][::-1] #step -1 means go backwards 

                if computeDistance(newTour,distanceMatrix)<computeDistance(tour,distanceMatrix):
                    tour=newTour
                    improved=True
    return tour,computeDistance(tour,distanceMatrix)