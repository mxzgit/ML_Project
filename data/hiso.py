import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

#x = np.array(pickle.load(open('test_labels.data', 'rb')))
x = np.genfromtxt('reduced_train_label.txt', dtype='uint8')

plt.hist(x)#, bins=20)
plt.ylabel('No of times')
plt.show()



