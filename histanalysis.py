from filter import Filter

def analyze(filter):
    sink = filter()
    
    #from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.axes, see
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    from matplotlib.ticker import NullFormatter
    
    
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
    
    x,y = X,Y
    
    nullfmt   = NullFormatter()         # no labels

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left+width+0.02
    
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]
    
    # start with a rectangular Figure
    plt.figure(1, figsize=(8,8))
    
    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    
    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)
    
    # the scatter plot:
    axScatter.scatter(x, y, marker = 's', color=colors, s = ((Z-Z_min+Z_min/Z_range)*Z_scale)**2*200)# color = [['r','b','y'][random.randint(0,2)] for i in range(len(sink))])
    
    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
    lim = ( int(xymax/binwidth) + 1) * binwidth
    
    axScatter.set_xlim( (0, lim) )
    axScatter.set_ylim( (0, lim) )
    
    bins = np.arange(-lim, lim + binwidth, binwidth)
    axHistx.hist(x, bins=bins)
    axHisty.hist(y, bins=bins, orientation='horizontal')
    
    axHistx.set_xlim( axScatter.get_xlim() )
    axHisty.set_ylim( axScatter.get_ylim() )

    
    ax.set_xlabel('Latitudinal Offset')
    ax.set_ylabel('Longitudinal Offset')
    
    return plt

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Usage: histanalysis.py <file> <street1> <street2> <street3> ..."
        sys.exit(1)
    plt = analyze(Filter(*sys.argv[1:]))
    plt.savefig("results/data.hist."+(".".join(sys.argv[2:])).replace(" ","_")+".png")
    print "0"