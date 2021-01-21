import networkx as nx
import matplotlib.pyplot as plt
import graphistry
from pylab import *
import pandas as pd
from constant import *

class AnnoteFinder:  # thanks to http://www.scipy.org/Cookbook/Matplotlib/Interactive_Plotting
    """
    callback for matplotlib to visit a node (display an annotation) when points are clicked on.  The
    point which is closest to the click and within xtol and ytol is identified.
    """
    def __init__(self, xdata, ydata, annotes, axis=None, xtol=None, ytol=None):
        self.data = list(zip(xdata, ydata, annotes))
        if xtol is None: xtol = ((max(xdata) - min(xdata))/float(len(xdata)))/2
        if ytol is None: ytol = ((max(ydata) - min(ydata))/float(len(ydata)))/2
        self.xtol = xtol
        self.ytol = ytol
        if axis is None: axis = gca()
        self.axis= axis
        self.drawnAnnotations = {}
        self.links = []

    def __call__(self, event):
        if event.inaxes:
            clickX = event.xdata
            clickY = event.ydata
            #print(dir(event),event.key)
            if self.axis is None or self.axis==event.inaxes:
                annotes = []
                smallest_x_dist = float('inf')
                smallest_y_dist = float('inf')

                for x,y,a in self.data:
                    print(clickX, x, clickY, y);
                    if abs(clickX-x) <= RADIUS and abs(clickY-y) <= RADIUS:
                        dx, dy = x - clickX, y - clickY
                        annotes.append((dx*dx+dy*dy,x,y, a))
                        self.drawAnnote(event.inaxes, x, y, a)
    def drawAnnote(self, axis, x, y, annote):
        result = [1, 2, 3];
        fig1, ax1 = plt.subplots()
        ax1.plot(np.arange(3), result);
        plt.show();


df = pd.read_csv("edges.csv") #DataFrame("edges.csv")

# Build your graph
# G = nx.from_pandas_edgelist(df, 'from', 'to')
G = nx.Graph()
G.add_edge(1,2,weight=0.5)
G.add_edge(1,3,weight=9.8)
pos=nx.spring_layout(G)
nx.draw_networkx(G,pos)
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
x, y, annotes = [], [], []
for key in pos:
    d = pos[key]
    annotes.append(key)
    x.append(d[0])
    y.append(d[1])




af = AnnoteFinder(x, y, annotes)
connect('button_press_event', af)

show()
