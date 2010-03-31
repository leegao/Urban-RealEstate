from filter import Filter

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
    
    Z_min = min(Z)
    Z_range = max(Z)-min(Z)
    Z_scale = 1.0/Z_range
    
    colors = []
    for i in range(len(sink)):
        X[i] = (X[i]-X_min)*110.83575 #* X_scale
        Y[i] = (Y[i]-Y_min)*97.43888 #* Y_scale
        colors.append(tuple([0.2,0.1]+[1-Z[i]/max(Z)]*1+[1]))
    
    z = zip(*filter.coords)
    coords = zip( (np.array(z[0])-X_min)*110.83575, (np.array(z[1])-Y_min)*97.43888)

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    
    from numpy.random import uniform
    # make up some randomly distributed data
    npts = 200
    #X = uniform(-2,2,npts)
    #Y = uniform(-2,2,npts)
    #Z = X*Y
    #print X
    #print Y
    xi = np.linspace(X.min(),X.max(),100)
    yi = np.linspace(Y.min(),Y.max(),100)
    zi = griddata(X,Y,Z,xi,yi)
    
    CS = plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
    CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
    
    plt.colorbar()
    #print ((Z-Z_min+Z_min/Z_range)*Z_scale)**2*200
    plt.scatter(X, Y, marker = 's', color=colors, s = ((Z-Z_min+Z_min/Z_range)*Z_scale)**2*200)# color = [['r','b','y'][random.randint(0,2)] for i in range(len(sink))])
    plt.scatter(*zip(*coords), marker = '+')
#    
    for i in range(len(filter.intersections)):
        plt.text(coords[i][0], coords[i][1], filter.intersections[i].replace(", Houston TX", "").replace("and", "\n"), fontsize=8, alpha = 0.5)
    #print ((Z-Z_min)*Z_scale)**4*15
#    print dir(plt)
#    plt.set_xlabel('Latitudinal Offset')
#    plt.set_ylabel('Longitudinal Offset')
    x,y = zip(*coords)
    x = np.array(x)
    y = np.array(y)
    plt.xlim(x.min(),x.max())
    plt.ylim(y.min(),y.max())
    return plt

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Usage: contouranalysis.py <file> <street1> <street2> <street3> ..."
        sys.exit(1)
    plt = analyze(Filter(*sys.argv[1:]))
    #plt.show()
    plt.savefig("results/data.contour."+(".".join(sys.argv[2:])).replace(" ","_")+".png")
    print "0"