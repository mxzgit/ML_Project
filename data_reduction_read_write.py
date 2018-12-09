#
# reduce the number of examples using Condensed nearest neighbors
#

import pickle
import numpy as np
from dp_rolling import dp_rolling_ed
from timeit import default_timer as timer
import sys

if __name__ == "__main__":
    #X = pickle.load(open("train_code_scaled_half.data", "rb"))
    #X = np.array(X)
    
    y = pickle.load(open("train_labels.data", "rb"))
    #y = np.array(y)
    
    #for x in X:
    #    for i in x:
    #        print(i,end='')
    #    print()

    for x in y:
        print(x)
	
	