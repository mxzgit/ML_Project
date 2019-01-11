import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


fig = plt.figure()
axs = fig.add_subplot(111)
axs.xaxis.set_major_locator(MaxNLocator(integer=True))
axs.set_xlabel('k')
axs.set_ylabel('accuracy')

D0 = np.genfromtxt('accuracy_reduced_GANs.csv',\
    delimiter=',', names=['k', 'accuracy'])

D1 = np.genfromtxt('accuracy_GAN_no_reduce.csv',\
    delimiter=',', names=['k', 'accuracy'])


axs.plot(D0['k'], D0['accuracy'], color='r', label='GANs reduced')
axs.plot(D1['k'], D1['accuracy'], color='b', label='GANs No reduce')

axs.axvline(x=8, color='k', linestyle='dashed')
axs.text(8.1, 0.935, 'k=8')

axs.axvline(x=7, color='k', linestyle='dashed')
axs.text(5.7, 0.935, 'k=7')

axs.legend()
plt.show()
