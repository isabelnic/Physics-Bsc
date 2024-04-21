# For checkpoint 3 there are 2 .py files:
poisson3d.py and cahn-hilliard.py

## For cahn-hilliard.py:
1. Run the file in the terminal following the starting perturbation for phi which can be 
    0, 0.5, -0.5 or other.
2. An animation should start once the code starts running.
3. At the end of the run the code will save a file of how the free energy changes over 
    the iterations in the simulation.

## For poisson3d.py:
1. Run the file in the terminal following the simulation dimension (N fro example 50 or 100), simulation method,
(method, options = jacobian, gauss, sor) and then the field type (field_type, options = electric or 
magnetic).
2. The simulation will run until the error of the previous phi an current phi go below 10e-3
3. Once the simulation has finished it will save and show a plot of the potential (phi), the field 
and the potential strength as a function of distance from the centre.

- you can also plot a fancy (not that fancy) arrangement of charges or wires. all you need to do is
type any string (or "fancy") when the prompt appears in the terminal. If you wish to just have a 
normal (boring) arrangement when the prompt appears just type enter. Bare in mind the fitting for
potential and field strength is not meant for the fancy arrangements.
