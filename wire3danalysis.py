from filter import Filter

def analyze(filter):
    sink = filter()
    
    from mpl_toolkits.mplot3d import axes3d
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    
    
    fig = plt.figure()
    ax = axes3d.Axes3D(fig)
    
    X = []
    Y = []
    Z_ = []
    for k in sink:
        X += [k[0][0]]
        Y += [k[0][1]]
        Z_ += [k[1]]
    
    X_min = min(X)
    X_range = max(X)-min(X)
    X_scale = 20.0/X_range
    
    Y_min = min(Y)
    Y_range = max(Y)-min(Y)
    Y_scale = 20.0/Y_range
    
    
    colors = []
    for i in range(len(sink)):
        X[i] = (X[i]-X_min)*110.83575 #* X_scale
        Y[i] = (Y[i]-Y_min)*97.43888 #* Y_scale
        colors.append(tuple([0.2,0.1]+[1-Z_[i]/max(Z_)]*1+[1]))
    
    z = zip(*filter.coords)
    coords = zip( (np.array(z[0])-X_min)*110.83575, (np.array(z[1])-Y_min)*97.43888)

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
                if x == (k[0][0]-X_min)*110.83575 and y == (k[0][1]-Y_min)*97.43888:
                    z_ += [k[1]]
                    done = True
            if not done:
                z_ += [0]
        Z += [z_]
    Z = np.array(Z)
    ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
    ax.set_xlabel('Latitudinal Offset')
    ax.set_ylabel('Longitudinal Offset')
    ax.set_zlabel('Price')
    return plt

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Usage: wire3danalysis.py <file> <street1> <street2> <street3> ..."
        sys.exit(1)
    plt = analyze(Filter(*sys.argv[1:]))
    plt.savefig("results/data.wire3d."+(".".join(sys.argv[2:])).replace(" ","_")+".png")
    print "0"