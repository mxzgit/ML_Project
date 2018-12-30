import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


fig = plt.figure()
axs = fig.add_subplot(111)
axs.xaxis.set_major_locator(MaxNLocator(integer=True))
axs.set_xlabel('k')
axs.set_ylabel('accuracy')

D0 = np.genfromtxt('accuracy_noscale_noreduce.csv',\
    delimiter=',', names=['k', 'accuracy'])

D1 = np.genfromtxt('accuracy_reduced.csv',\
    delimiter=',', names=['k', 'accuracy'])

D2 = np.genfromtxt('accuracy_scaled.csv',\
    delimiter=',', names=['k', 'accuracy'])

D3 = np.genfromtxt('accuracy_reduced_scaled.csv',\
    delimiter=',', names=['k', 'accuracy'])


axs.plot(D0['k'], D0['accuracy'], color='r', label='noscale noreduce')
axs.plot(D1['k'], D1['accuracy'], color='b', label='reduced')
axs.plot(D2['k'], D2['accuracy'], color='y', label='scaled')
axs.plot(D3['k'], D3['accuracy'], color='g', label='reduced scaled')

axs.axvline(x=7, color='k', linestyle='dashed')
axs.text(7.1, 0.90, 'k=7')

axs.legend()
plt.show()
