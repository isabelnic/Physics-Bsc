import numpy as np
from scipy import integrate
from scipy.special import erfinv
from iminuit import Minuit
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2





class Linear:
    def __init__( self,  lolimit, hilimit, slope, intercept):
        self.lolimit = lolimit
        self.hilimit = hilimit
        self.slope = slope
        self.intercept = intercept
        self.mass = []

    # Evaluate method (un - normalised )
    def evaluate( self , t ):
        return self.intercept + self.slope * t
    
    def maxval( self ):
        return self.evaluate(self.lolimit)

    def next( self ):
        doLoop = True
        while ( doLoop ):
            # start with uniform random number in [ lolimit , hilimit ]
            x = np.random.uniform( self.lolimit, self.hilimit )
            y1 = self.evaluate(x)
            y2 = np.random.uniform(0, self.maxval())
            if (y2 < y1):
                filtered_x = x
                self.mass.append(filtered_x)
                return filtered_x
    
    def integral( self, low, high ):
        return integrate.quad(self.evaluate, low, high)[0]
    





class Gaussian:
    def __init__( self,  mean, sigma ):
        self.mean = mean
        self.sigma = sigma
        self.mass = []
    
    #Method to return value of Gaussian at point x
    def evaluate( self, x ):
        val = np.exp( - (x-self.mean)**2 / (2.0 * self.sigma**2 ))
        norm = self.sigma * np.sqrt( 2.*np.pi )
        return val/norm

    def evaluate_nonorm( self, x ):
        return np.exp( - (x-self.mean)**2 / (2.0 * self.sigma**2 ))

    def maxval( self ):
        return self.evaluate(self.mean)

    # Method to return a random number with a Gaussian distribution 
    def next( self ):      
        val = np.random.normal(self.mean, self.sigma, size=None)
        self.mass.append(val) 
        return val

    def integral( self, low, high ):
        return integrate.quad(self.evaluate, low, high)[0]
    
    def Zscore( self, pvalue ):
        return erfinv(1 - pvalue) * np.sqrt(2)
    




class SignalWithBackground:
    def __init__( self, mean , sigma , sig_fraction , intercept , slope , XMIN , XMAX ):
        self.sig_fraction = sig_fraction
        self.signal = Gaussian(mean, sigma)
        self.background = Linear(XMIN, XMAX, slope, intercept)
        self.mass_sig, self.mass_bgd, self.mass = [], [], []
        self.mean, self.sigma = mean, sigma

    # Draw random number form distribution
    def next( self ):
        q = np.random.uniform()
        if (q < self.sig_fraction):
            # draw x from signal distribution
            filtered_x = self.signal.next()
            self.mass_sig.append( filtered_x )
        else:
            # draw x from background distribuion
            filtered_x = self.background.next()
            self.mass_bgd.append( filtered_x )

        self.mass.append( filtered_x )
        return filtered_x

    def combined_sigs(self, x, p0, p1, F):
        sig = np.exp( - (x-self.mean)**2 / (2.0 * self.sigma**2 )) / (self.sigma * np.sqrt( 2.*np.pi ))
        bgd = p1*x + p0
        return F * sig + bgd  # when F=0, just background

    def calc_chi2( self, p0, p1, F ): # signal present
        n_obs, bin_edges = np.histogram(self.mass, NBINS)
        x = np.zeros(len(n_obs))
        # don't normalise the gaussian
        for i in range(len(n_obs)):
            x[i] = (bin_edges[i] + bin_edges[i+1])/2
            
        n_exp = self.combined_sigs(x, p0, p1, F)
        n_exp[n_exp<=0] = 1e-3  # to prevent dividing by 0

        return 2*np.sum(n_exp - n_obs + n_obs * np.log(n_obs/n_exp))
