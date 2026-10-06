class Logger:

    def __init__(self,tspProblem,logWhen=100,solutionType='GA'):
        
        self.problem=tspProblem
        self.logWhen=logWhen
        self.solutionType=solutionType
        self.rows=[]

    #diversity in the population so determine how many edges are shared to see if GA is convergin
    #or not 
    #fix Later
    def edgeEncoding(self,population)  