To execute the code you type python file_Checkpoint-1.py followed by the following numbers, in the same 
order with a space between them:
- Dimension of the lattice, usually 50 so type your number x. It will always be square.
- The starting temperature for example, 1
- The method: for Glauber type 'g' for Kawasaki type 'k'

When you run the file it will calculate the energy, magnetization, susceptibility, and heat capacity
for temperatures from 1 to 3 in steps of 0.1. It will plot all 4 graphs as a quick check. After
running the file it will save a csv with the data.
The file plot_cp1.py can be run after running the main file Checkpoint-1.py, it takes in the 
datafiles and plots them comparing Glauber to Kawasaki (you have to run both Glauber and Kawasaki
in order to get this plot).


If you would only like to see the animation for one temperature you need to comment out the 
functions runalltemps() and plot() and add a line that calls the main(kT, init(0, kT)) function
like so. To see the animation uncomment lines 42-45 and 83-87 or 114-117 depending on if you 
are running for Glauber or Kawasaki.

