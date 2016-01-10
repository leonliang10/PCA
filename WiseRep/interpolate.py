__author__ = 'Leon Liang'

'''
This Python file takes processed spectra and interpolates
to desire number of points based on input, min_wave, and 
max_wave

Outputs the interpolated spectra into a hdf5 file
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import os, os.path, glob, sys, optparse, h5py
import util.get_data as get_data
import util.convert_HDF5 as convert_HDF5

def interpolation(min_wave, max_wave, category = None):
	data_path = get_data.demean(category)
	f_x = {}
	for data_file in data_path:
		dataset = h5py.File(data_file, 'r')
		for data_name in dataset:
			spectrum = dataset[data_name][:,:]
			wavelength = spectrum[:,0]
			flux = spectrum[:,1]
			nonzeros = np.where(wavelength)
			wavelength = wavelength[nonzeros]
			flux = flux[nonzeros]
			[num_waves,] = wavelength.shape
			f = interpolate.interp1d(wavelength, flux, bounds_error = False, fill_value = 0)
			f_x[data_name] = f
	return f_x

def log_rebinning(min_wave, max_wave, N, category = None):
	f_x = interpolation(min_wave, max_wave, category)
	data_path = get_data.demean(category)
	for data_file in data_path:
		dataset = h5py.File(data_file, 'r')
		data_category = data_file.split('/')[1]
		for data_name in dataset:
			new_wavelength = np.logspace(np.log10(min_wave), np.log10(max_wave), num = N, endpoint = False)
			f = f_x[str(data_name)]
			new_flux = f(new_wavelength)
			new_rebin_data = np.vstack([new_wavelength, new_flux]).T
			data_type = data_category + '_' + 'log_rebin'
			convert_HDF5.write(data_category, str(data_name), data_type, new_rebin_data)

def linear_rebinning(min_wave, max_wave, N, category = None):
	f_x = interpolation(min_wave, max_wave, category)
	data_path = get_data.demean(category)
	for data_file in data_path:
		dataset = h5py.File(data_file, 'r')
		data_category = data_file.split('/')[1]
		for data_name in dataset:
			new_wavelength = np.linspace(min_wave, max_wave, num = N, endpoint = False)
			f = f_x[str(data_name)]
			new_flux = f(new_wavelength)
			new_rebin_data = np.vstack([new_wavelength, new_flux]).T
			data_type = data_category + '_' + 'linear_rebin'
			convert_HDF5.write(data_category, str(data_name), data_type, new_rebin_data)

parser = optparse.OptionParser()
parser.add_option("--rebin",dest="rebin")
(opts, args) = parser.parse_args()

if (opts.rebin):
	log = False
	linear = False
	if (opts.rebin.lower() == 'log'):
		log = True
	elif (opts.rebin.lower() == 'linear'):
		linear = True
	else:
		print 'Please enter a valid rebin option: [log / linear]'
		sys.exit()
else:
	log = True
	linear = False

if (log):
	print 'Logrithmic rebinning data...'

if (linear):
	print 'Linearly rebinning data...'

min_wave = 4000
max_wave = 8000
N = 2000
if (log):
	log_rebinning(min_wave, max_wave, N)
if (linear):
	linear_rebinning(min_wave, max_wave, N)



