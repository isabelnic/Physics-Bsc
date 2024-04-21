ReadMe:

-------For gameoflife.py------
When running in the terminal input 3 values after the file name:
N - the dimensions of the square lattice
start - options are 'rand' for random starting conditions, 'glider' for a glider
	and 'blinker' for a blinker.
num_sims - the number of simulations you would like to do to create the histogram

If you want to see the animation uncomment the animation lines. The plot will be shown at the end of the simulation.

-------For track_glider.py-------
Input, N the lattice number. For animation uncomment animation lines. At the end the plot will show the path of the glider and the average speed will be printed in the terminal.

-------For SIRS.py-------
input values:
N - lattice dimensions
prob1, prob2, prob3 - the 3 probabilities that determine whether a square changes from S->I, I->R and R->S, respectively.
plot_type - 'avgi' for the plot of the average for p1 and p2 varying and 'vari' for the cut section across p1.

Uncomment animation lines for animation. If 'avgi' has already run and you would like the contour plot of the variance run the file plot_contour_vari.py to plot it.

-------For immunity_frac.py-------
input:
N - lattice dimensions
ifrac - the fraction immune

The plot will be shown at the end of the simulation
