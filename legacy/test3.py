from filter import Filter

filter = Filter("77005.csv", "Bellaire Blvd", "Stella Link Rd", "Weslayan St", "Bissonnet St", "Community Dr")
sink = filter()

print sink

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.axes, see
import matplotlib.pyplot as plt
import numpy as np
import random



fig = plt.figure()
ax = Axes3D(fig)

X = []
Y = []
Z = []
for k in sink:
    X += [k[0][0]]
    Y += [k[0][1]]
    Z += [k[1]]

X_min = min(X)
X_range = max(X)-min(X)
X_scale = 20.0/X_range

Y_min = min(Y)
Y_range = max(Y)-min(Y)
Y_scale = 20.0/Y_range

Z_min = min(Y)
Z_range = max(Z)-min(Z)
Z_scale = 255.0/Z_range

colors = []
for i in range(len(sink)):
    X[i] = (X[i]-X_min) * X_scale
    Y[i] = (Y[i]-Y_min) * Y_scale
    colors.append(tuple([Z[i]/max(Z)]+[0,0.9,1]))
print colors
X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)
ax.scatter(X, Y, Z, marker = '+', color=colors, s = np.array(colors)*100)# color = [['r','b','y'][random.randint(0,2)] for i in range(len(sink))])

ax.set_xlabel('Latitudinal Offset')
ax.set_ylabel('Longitudinal Offset')
ax.set_zlabel('Price')

plt.show()