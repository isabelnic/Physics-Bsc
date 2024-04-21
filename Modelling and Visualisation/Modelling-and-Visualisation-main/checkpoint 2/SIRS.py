import pandas as pd
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import bootstrap
import csv
np.set_printoptions(threshold=sys.maxsize)
'''
for Q2(i) where all are susptible to infection choose p1=0.001, p2=0.99, p3=0.99 
Q2(ii) where all are in equilibrium choose p1, p2, p3 = 0.5
Q2(iii) where there are cyclic infections p1=0.95, p2=0.1 p3=0.01 use plot_freq = 5000
'''
if(len(sys.argv) != 6):
    print("type after file name these params: N, p1, p2, p3, optional ['avgi', 'vari']")
    sys.exit()

''' either type 'avgi' or 'vari' after N, p1, p2, p3'''
N, prob1, prob2, prob3 = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
plot_type = str(sys.argv[5])

n2 = N*N
plot_freq = 5000
sweeps = 10000

r = np.random.random(sweeps*n2)
ij = np.random.randint(0, N, sweeps*n2*2)


def iterating(state, sweep, p1, p2, p3):
    vals, labels = [0, 1, 2], ['S', 'I', 'R']
    ilist = []
    for n in range(sweeps*n2): # sweeps = 10,000
        # list of neighbors below
        i, j = ij[n*2], ij[n*2+1]
        # counting neibhors that are infected below
        neibs = np.count_nonzero(state[[i,i,(i+1)%N,(i-1)%N], [(j+1)%N,(j-1)%N,j,j]] == 1)
        if (state[i][j] == 0) and (neibs > 0) and (r[n] < p1):
            state[i][j] = 1 # make infected
        elif (state[i][j] == 1) and r[n] < p2:
            state[i][j] = 2 # make recovered
        elif (state[i][j] == 2) and r[n] < p3:
            state[i][j] = 0 # make susptible
        
        if (n >= n2) and (n%n2) == 0:
            ilist.append(np.count_nonzero(state==1))

        if (n > n2*100) and (ilist[-1] == 0): 
            if len(ilist) < sweeps-1:
                ilist = np.concatenate((ilist, np.zeros(sweeps-1-len(ilist))))
            break  # n2*100 because its till eqilibrium time


        if(n%(plot_freq) == 0):
            plt.cla()
            im = plt.imshow(state)
            # put those patched as legend-handles into the legend
            # get the colors of the values, according to the 
            # colormap used by imshow
            colors = [ im.cmap(im.norm(value)) for value in vals]
            # create a patch (proxy artist) for every color 
            patches = [ mpatches.Patch(color=colors[i], label=labels[i] ) for i in range(len(vals)) ]
            plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
            plt.draw()
            plt.pause(0.001)
    return ilist # list of # of I states with each iteration


'for repeating rand evolution for the hist uncomment everything out below'
def rand_evolution():
    if plot_type == 'avgi':
        print('plotting contour plot of mean I / N')
        q3 = {'p1':[], 'p3':[], 'avgi/N': [], 'vari':[]}
        for varp1 in np.arange(0, 1.05, 0.05):
            print('_______________p1 =  ', varp1)
            for varp3 in np.arange(0, 1.05, 0.05):
                print('p2=', varp3)
                ilist = iterating(np.random.choice([0, 1, 2], (N, N)), sweeps, varp1, 0.5, varp3)
                vari = (np.mean(np.square(ilist)) - (np.mean(ilist))**2)/n2
                print('variance =', vari)
                print('average =', np.mean(ilist)/n2)
                q3['vari'].append(vari) 
                q3['avgi/N'].append(np.mean(ilist)/n2)
                q3['p1'].append(varp1)
                q3['p3'].append(varp3)
        pd.DataFrame(q3).to_csv('contourQ3data.csv') 

    elif plot_type == 'vari':
        q4 = {'p1':[], 'vari':[], 'std':[]} 
        for varp1 in np.arange(0.2, 0.502, 0.02):
            print('p1 = ', varp1)
            ilist = iterating(np.random.choice([0, 1, 2], (N, N)), sweeps, varp1, 0.5, 0.5)
            vari = (np.mean(np.square(ilist)) - (np.mean(ilist))**2)/n2
            error = bootstrap((ilist,), statistic=np.var, method='basic').standard_error/n2
            q4['vari'].append(vari)
            q4['p1'].append(varp1)
            q4['std'].append(error)
        pd.DataFrame(q4).to_csv('contourQ4data.csv') 


def plot_contour():
    if plot_type == 'avgi':
        df = pd.read_csv('contourQ3data.csv')
        Z = df.pivot_table(index='p1', columns='p3', values='avgi/N').T.values
        X_unique = np.sort(df.p1.unique())
        Y_unique = np.sort(df.p3.unique())
        X, Y = np.meshgrid(X_unique, Y_unique)

        fig, ax = plt.subplots()
        CS = ax.contourf(X, Y, Z, cmap='RdGy')
        ax.set_title('Contour plot of the behavour of avg I')
        ax.set_xlabel('p1')
        ax.set_ylabel('p3')
        ax.set_aspect('equal')
        fig.colorbar(CS, format="%.2f")
        plt.savefig('contour-plot-of-avgi.png', dpi=300)
        plt.show()
    elif plot_type == 'vari':
        df = pd.read_csv('contourQ4data.csv')
        fig, ax = plt.subplots()
        ax.errorbar(df['p1'], df['vari'], yerr=df['std']) # standard deviation
        ax.scatter(df['p1'], df['vari'])
        ax.set_title('Cut plot of the variance across p1 (p2=p3=0.5)')
        ax.set_xlabel('p1')
        ax.set_xlim(left=0.2, right=0.6)
        ax.set_ylabel('varience')
        plt.savefig('cut-plot-of-vari.png', dpi=300)
        plt.show()
    return


'''Comment out iterating() when you want the animation (also remember to comment out the animations)'''
iterating(np.random.choice([0, 1, 2], (N, N)), sweeps, prob1, prob2, prob3)
'''comment out these funtions for the plots that vary p1 and p3 depending if you want 
a plot of the variance of the infectious squares or a contour plot of the average number of infections
with varying p1 and p3'''
# rand_evolution()
# plot_contour()

'''to check individual values of p1, p2 and p3 to see if they are right'''
# list = iterating(np.random.choice([0, 1, 2], (N, N)), 0.8, 0.5, 0.8)
# avgioN = np.mean(list)/n2
# var = (np.mean(np.square(list)) - (np.mean(list))**2)/n2
# std = np.sqrt(var)
# print(avgioN)

