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
    Z_scale = 255.0/Z_range
    
    colors = []
    for i in range(len(sink)):
        X[i] = (X[i]-X_min) * X_scale
        Y[i] = (Y[i]-Y_min) * Y_scale
        colors.append(tuple([0.3,0.1]+[1-Z[i]/max(Z)]*1+[1]))

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    ax.scatter(X, Y, Z, marker = '+')# color = [['r','b','y'][random.randint(0,2)] for i in range(len(sink))])

    ax.set_xlabel('Latitudinal Offset')
    ax.set_ylabel('Longitudinal Offset')
    ax.set_zlabel('Price')
    return plt

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Usage: scatter3danalysis.py <file> <street1> <street2> <street3> ..."
        sys.exit(1)
    plt = analyze(Filter(*sys.argv[1:]))
    plt.savefig("results/data.scatter3d."+(".".join(sys.argv[2:])).replace(" ","_")+".png")
    print "0"