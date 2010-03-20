from filter import Filter

def analyze(filter):
    sink = filter()
    #from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.axes
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    
    
    fig = plt.figure()
    ax=fig.add_subplot(111)
    
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
    
    ax.scatter(X, Y, marker = 's', color=colors, s = ((Z-Z_min)*Z_scale)**4*15)# color = [['r','b','y'][random.randint(0,2)] for i in range(len(sink))])
    ax.scatter(*zip(*coords), marker = '+')
    
    for i in range(len(filter.intersections)):
        ax.text(coords[i][0], coords[i][1], filter.intersections[i].replace(", Houston TX", "").replace("and", "\n"), fontsize=8, alpha = 0.5)
    #print ((Z-Z_min)*Z_scale)**4*15
    ax.set_xlabel('Latitudinal Offset')
    ax.set_ylabel('Longitudinal Offset')
    
    return plt

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Usage: analyze.py <file> <street1> <street2> <street3> ..."
        sys.exit(1)
    plt = analyze(Filter(*sys.argv[1:]))
    plt.savefig("results/data.marked."+(".".join(sys.argv[2:])).replace(" ","_")+".png")
    print "0"