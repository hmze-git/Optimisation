import numpy as np

class TspWorld:

    def __init__(self,path,optimum):

        self.optimal=optimum


        cordninates=[]

        with open(path) as fl:
            cordinateSection=False

            for line in fl:
                line=line.strip() #remove white spaces

                if line.startswith('NODE_COORD_SECTION'):
                    cordinateSection=True

                elif line.startswith('EOF'):
                    break
                elif cordinateSection:
                    parts=line.split() #split on spaces get 3 values the city #,xCord,yCord
                    cordninates.append((float(parts[1]),float(parts[2])))


        self.cordinates=cordninates #store city coordinate tuples 
        self.numCities=len(cordninates)
        
        #Compute the distances between all cities in advance so no need to compute at eval time

        self.distanceMatrix=np.zeros((self.numCities,self.numCities))

        for r in range(self.numCities):
            for c in range(self.numCities):
                x1,y1=self.cordinates[r]
                x2,y2=self.cordinates[c]

                distance=np.floor(np.sqrt((x1-x2)**2+(y1-y2)**2))

                self.distanceMatrix[r][c]=distance
    
    def computePopLen(self,population):
        length=[]

        for tour in population:
            distance=0

            for i in range(len(tour)):
                currCity=tour[i]
                nextCity=tour[(i+1)%len(tour)] #wrap around to first city logic included here

                distance+=self.distanceMatrix[currCity][nextCity]
            length.append(distance)


        return np.array(length)