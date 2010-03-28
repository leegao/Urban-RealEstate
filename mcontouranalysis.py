from filter import CoordFilter
from geocode import get_box

def analyze(filter):
    sink = filter()
    #from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.mlab import griddata
    import numpy.ma as ma
    import matplotlib.axes
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    
    
#    fig = plt.figure()
#    ax=fig.add_subplot(111)
    #print filter.coords
    X = []
    Y = []
    Z = []
    for k in sink:
        X += [k[0][1]]
        Y += [k[0][0]]
        Z += [k[1]]

    X_min = min(X)
    X_range = max(X)-min(X)
    X_scale = 20.0/X_range
    
    Y_min = min(Y)
    Y_range = max(Y)-min(Y)
    Y_scale = 20.0/Y_range
    
    Z_min = min(Z)
    Z_range = max(Z)-min(Z)
    Z_scale = 1.0/Z_range
    
#    print min(X), max(X), min(Y), max(Y)
    
    colors = []
    for i in range(len(sink)):
        X[i] = (X[i]-X_min)*110.83575 #* X_scale
        Y[i] = (Y[i]-Y_min)*97.43888 #* Y_scale
        #colors.append(plt.cm.jet(Z[i]))#tuple([0.6,0.1]+[1-Z[i]/max(Z)]*1+[1]))
    
    z = zip(*filter.coords)
    coords = zip( (np.array(z[0])-X_min)*110.83575, (np.array(z[1])-Y_min)*97.43888)

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    
    xi = np.linspace(X.min(),X.max(),100)
    yi = np.linspace(Y.min(),Y.max(),100)
    zi = griddata(X,Y,Z,xi,yi)
    
    CS = plt.contour(xi,yi,zi,5,linewidths=0.1,colors='w')
    CS = plt.contourf(xi,yi,zi,50,cmap=plt.cm.jet)
    
    plt.colorbar()
    #print ((Z-Z_min+Z_min/Z_range)*Z_scale)**2*200
    #plt.scatter(X, Y, marker = 's',s=0.1)# s = ((Z-Z_min+Z_min/Z_range)*Z_scale)*100)# color = [['r','b','y'][random.randint(0,2)] for i in range(len(sink))])
    #plt.scatter(*zip(*coords), marker = '+')
#    
    #for i in range(len(filter.intersections)):
    #    plt.text(coords[i][0], coords[i][1], filter.intersections[i].replace(", Houston TX", "").replace("and", "\n"), fontsize=8, alpha = 0.5)
    #print ((Z-Z_min)*Z_scale)**4*15
    #print dir(plt)
    plt.title("Distribution of Housing Price in "+sys.argv[2])
    plt.xlabel('Longitudinal Offset in Miles (W>E)', fontsize=8, alpha = 0.5)
    plt.ylabel('Latitudinal Offset in Miles (S>N)', fontsize=8, alpha = 0.5)
    x,y = zip(*coords)
    x = np.array(x)
    y = np.array(y)
    plt.xlim(X.min(),X.max())
    plt.ylim(Y.min(),Y.max())
    return plt

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Usage: mcontouranalysis.py <file> <street1> <street2> <street3> ..."
        sys.exit(1)
    plt = analyze(CoordFilter(sys.argv[1], *get_box(sys.argv[2])))
    #plt.show()
    plt.savefig("results/data.mcontour."+(".".join(sys.argv[2:])).replace(" ","_")+".png")
    print "0"