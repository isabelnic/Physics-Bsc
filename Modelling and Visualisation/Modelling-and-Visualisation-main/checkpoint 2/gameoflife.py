import pandas as pd
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
np.set_printoptions(threshold=sys.maxsize)

if(len(sys.argv) != 4):
    print("type after file name these params: N, ['rand' or 'glider' or 'blinker'], number of simulations" 
          "for the histogram")
    sys.exit()

''' either type 'rand' or 'glider' after the N'''
N, start, num_sims = int(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3])

nstep = 10100  # evergy n step there is 1 sweep
n2 = N*N
sweeps = 1000
plot_freq = 20

def glider(loca, locb):
    return [loca, loca+1, loca+1, loca, loca-1], [locb-2, locb-1, locb, locb, locb]  
def blinker(loca, locb):
    return [loca, loca, loca], [locb-1, locb, locb+1]  


def pick_state():
    state = 0
    if start == 'rand':
        state = np.random.choice([0, 1], (N, N))
    if start == 'glider':
        state = np.zeros((50, 50))
        glides = [glider(5, 20), glider(10, 26), glider(40, 5)]
        for g in glides:
            state[g[0], g[1]] = 1
    if start == 'blinker':
        state = np.zeros((50, 50))
        blinks = [blinker(25, 25), blinker(13, 30), blinker(10, 40)]
        for b in blinks:
            state[b[0], b[1]] = 1

    fig = plt.figure()
    # uncomment for animation
    plt.cla()
    plt.imshow(state)
    plt.draw()
    plt.show()
    # live cell = +1
    return state


def iterating(old_state):
    sumstate = []
    new_state = old_state.copy()
    for n in range(sweeps*n2):
        for j in range(N):
            for i in range(N):
                # how many neibhors below
                neib = np.sum( old_state[ [(i-1)%N,(i-1)%N,(i-1)%N,i,i,(i+1)%N,(i+1)%N,(i+1)%N], [(j-1)%N,j,(j+1)%N,(j-1)%N,(j+1)%N,(j-1)%N,j,(j+1)%N]] )
                
                # check if old state coord if alive or dead
                if (old_state[i, j] == 1) and ((neib < 2) or (neib > 3)):
                    new_state[i, j] = 0
                elif (old_state[i, j] == 0) and (neib == 3):
                    new_state[i, j] = 1
                # Any live cell with 2 or 3 live neighbours lives on to the next step.
                
        sumstate.append(np.sum(old_state)-np.sum(new_state))
        if (n > 10) and (all(s < 4 for s in np.abs(sumstate[-10: -1]))):
            break
        
        # for simulation uncomment this
        if(n%(plot_freq) == 0):
            plt.cla()
            plt.imshow(new_state)
            plt.draw()
            plt.pause(0.001)

        old_state = new_state.copy()
    equilibrium_time = len(sumstate)
    print('number of iterations till equilibrium =', equilibrium_time)
    return equilibrium_time


# iterating(pick_state())

'for repeating rand evolution for the hist uncomment everything out below'
def rand_evolution():
    equil_times = {'times': []}
    for sim in range(num_sims):
        start = time.time()
        print('simulation', sim)
        equil_times['times'].append(iterating(np.random.choice([0, 1], (N, N))))
        print('time for this sim =', time.time() - start)
    print('the mode and min value is =', max(set(equil_times['times']), key=equil_times['times'].count))
    pd.DataFrame(equil_times).to_csv('hist-data.csv') 

def plot_hist():
    times = pd.read_csv('hist-data.csv')['times']
    print(times.max(), times.min())
    plt.hist(times, bins=np.arange(0, 4000, 100))
    plt.title(f'The Equilibration Times of the Game of Life with {num_sims} sims')
    plt.xlabel('# iterations')
    plt.xlim(0, 4000)
    plt.ylabel('frequency')
    plt.savefig(f'GOL-hist-{num_sims}-sims.png', dpi=300)
    plt.show()
    return

if start == 'rand':
    rand_evolution()
    plot_hist()