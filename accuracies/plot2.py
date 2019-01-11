import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


fig = plt.figure()
axs = fig.add_subplot(111)
axs.xaxis.set_major_locator(MaxNLocator(integer=True))
axs.set_xlabel('k')
axs.set_ylabel('accuracy')

D0 = np.genfromtxt('deep_learning_acc.csv',\
    delimiter=',', names=['k', 'accuracy'])

D1 = np.genfromtxt('deep_learning_acc2.csv',\
    delimiter=',', names=['k', 'accuracy'])


axs.plot(D0['k'], D0['accuracy'], color='r', label='original data')
axs.plot(D1['k'], D1['accuracy'], color='b', label='LMNN transformed data')

axs.axvline(x=7, color='k', linestyle='dashed')
axs.text(7.1, 0.968, 'k=7')

axs.legend()
plt.show()
