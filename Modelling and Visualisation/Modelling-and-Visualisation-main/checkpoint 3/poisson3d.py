import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
from tqdm import tqdm
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
import sys

if(len(sys.argv) != 4):
    print("\nType one for the 3 of these: \n1. The dimention: N (int), \n2. Analysis method: 'jacobian', 'gauss', 'sor' or 'findw', \n3. Field type: 'electric' or 'magnetic'. \n")
    sys.exit()

def create_checkerboard(shape):
        mask =  np.bool_(np.indices(shape).sum(axis=0) % 2)
        return mask, ~mask

# Set up the system parameters
N = int(sys.argv[1])  # Number of grid points in each dimension
ep0, dx = 1, 1  # sp.epsilon_0
sweeps = 500000
method, field_type, xyb = sys.argv[2], sys.argv[3], slice(1, N-1)  # method, field and  xy pab boundry
padding_loc = 0
No2, No3 = N//2, N//3 # middle of lattice
rho = np.zeros((N, N, N)) # system with nothing
fancy = input(print('\nWould you like a fancy arrangement (electric)? \n type "fancy" or click enter if not'))


if field_type == 'electric':
    zb = slice(1, N-1) # z boundry to pad
    padding_loc = ((1,1), (1,1),(1, 1))
    if bool(fancy):
        # adding a funky start pattern
        rho[No2, No2-15, No2] = 1
        rho[No2, No2+15, No2] = 1
        rho[No2, No2, No2+15] = 1
        rho[No2, No2, No2-15] = 1
    else:
        # adding a boring charge at the centre
        rho[No2, No2, No2] = 1
elif field_type == 'magnetic':
    '''wire going in the z direction'''
    zb = slice(0, N)  # z boundry
    padding_loc = ((0, 0), (1,1), (1,1))
    if bool(fancy):
        rho[:, 25//2, No2] = 3
        rho[:, 50-25//2, No2] = 3
        rho[:, No2, 25//2] = 3
        rho[:, No2, 50-25//2] = 3
    else:
        rho[:, No2, No2] = 1  # [z, x, y]


def jacobi3d(phi):
    # convergence of ~ N^2 
    error, end_n = 1, 1
    for n in tqdm(range(sweeps)):
        newphi = (1/6)*(np.roll(phi, shift=1, axis=0) + np.roll(phi, shift=-1, axis=0) + 
                    np.roll(phi, shift=1, axis=1) + np.roll(phi, shift=-1, axis=1) + 
                    np.roll(phi, shift=1, axis=2) + np.roll(phi, shift=-1, axis=2) ) + rho
        
        newphi = np.pad(newphi[zb, xyb, xyb], pad_width=padding_loc) # set BCs
        error = np.sum(np.abs(phi-newphi))
        if error < 10e-3:
            end_n = n
            break
        if n%300 == 0:
            print('\nError ========', error)
        phi = newphi.copy()
    print('iterations till finish=', end_n)
    return phi


def gauss(phi):
    # faster than jacobi by factor of 2
    black, white = create_checkerboard(np.full(3,N))
    error, end_n = 1, 1
    for n in tqdm(range(sweeps), desc=f'{method} sim'): 
        start_phi = phi.copy()
        phi = (1/6)*(np.roll(phi, shift=1, axis=0) + np.roll(phi, shift=-1, axis=0) + 
                    np.roll(phi, shift=1, axis=1) + np.roll(phi, shift=-1, axis=1) + 
                    np.roll(phi, shift=1, axis=2) + np.roll(phi, shift=-1, axis=2) ) + rho
        phi[black] = start_phi[black]  # set phi to white squares only updates values
        phi = np.pad(phi[zb, xyb, xyb], pad_width=padding_loc)  # BCs
        phi_half_upd = phi.copy()  # half updated phi (white updated)
        # find out black squares based on future white squares
        phi = (1/6)*(np.roll(phi, shift=1, axis=0) + np.roll(phi, shift=-1, axis=0) + 
                    np.roll(phi, shift=1, axis=1) + np.roll(phi, shift=-1, axis=1) + 
                    np.roll(phi, shift=1, axis=2) + np.roll(phi, shift=-1, axis=2) ) + rho   
        # setting the whites to the 1st updated whites
        phi[white] = phi_half_upd[white]  
        # phi = Gauss phi
        phi = np.pad(phi[zb, xyb, xyb], pad_width=padding_loc)  # BCs

        error = np.sum(np.abs(start_phi-phi))
        if n%200 == 0:
            print('\nError ========', error)
        if error < 10e-3:
            end_n = n
            break
    return phi


def sor(phi, omega):
    # faster than jacobi by factor of 2
    print('\nomega =', omega)
    black, white = create_checkerboard(np.full(3,N))
    error, end_n = 1, 1
    for n in tqdm(range(sweeps), desc=f'{method} sim'): 
        start_phi = phi.copy()
        phi = (1/6)*(np.roll(phi, shift=1, axis=0) + np.roll(phi, shift=-1, axis=0) + 
                    np.roll(phi, shift=1, axis=1) + np.roll(phi, shift=-1, axis=1) + 
                    np.roll(phi, shift=1, axis=2) + np.roll(phi, shift=-1, axis=2) ) + rho
        phi = omega*phi + (1-omega)*start_phi
        phi[black] = start_phi[black]  # set phi to white squares only updates values
        phi = np.pad(phi[zb, xyb, xyb], pad_width=padding_loc)  # BCs
        phi_half_upd = phi.copy()  # half updated phi (white updated)

        # find out black squares based on future white squares
        phi = (1/6)*(np.roll(phi, shift=1, axis=0) + np.roll(phi, shift=-1, axis=0) + 
                    np.roll(phi, shift=1, axis=1) + np.roll(phi, shift=-1, axis=1) + 
                    np.roll(phi, shift=1, axis=2) + np.roll(phi, shift=-1, axis=2) ) + rho
        
        phi = omega*phi + (1-omega)*start_phi    
        # setting the whites to the 1st updated whites
        phi[white] = phi_half_upd[white]  
        # phi = Gauss phi
        phi = np.pad(phi[zb, xyb, xyb], pad_width=padding_loc)  # BCs

        error = np.sum(np.abs(start_phi-phi))
        if n%200 == 0:
            print('\nError ========', error)
        if error < 10e-3:
            end_n = n
            break
    print('\ntotal # iterations=', end_n)
    return phi, end_n


def calc_man_field(phi):
    Ex = (np.roll(phi, shift=-1, axis=2) - np.roll(phi, shift=1, axis=2))/(-2*dx)
    Ey = (np.roll(phi, shift=-1, axis=0) - np.roll(phi, shift=1, axis=0))/(-2*dx)
    Ez = (np.roll(phi, shift=-1, axis=1) - np.roll(phi, shift=1, axis=1))/(-2*dx)
    return  Ez, Ex, Ey


def fitting(x, a):
    # if a == 2 then 1/x^2 graph if 1 then 1/x
    y = 1 / (x**a)
    return y


def distance_plots(data, data_type, initial):
    # data is either potential or field strength
    if data_type == 'potential':
        y = data[No2, No2, No2:-2] # electric
    elif data_type == 'field-strength':
        ei, ej, ek = data
        # mag of field in each direcion across the y direction from centre to edge
        y = np.sqrt(ei[No2, No2+1:-2, No2]**2 + ej[No2, No2+1:-2, No2]**2 + ek[No2, No2+1:-2, No2]**2)
    x = np.arange(0, len(y), 1)
    popt, pcov = curve_fit(fitting, x, y, p0=initial)
    print('fit values from y = 1 / (x**a) are ====', popt)

    ax = plt.figure().add_subplot()
    ax.set_title(f'{field_type} {data_type} with distance. 1/x^{popt[-1]}')
    ax.scatter(x, y)
    # ax.plot(x, fitting(x, *popt), c='r')
    ax.plot(x, fitting(x, 2))
    ax.set_xlabel('Distance from centre to edge')
    plt.savefig(f'{data_type}-distance-plot-{field_type}-{method}-N{N}.png')
    plt.show()


def plot2d(phi):
    '''potential'''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(f'Potential of the {field_type} Field using {method} at z={No2}')
    ax.set_xlabel('x'), ax.set_ylabel('y')
    ax.imshow(phi[No2,:, :], interpolation='gaussian')
    # ax.imshow(phi[No2, :, :], interpolation='gaussian') # phi[z, y, x]
    plt.savefig(f'2dSlice-{field_type}-{method}-field-N{N}.png', dpi=300)

    '''vector field'''
    E_i, E_j, E_k = calc_man_field(phi) # mnaual field calc
    ei_slice, ej_slice = E_i[No2,:, :], E_j[No2,:, :]
    x, y = np.meshgrid(np.linspace(0, N, N), np.linspace(0, N, N)) 
    # if you want to normalise the vectors to all be the same length
    # ei_norm = ei_slice / (np.sqrt(ei_slice**2+ej_slice**2))
    # ej_norm = ej_slice / (np.sqrt(ei_slice**2+ej_slice**2))

    ax = plt.figure().add_subplot()
    ax.set_title(f'{field_type} field')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    if field_type == 'electric':
        ax.quiver(x, y, ej_slice, ei_slice)
        plt.savefig(f'2d-field-{field_type}-{method}-N{N}-plot.png')
    elif field_type == 'magnetic':
        # for magnetic x and y are flipped
        ax.quiver(x, y, ei_slice, -ej_slice)
        plt.savefig(f'2d-field-{field_type}-{method}-plot-N{N}.png')
    plt.show()

    '''plotting the potential strength with distance from charge/wire'''
    if field_type == 'electric':
        distance_plots(phi, 'potential', 1)
        distance_plots([E_i, E_j, E_k], 'field-strength', 2)
    if field_type == 'magnetic':
        distance_plots(phi, 'potential', 1)
        distance_plots([E_i, E_j, E_k], 'field-strength', 1)

    return E_i, E_j, E_k


def save_data(phi, Ei, Ej, Ek):
    df = pd.DataFrame(columns = ['phi', 'Ex', 'Ey', 'Ez'])
    df['phi'] = phi.ravel()
    df['Ex'] = Ei.ravel()
    df['Ey'] = Ej.ravel()
    df['Ez'] = Ek.ravel()
    df.to_csv(f'{field_type}-N{N}-data-{method}-{N}by{N}.csv')
    return


def initialise():
    phi, w = np.zeros((N, N, N)), 1.81  # w= 1.81 for N = 50
    if field_type == 'electric':
        w = 1.88
    elif field_type == 'magnetic':
        w = 1.92 
    if method == 'jacobian':
        phi = jacobi3d(phi)
    elif method == 'gauss':
        phi = gauss(phi) # w is not used here
    elif method == 'sor':
        phi, _ = sor(phi, w)
    elif method == 'findw':
        wdf = pd.DataFrame(columns=['w', 'iterations'])
        ws = np.linspace(1, 1.999, 50)
        for w in tqdm(ws, desc='\nw iterations'):
            _ , end_n = sor(np.zeros((N, N, N)), w)
            wdf.loc[len(wdf)] = [w, end_n]

        wdf['norm iterations'] = wdf['iterations']/max(wdf['iterations'])
        best_w = round(wdf.iloc[np.argmin(wdf['iterations'])][0], 2) 
        plt.scatter(wdf['w'], wdf['norm iterations'])
        plt.title(f'Finding the optimal Omega value\nBest W={best_w}')
        plt.xlabel('omega value')
        plt.ylabel('Relatve iterations')
        plt.savefig(f'{fancy}-iterations-{field_type}-{method}-N{N}-omega-{best_w}.png')
        plt.show()
        wdf.to_csv(f'optimal-w-values-{field_type}-{method}-N{N}-{best_w}.csv')

    if method != 'findw':
        Ei, Ej, Ek = plot2d(phi)
        save_data(phi, Ei, Ej, Ek)


initialise()