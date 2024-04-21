from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
if(len(sys.argv) != 2):
    print("Type the pertubation of the starting phi")
    sys.exit()

# Define parameters
N = 100  # dimension Number 
M, a, k = 0.1, 0.1, 0.1  # Diffusion, chemical potential constants
sweeps = 500000 # Number of simulations
'''good params: dt = 1.2, dx = 2'''
dx = 1
dt = 2 
phi0 = float(sys.argv[1])
phi = np.random.uniform(-0.1+phi0, 0.1+phi0, (N,N))

# calculating stability
stability = M * dt / (dx**2)
if stability >= 1/4:
    print('!!NOT A STABLE ALGOrithm!! \nstabiliy =', stability)
else:
    print('A Stable Algoithm, well done! \nstabiliy =', stability)


def iterating(phi, dx, dt):
    plt.cla()
    plt.imshow(phi, cmap='coolwarm')
    plt.draw()
    plt.colorbar()
    plt.pause(0.001)
    plot_freq = 300
    fed = {'fed': [], 'step': []} # FreeEnergyDensity

    for n in tqdm(range(sweeps)):
        mu = - a*phi + a*phi**3 - k*(np.roll(phi, shift=1, axis=0) + np.roll(phi, shift=-1, axis=0) +
                    np.roll(phi, shift=1, axis=1) + np.roll(phi, shift=-1, axis=1) - 4*phi) 
        phi += M*(dt/dx**2)*(np.roll(mu, shift=1, axis=0) + np.roll(mu, shift=-1, axis=0) +
                    np.roll(mu, shift=1, axis=1) + np.roll(mu, shift=-1, axis=1) - 4*mu)
        if(n%(plot_freq) == 0):
            fed['fed'].append(dx**2 * np.sum(-(a/2) * phi**2 + (a/4) * phi**4 + (k/2) * ( (np.roll(phi, shift=1, axis=0)-phi)**2
                        + (np.roll(phi, shift=1, axis=1)-phi)**2) ))
            fed['step'].append(n)
            plt.cla()
            plt.imshow(phi, cmap='coolwarm')
            plt.draw()
            plt.pause(0.001)
        if n % int(sweeps/6) == 0:
            plot_freq *= 2 # decreasing plotting as time goes on
    return fed


fed = iterating(phi, dx, dt)
fig, ax = plt.subplots()
ax.scatter(fed['step'], fed['fed'], marker='X')  
ax.set_xlabel(r'sweeps')
ax.set_ylabel('Free energy')
plt.savefig(f'freeEnergy-starting-{phi0}-sweeeps{sweeps}.png')
plt.show()  

