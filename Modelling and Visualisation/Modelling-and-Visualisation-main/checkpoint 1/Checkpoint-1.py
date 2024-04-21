#%% this is to run it as a Jupyter file in VS code and it represents the start/end of a cell
import matplotlib
matplotlib.use('TKAgg')
import sys
import math
import time
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.gridspec as gridspec
from scipy.stats import bootstrap
plt.style.use('ggplot')


if(len(sys.argv) != 4):
    print("type after file name these params: N T ['g' or 'k']")
    sys.exit()

nstep = 10100  # evergy n step there is 1 sweep
# J = 1 and K = 1
kT, dim, gork = float(sys.argv[2]), int(sys.argv[1]), str(sys.argv[3])  # dimation & kT(beta)
numloops = nstep*dim**2
start = time.time()
rde = np.random.randint(0, dim, numloops)
r = np.random.randint(0, dim, numloops*4)  # random number for index spin


def init(spin, T):
    if (spin == 0) and (T == 1):
        if (gork == 'g'): # all up for all down
            spin = np.ones((dim, dim))
        else: # for kawa equal # of up and down
            spin = np.ones((dim, dim))
            for i in range(25):
                for j in range(dim):
                    spin[i, j] *= -1
    else:
        spin = np.random.choice([-1, 1], (dim, dim))
    # setting up all variables and the 
    fig = plt.figure()
    plt.cla()
    plt.imshow(spin)
    plt.draw()
    return spin


def main(T, spin): # put here if they are an unput to the class
    # spin = init()
    graph_values = {'temp': [], 'mag': [], 'energy': []}
    #update loop here - for Glauber dynamics
    if gork == 'k':
        '''for Kawasaki dynamics'''
        for n in range(numloops):
            ia, ib, ja, jb = r[n*4: n*4+4] #np.random.randint(0, dim, 4)
            if ia != ib and ja != jb:  # making sure a and b coords aren't the same
                if spin[ia, ja] != spin[ja, jb]:
                    # check one spin is not eqial to the other!!!!
                    de = 2 * spin[ia, ja] * (spin[(ia + 1)%dim, ja] + 
                            spin[(ia - 1)%dim, ja] + 
                            spin[ia, (ja + 1)%dim] + 
                            spin[ia, (ja - 1)%dim]) + 2 * spin[ib, jb] * (
                            spin[(ib + 1)%dim, jb] + 
                            spin[(ib - 1)%dim, jb] + 
                            spin[ib, (jb + 1)%dim] + 
                            spin[ib, (jb - 1)%dim])
                    '''to check for the kawasaki dyneamics if two spins are nearest neibours'''
                    '''-2J new_a(2new_b)= -2J new_a*old_a where a and b are spin nearest neighbors selected
                    with: new_b = old_a & old_a = -new_a, this turns out to always be 4'''
                    if (ia == ib):
                        if ((ja == (jb+1)%50) or (ja == (jb-1)%50)):
                            de += 8 # correction term * 2 for energies of both spin a and b  
                    elif (ja == jb):
                        if ((ia == (ib+1)%50) or (ia == (ib-1)%50)):
                            de += 8
                    if (de <= 0) or (rde[n] < np.exp(- de/T)):
                        spin[ia, ja] *= -1
                        spin[ib, jb] *= -1
            
                    '''update measurements, every 10 sweeps'''
                    if(n%(10*dim**2) == 0) and (n > 100*dim**2): 
                        # show animation
                        # plt.cla()
                        # plt.imshow(spin)
                        # plt.draw()
                        # plt.pause(0.001)

                        energy = 0
                        for i in range(dim):
                            for j in range(dim):
                                ei = -1*spin[i, j]*(spin[(i+1)%50, j] + spin[i, (j+1)%50])
                                energy += ei                            
                        graph_values['temp'].append(T)
                        graph_values['mag'].append(np.abs(np.sum(spin))) # mag
                        graph_values['energy'].append(energy)

    else:
        '''for globular dyneamics'''
        for n in range(numloops):
            i, j = r[n*2:n*2+2] # np.random.randint(0, dim, 2)
            '''from evaluating the sum = 2E_initial including the -J'''
            de = 2 * spin[i, j] * (spin[(i + 1)%dim, j] + 
                            spin[(i - 1)%dim, j] + 
                            spin[i, (j + 1)%dim] + 
                            spin[i, (j - 1)%dim])
            if(de <= 0) or (rde[n] < np.exp(- de/T)):
                '''if the new state is favourable change to the new'''
                spin[i, j] *=-1
                        
            '''update measurements, every 10 sweeps'''
            # if (n%(50) == 0) and (n > 100):  # dim**2 is one sweep
            if (n%(10*dim**2) == 0) and (n > 100*dim**2):  # dim**2 is one sweep
                plt.cla()
                plt.imshow(spin)
                plt.draw()
                plt.pause(0.001)

                energy = 0
                for spi in range(dim):
                    for spj in range(dim):
                        ei = -1*spin[spi, spj]*(spin[(spi+1)%50, spj] + spin[spi, (spj+1)%50])
                        energy += ei 
                graph_values['temp'].append(T)
                graph_values['mag'].append(np.abs(np.sum(spin)))
                graph_values['energy'].append(energy)

    return graph_values, spin

main(kT, init(0, T=kT))

def calc_sup(mag, T):
    return (np.mean(np.square(mag)) - (np.mean(mag))**2)/(dim*dim*T)
def calc_hc(energy, T):
    return (np.mean(np.square(energy)) - (np.mean(energy))**2)/(dim*dim*T**2)


def runalltemps_glob(ts):
    masterdf = {'temp': [], 'mag':[], 'energy': [], 'avgHC': [], 'avgSUP': [], 'energyerr':[], 'magerr':[], 'superr':[], 'hcerr':[]}
    spin = init(0, ts[0])
    for i in ts:
        T = i
        print(f'Calculating temperature {i}')
        dict, spin = main(i, spin)
        #bootstrap of varience
        energyerr = bootstrap((dict['energy'],), np.var, confidence_level=0.90, random_state=None, method='percentile').standard_error
        magerr = bootstrap((dict['mag'],), np.var, confidence_level=0.90, random_state=None, method='percentile').standard_error
        avgenergy, avgmag = np.median(dict['energy']), np.median(dict['mag'])
        # energyerr, magerr = np.std(dict['energy']), np.std(dict['energy'])
        sup, superr = calc_sup(dict['mag'], T), magerr/(dim*dim*T)
        hc, hcerr = calc_hc(dict['energy'], T), energyerr/(dim*dim*T**2)
        masterdf['temp'].append(i)
        masterdf['energy'].append(avgenergy)
        masterdf['energyerr'].append(energyerr)
        masterdf['avgHC'].append(hc)
        masterdf['hcerr'].append(hcerr)

        if gork == 'g':
            masterdf['mag'].append(avgmag)
            masterdf['magerr'].append(magerr)
            masterdf['avgSUP'].append(sup)
            masterdf['superr'].append(superr)

        for key in masterdf:
            print(masterdf[key])
        print('supeptibily and heat cap =', sup, hc)
        print('average energy and magitisation =', avgenergy, avgmag)
        print(start-time.time())

    df = pd.DataFrame.from_dict(masterdf, orient='columns')
    df.to_csv('graph_data_'+gork+'.csv')
    print(time.time()-start)
    return df


def runalltemps_kawa(ts):
    masterdf = {'temp': [], 'energy': [], 'energyerr':[], 'avgHC': [], 'hcerr':[]}
    spin = init(0, ts[0])
    for i in ts:
        T = i
        print(f'Calculating temperature {i}')
        dict, spin = main(i, spin)
        # bootstrap of varience
        energyerr = bootstrap((dict['energy'],), np.var, confidence_level=0.90, random_state=None, method='percentile').standard_error
        avgenergy = np.median(dict['energy'])
        hc, hcerr = calc_hc(dict['energy'], T), energyerr/(dim*dim*T**2)
        masterdf['temp'].append(i)
        masterdf['energy'].append(avgenergy)
        masterdf['energyerr'].append(energyerr)
        masterdf['avgHC'].append(hc)
        masterdf['hcerr'].append(hcerr)

        print('average energy =', avgenergy)
        print('heat cap =', hc)
        print(start-time.time())

    df = pd.DataFrame.from_dict(masterdf, orient='columns')
    df.to_csv('graph_data_'+gork+'.csv')
    print(time.time()-start)
    return df


def plot(Ts):
    df = 0
    if gork == 'g':
        df = runalltemps_glob(Ts)
    else:
        df = runalltemps_kawa(Ts)
    plt.rcParams['figure.figsize'] = 13, 10
    fig = plt.figure()
    plt.suptitle(f"Graphs for {gork}")
    gs = gridspec.GridSpec(2, 2)
    axsup = fig.add_subplot(gs[0, 1]) # susepti # row, column
    axhc = fig.add_subplot(gs[0, 0]) # heat capacity
    axen = fig.add_subplot(gs[1, 0]) # energy
    axmag = fig.add_subplot(gs[1, 1]) # mag
    # plt.xlim(left=Ts[0], right=Ts[-1])

    axhc.scatter(df['temp'], df['avgHC'], label='HC')
    axen.scatter(df['temp'], df['energy'], label='energy')
    if gork == 'g':
        axsup.scatter(df['temp'], df['avgSUP'], label='SUP')
        axmag.scatter(df['temp'], df['mag'], label='mag')
    axsup.set_xlim(left=1, right=3), axhc.set_xlim(left=1, right=3)
    axen.set_xlim(left=1, right=3), axmag.set_xlim(left=1, right=3)
    axen.set_xlabel('Temperature'), axmag.set_xlabel('Temperature')
    axsup.set_ylabel('Suseptibility'), axhc.set_ylabel('Heat capacity')
    axen.set_ylabel('Energy'), axmag.set_ylabel('Magnitisation')
    plt.legend()
    plt.savefig(f'data-{gork}.png', dpi=400)

plot(np.arange(1, 3.1, 0.1))



# %%
# def delta_E_kawasaki(spin, ia, ib, ja, jb):
#     '''calculated from evaluating the sum = 2E_initial including the -J at the front'''
#     dea = 2 * spin[ia, ja] * (spin[(ia + 1)%dim, ja] + 
#                     spin[(ia - 1)%dim, ja] + 
#                     spin[ia, (ja + 1)%dim] + 
#                     spin[ia, (ja - 1)%dim])
#     deb = 2 * spin[ib, jb] * (spin[(ib + 1)%dim, jb] + 
#                     spin[(ib - 1)%dim, jb] + 
#                     spin[ib, (jb + 1)%dim] + 
#                     spin[ib, (jb - 1)%dim])
#     de = dea + deb
#     '''to check for the kawasaki dyneamics if two spins are nearest neibours'''
#     '''-2J new_a(2new_b)= -2J new_a*old_a where a and b are spin nearest neighbors selected
#     with: new_b = old_a & old_a = -new_a, this turns out to always be 4'''
#     if (ia+1)%50 == ib or (ia-1)%50 == ib or (ja+1)%50 == jb or (ja-1)%50 == jb:
#         de += 8 # correction term * 2 for energies of both spin a and b  
#     return de 


# def Kawasaki_dynamics(spin, ia, ib, ja, jb):
#     # a for position a, b for etc...
#     spin_new = [spin[ib, jb], spin[ia, ja]] # list of
#     if spin[ib, jb] != spin[ia, ja]:
#         # ia lso need to account for when spins a and b are very slide to each other
#         de = delta_E_kawasaki(spin, ia, ib, ja, jb) + delta_E_kawasaki(spin, ia, ib, ja, jb)

#         if de <= 0:
#             spin_new = [-1 * spin[ib, jb], -1 * spin[ia, ja]]
#         elif np.random.random() < np.exp(- de/T):
#             # prob = np.exp(- de/T)
#             # num = np.random.random()
#             # if num < prob:
#             spin_new = [-1 * spin[ib, jb], -1 * spin[ia, ja]]
#     return spin_new  # list of both the spins




# '''- For the measurements for Glauber and Kawasaki (i.e., to obtain quantitative plots):
# A good idea is to start from low T (ie., T=1) with the ground state. For Glauber, this is simply all spins 
# up or all down. This cuts down on initial equilibration time. Then when moving to the next temperature 
# (e.g., from T =1 to T=1.1) just use the final state from the previous temperature (i.e., do not reinitialise 
# the spin all up/all down for each temperature, for instance you can just do the initialisation out of the for 
# loop on temperature). This way 100 sweeps is always enough for equilibration, to lose memory of the initial
# configuration. For Kawasaki, have a think about the analogous of the Glauber initialisation (it is best if it
#  is again the ground state for the system).
# We suggest you have a look from the recordings at the behaviour in one point at the graph and see you get a 
# similar value before starting the longer measurement run, this way it takes a couple of minutes rather than 
# two hours! Otherwise, you can if you prefer do the whole run at a very small N (10 or 20) to see the behaviour 
# is qualitatively OK and then do the longer 50x50 run.
# It may be a good idea at some point (now or in other checkpoints), if using CPlab machines, to ssh and leave 
# a calculation running, once you are confident the code is OK. There is information on how to do this, and 
# specifically how to use ssh to log in remotely, and how to copy files to/from your computer in the wiki at 
# this page
# https://www.wiki.ed.ac.uk/pages/viewpage.action?pageId=463738783
# Please let me or the tutors know if you have issues with this.
# If you are struggling with a slow or very slow code it may well be that the visualisation is done too often. 
# This should be easy to fix (visualise every 10 sweeps or so, recall 1 sweep=2500 attempted flips). The 
# exception is when the animation is tightly entangled with the physics (as discussed a couple of times in the 
# lectures and tutorial, we suggest you try to avoid this); if this is the case, another option would be to not 
# to do the visualisation with matplotlib but gnuplot for this one (this way there is no overhead for the 
# visualisation in the code).
# - For the marking:
# you can get interactive marking from one of us in the workshop (next week if you submit then, or the 
# following one if you have an extension, we can also find another slot if these are unsuitable). If you'd like
#  to do this, it is important you still please submit to learn by the deadline (4 pm on Friday 10 Feb, or at 
#  your extension deadline), we will not look at the code/datafiles again if marked interactively but this is 
#  still needed to record the marking in learn (we need to link the mark to a file). If you prefer to have off-
#  line marking (as in other courses), of course, you can just submit to learn (i.e., interactive/in-person 
#  marking is possible but not compulsory!).
# '''
