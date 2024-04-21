import pandas as pd
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
np.set_printoptions(threshold=sys.maxsize)
'''
for Q2(i) where all are susptible to infection choose p1=0.001, p2=0.99, p3=0.99 
Q2(ii) where all are in equilibrium choose p1, p2, p3 = 0.5
Q2(iii) where there are cyclic infections p1=0.95, p2=0.1 p3=0.01 use plot_freq = 5000
'''
if(len(sys.argv) != 3): # = num argv[n+1]
    print("type after file name these params: N")
    sys.exit()

''' either type 'avgi' or 'vari' after N, p1, p2, p3'''
N, ifrac = int(sys.argv[1]), float(sys.argv[2])

nstep = 10100  # evergy n step there is 1 sweep
n2 = N*N
plot_freq = 300
sweeps = 10000

r = np.random.random(sweeps*n2)
ij = np.random.randint(0, N, sweeps*n2*2)

p1, p2, p3 = 0.8, 0.1, 0.02


def iterating(state, immfrac):
    vals, labels = [0, 1, 2], ['S', 'I', 'R']
    ilist = []
    idx = np.random.choice(n2, size=int(immfrac*n2), replace=False)  # replace makes no 2 the same
    out = np.column_stack((np.unravel_index(idx,(50,50))))  # turns into the 2D of shape (50, 50)

    for n in range(sweeps*n2): # sweeps = 1,000
        if n%n2 == 0:
            ilist.append(np.count_nonzero(state==1))
        i, j = ij[n*2], ij[n*2+1]
        neibs = np.count_nonzero(state[[i,i,(i+1)%N,(i-1)%N], [(j+1)%N,(j-1)%N,j,j]] == 1) # countingIneibhors

        if (state[i][j] == 0) and (neibs != 0) and (r[n] < p1):
            coord_set = map(tuple, [[i, j]]) # using sets to check if its immune
            immune_set = map(tuple, out)
            if_immune = set(coord_set).intersection(immune_set)
            if len(if_immune) == 0:
                state[i][j] = 1 # make infected
            # if [i, j] not in out:
            #     state[i][j] = 1 # make infected
        elif (state[i][j] == 1) and r[n] < p2:
            state[i][j] = 2 # make recovered
        elif (state[i][j] == 2) and r[n] < p3:
            state[i][j] = 0 # make susptible

        if (n > n2*100) and (ilist[-1] == 0): 
            if len(ilist) < sweeps-1:
                ilist = np.concatenate((ilist, np.zeros(sweeps-1-len(ilist))))
            break  # n2*100 because its till eqilibrium time

        # if(n%(plot_freq) == 0):
        #     plt.cla()
        #     im = plt.imshow(state)
        #     # put those patched as legend-handles into the legend
        #     # get the colors of the values, according to the 
        #     # colormap used by imshow
        #     colors = [ im.cmap(im.norm(value)) for value in vals]
        #     # create a patch (proxy artist) for every color 
        #     patches = [ mpatches.Patch(color=colors[i], label=labels[i] ) for i in range(len(vals)) ]
        #     plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
        #     plt.draw()
        #     plt.pause(0.001)
    return ilist # list of # of I states with each iteration


'for repeating rand evolution for the hist uncomment everything out below'
def immune_fractions():
    q5 = {'immfrac':[], 'avgi':[]} 
    for imm_frac in np.arange(0, 1.05, 0.05):
        start = time.time()
        print('immune fraction = ', imm_frac)
        ilist = iterating(np.random.choice([0, 1, 2], (N, N)), imm_frac)
        q5['immfrac'].append(imm_frac)
        q5['avgi'].append(np.mean(ilist)/n2) # avg infeacted frac in sim
        print(f'time taken =', start-time.time())

    fig, ax = plt.subplots()
    ax.scatter(q5['immfrac'], q5['avgi'])
    ax.set_title('The average number infected with the fraction immune')
    ax.set_xlabel(r'fraction immune')
    ax.set_ylabel(r'Average fraction infected')
    plt.savefig('immunity-fraction.png', dpi=300)
    plt.show()
    pd.DataFrame(q5).to_csv('contourQ5data.csv') 


'''Comment out iterating() when you want the animation (also remember to comment out the animations)'''
# iterating(np.random.choice([0, 1, 2], (N, N)), ifrac)
'''comment out these funtions for the plots that vary p1 and p3 depending if you want 
a plot of the variance of the infectious squares or a contour plot of the average number of infections
with varying p1 and p3'''
immune_fractions()


