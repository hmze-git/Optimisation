import json
import numpy as np

import matplotlib.pyplot as plt



def pltoSeeds(runs,dictKey,title,fileName,xKey='gen'):

    plt.figure()

    for seed in runs:
        print(seed)
        seededRunDict=runs[seed]
        x=[r[xKey] for r in seededRunDict]
        y=[r[dictKey] for r in seededRunDict]

        plt.plot(x,y,label='seed'+seed)

    plt.xlabel(xKey)
    plt.ylabel(dictKey)
    plt.title(title)
    plt.legend()
    plt.savefig(fileName)
    plt.close()