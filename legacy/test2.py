from filter import Filter

filter = Filter("77005.csv", "University Blvd", "Kirby Dr", "Bissonnet St", "Buffalo Speedway")
sink = filter()

print sink

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = axes3d.Axes3D(fig)
#X = np.arange(-5, 5, 1)
#
#Y = np.arange(-5, 5, 1)
#
#X, Y = np.meshgrid(X, Y)
#print X
#print Y
#R = np.sqrt(X)
#Z = 2*X
#print Z
#ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
#
#plt.show()

#print X,Y,Z

X = []
Y = []
Z_ = []
for k in sink:
    X += [k[0][0]]
    Y += [k[0][1]]
    Z_ += [k[1]]

X = np.array(X)
Y = np.array(Y)

X,Y = np.meshgrid(X, Y)

Z = []

for xx in range(len(X)):
    z_ = []
    for yy in range(len(Y)):
        done = False
        x = X[xx][yy]
        y = Y[xx][yy] 
        for k in sink:
            #print x
            if k[0][0] == x and k[0][1] == y:
                z_ += [k[1]]
                done = True
        if not done:
            z_ += [0]
    Z += [z_]
Z = np.array(Z)
#print Z
from matplotlib import cm
#ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
cset = ax.contour(X, Y, Z)
ax.clabel(cset, fontsize=9, inline=1)

plt.show()