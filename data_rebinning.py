# @author Leon Liang
#
# Takes in [filename] that consists of all the data
# and rebins the data into [factor] of data points
# of the original data

import numpy as np
import scipy as sp
import sys

def data_rebinning(data, factor):
    from scipy import ndimage
    from numpy import zeros

    [x,y] = data.shape
    new_x = int(round(x*factor))

    rebinned_data = np.zeros([new_x,y])
    for i in range(y):
        rebinned_data[:,i] = sp.ndimage.interpolation.zoom(data[:,i], factor)

    return rebinned_data



# first input is filename
# second input is the factor of float type
# that user wants to rebin data by
filename = sys.argv[1]
factor = float(sys.argv[2])

data = np.loadtxt(filename)
rebinned_data = data_rebinning(data, factor)

filename = 'rebin_' + filename

np.savetxt(filename, rebinned_data)

