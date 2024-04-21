import pandas as pd
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
np.set_printoptions(threshold=sys.maxsize)

if(len(sys.argv) != 2):
    print("type after file name these params: N")
    sys.exit()

''' either type 'rand' or 'glider' after the N'''
N = int(sys.argv[1])

nstep = 10100  # evergy n step there is 1 sweep
n2 = N*N
sweeps = 10100
plot_freq = 5

def glider(loca, locb):
    return [loca, loca+1, loca+1, loca, loca-1], [locb-2, locb-1, locb, locb, locb]  


def pick_state():
    state = np.zeros((50, 50))
    glides = [glider(3, 3)]
    for g in glides:
        state[g[0], g[1]] = 1

    fig = plt.figure()
    plt.cla()
    plt.imshow(state)
    plt.draw()
    # plt.show()
    return state


def iterating(old_state):
    i, j, x, y, t, speed = 0, 0, [], [], [], []
    new_state = old_state.copy()
    for n in range(sweeps):
        for j in range(N):
            for i in range(N):
                # how many neibhors below
                neib = np.sum( old_state[[(i-1)%N,(i-1)%N,(i-1)%N,i,i,(i+1)%N,(i+1)%N,(i+1)%N], [(j-1)%N,j,(j+1)%N,(j-1)%N,(j+1)%N,(j-1)%N,j,(j+1)%N]] )
                
                # check if old state coord if alive or dead
                if (old_state[i, j] == 1) and ((neib < 2) or (neib > 3)):
                    new_state[i, j] = 0
                elif (old_state[i, j] == 0) and (neib == 3):
                    new_state[i, j] = 1
                # Any live cell with 2 or 3 live neighbours lives on to the next step.

        if n%5 == 0:
            row, column = np.where(old_state == 1)
            xi = row.mean()
            yj = column.mean()
            if not bool(x):
                x.append(xi)
                y.append(yj)
                t.append(time.time())
            elif (np.abs(x[-1]-xi)< 5) or (np.abs(y[-1]-yj)< 5):
                x.append(xi)
                y.append(yj)
                t.append(time.time())
                #using pythagorous
                vel = np.sqrt((x[-1] - x[-2])**2 + (y[-1]-y[-2])**2) / plot_freq
                speed.append(vel) # unit = squares per sweep
                # print(vel)

        old_state = new_state.copy()
        if n > 5000:
            break
        # plt.cla()
        # plt.imshow(new_state)
        # plt.draw()
        # plt.pause(0.001)
    print('velocity mean =', vel.mean(), 'in squares per sweep')
    plt.plot(x[0: -1: 5], y[0: -1: 5]) # plot every 5 sweeps
    plt.show()
    return 


iterating(pick_state())
