#
# reduce the number of examples using Condensed nearest neighbors
#

import pickle
import numpy as np
import sys

if __name__ == "__main__":
	
	
	y = pickle.load(open("data/test_code_filtered.data", "rb"))
	#y = np.array(y)
	
	#for x in X:
	#    for i in x:
	#        print(i,end='')
	#    print()
	f = open('test_code_filtered.txt','w')
	for x in y:
		for i in x:
			f.write(str(i))
		#f.write(str(x)+'\n')
		f.write('\n')
	
