"""
Created on Thu Oct  24 11:48 2024

@author: Baptiste Guilleminot

"""


import numpy as np
import matplotlib.pyplot as plt

## Taille des cristaux

size = np.array([240., 170., 200., 45., 23., 170., 70., 70., 100., 120., 40., 180., 90., 80., 250., 180., 80., 70., 90., 230., 110., 90., 180., 50., 100., 150., 30., 40., 50., 30., 60.])

size *= (0.00012 / 3200.0)

area = size * size

X = np.linspace(min(area), max(area), int((max(area) - min(area)) // 1e-13))
Y = np.zeros(int((max(area) - min(area)) // 1e-13))

for a in area :
    Y[int((a-min(area)) // 1e-13) - 2] += 1

Y /= len(size) #normalisation


## Affichage
plt.scatter(X,Y)
plt.scatter(Xmod, Ymod[0:len(Xmod)])
plt.xlabel('Surface cristaux en m')
plt.ylabel('Nb Cristaux')
plt.title('Distribution de la taille des cristaux')
plt.show()


