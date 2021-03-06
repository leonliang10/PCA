__author__ = 'Leon Liang'

import numpy as np
import util.pca as pca
try:
	import matplotlib.pyplot as plt
except ImportError:
	print 'Cannot import Matplotlib. Please install Matplotlib before running.'
import util.get as get
import util.mkdir as mkdir
import h5py
import optparse, sys

WARNING = "Please enter the what you want to plot: python ploy.py [raw, deredshift, rebin, coefficients, pcomponents, U_matrix, K_reduced]."
COLORS = ['blue', 'green', 'red', 'cyan', 'magenta', 'purple', 'black']

def raw(category = None):
	data_path = get.data('raw', category)
	mkdir.plots(category = None, data_type = 'raw')
	for data_name in data_path:
		spectrum = np.loadtxt(data_name)
		wavelength = spectrum[:,0]
		flux = spectrum[:,1]
		plt.figure()
		plt.grid()
		plt.plot(wavelength, flux)
		name = data_name.split('/')[4]
		plt.title(name)
		plt.xlabel('wavelength')
		plt.ylabel('flux')
		data_category = data_name.split('/')[1]
		filename = 'supernova_data/' + data_category + '/plots/raw/' + name + '.eps'
		plt.savefig(filename, format='eps', dpi = 3500)
		plt.close()

def deredshift(category = None):
	data_path = get.data('deredshift', category)
	mkdir.plots(category = None, data_type = 'deredshift')
	for data_file in data_path:
		data_category = data_file.split('/')[1]
		dataset = h5py.File(data_file, 'r')
		for data_name in dataset:
			wavelength = dataset[data_name][:, 0]
			flux = dataset[data_name][:, 1]
			plt.figure()
			plt.grid()
			plt.plot(wavelength, flux)
			plt.xlabel('wavelength')
			plt.ylabel('flux')
			plt.title(data_name)
			filename = 'supernova_data/' + data_category + '/plots/deredshift/' + data_name + '.eps'
			plt.savefig(filename, format='eps', dpi = 3500)
			plt.close()
		dataset.close()

def trim(category = None):
	data_path = get.data('trim', category)
	mkdir.plots(category = None, data_type = 'trim')
	for data_file in data_path:
		data_category = data_file.split('/')[1]
		dataset = h5py.File(data_file, 'r')
		for data_name in dataset:
			wavelength = dataset[data_name][:, 0]
			flux = dataset[data_name][:, 1]
			plt.figure()
			plt.grid()
			plt.plot(wavelength, flux)
			plt.xlabel('wavelength')
			plt.ylabel('flux')
			plt.title(data_name)
			filename = 'supernova_data/' + data_category + '/plots/trim/' + data_name + '.eps'
			plt.savefig(filename, format='eps', dpi = 3500)
			plt.close()
		dataset.close()

def rebin(category = None, rebin_type = 'log'):
	data_path = get.data('rebin', category)
	mkdir.plots(category = None, dat_type = 'rebin_' + rebin_type)
	for data_file in data_path:
		data_category = data_file.split('/')[1]
		dataset = h5py.File(data_file, 'r')
		for data_name in dataset:
			wavelength = dataset[data_name][:, 0]
			flux = dataset[data_name][:, 1]
			plt.figure()
			plt.grid()
			plt.plot(wavelength, flux)
			plt.xlabel('wavelength')
			plt.ylabel('flux')
			plt.title(data_name)
			filename = 'supernova_data/' + data_category + '/plots/rebin_' + rebin_type + '/' + data_name + '.eps'
			plt.savefig(filename, format='eps', dpi = 3500)
			plt.close()
		dataset.close()

def coefficients(category = None, rebin_type = 'log', n = 80, legend = True, save = True, show = False):
	data_path = get.data('pca', category)
	mkdir.plots(category = 'all', data_type = 'pca/coefficients')
	for i in range(n):
		x = np.zeros([100])
		k = 0
		plt.figure()
		plt.grid()
		for data_file in data_path:
			data_category = data_file.split('/')[1]
			dataset = h5py.File(data_file, 'r')	
			coefficients_normal = dataset['coefficients_normal']
			[m,n] = coefficients_normal.shape
			plt.scatter(x[:n], coefficients_normal[i,:], color = COLORS[k%len(COLORS)], label = data_category)
			x += 1
			k += 1
			dataset.close()

		plt.scatter(x[0] + 2, np.array([0]), color = 'white')
		plt.title('coefficient ' + str(i))
		if legend:
			plt.legend()
		if save:
			name = 'supernova_data/all/plots/pca/coefficients/coefficient_' + str(i) + '.eps'
			plt.savefig(name, format='eps', dpi = 3500)
		if show:
			plt.show()
		plt.close()

def pcomponents(category = None, components = [[0,1]], legend = True, save = True, show = False):
	data_path = get.data('pca', category)
	mkdir.plots(category = 'all', data_type = 'pca/pcomponents')
	for component in components:
		k = 0
		plots = []
		plot_names = []
		plt.figure()
		plt.grid()
		i = component[0]
		j = component[1]
		for data_file in data_path:
			data_category = data_file.split('/')[1]
			dataset = h5py.File(data_file, 'r')	
			coefficients_reduced = dataset['coefficients_reduced'][:]
			cx = coefficients_reduced[i,:]
			cy = coefficients_reduced[j,:]
			p = plt.scatter(cx, cy, color = COLORS[k%len(COLORS)], label = category)
			plots.append(p)
			plot_names.append(data_category)
			k += 1
		if legend:
			plt.legend(plot_names, loc='right', bbox_to_anchor = (1.1, 0.2), fancybox = True)
		plt.grid()
		plt.xlabel('c' + str(i))
		plt.ylabel('c' + str(j))
		plt.title('c' + str(i) + ' vs ' + 'c' + str(j))
		if save:
			name = 'supernova_data/all/plots/pca/pcomponents/' + 'c' + str(i) + '_vs_' + 'c' + str(j) + '.eps'
			plt.savefig(name, format='eps', dpi = 3500)
		if show:
			plt.show()
		plt.close()

def U_matrix(category = None, legend = True, save = True, show = False):
	data_path = get.data('pca', 'all')
	mkdir.plots(category = 'all', data_type = 'pca/U')
	mkdir.plots(category = 'all', data_type = 'pca/individual_U')
	wavelength = np.linspace(4000, 8000, 2000)
	dataset = h5py.File(data_path[0], 'r')
	U = dataset['U']
	for i in range(2000):
		plt.figure()
		p = plt.plot(wavelength, U[:,i])
		plt.grid()
		plt.xlabel('wavelength')
		plt.ylabel('U[:,' + str(i) + ']')
		plt.title('column ' + str(i) + ' of U')
		if save:
			name = 'supernova_data/all/plots/pca/individual_U/column_' + str(i) + '_of_U.eps'
			plt.savefig(name, format='eps', dpi = 3500)
		if show:
			plt.show()
		plt.close()
	for j in range(0,2000,5):
		plt.figure()
		plot_names = []
		offset = 0
		for k in range(5):
			p = plt.plot(wavelength, U[:,j+k] + offset, color = COLORS[k], label = str(j + k))
			offset += max(U[:,j+k]) + 0.2
			plot_names.append(str(j + k))
		plt.grid()
		plt.xlabel('wavelength')
		plt.ylabel('U[:,i]')
		plt.title('columns ' + str(j) + ' ' + str(j+1) + ' ' + str(j+2) + ' ' + str(j+3) + ' ' + str(j+4) + ' of U')
		if legend:
			plt.legend(plot_names, loc='right', bbox_to_anchor = (1.1, 0.2), fancybox = True)
		if save:
			name = 'supernova_data/all/plots/pca/U/columns_' + str(j) + '-' + str(j+4) + '_of_U.eps'
			plt.savefig(name, format='eps', dpi = 3500)
		if show:
			plt.show()
		plt.close()

def K_reduced(category = None, data_file = None, legend = True, save = True, show = False):
	mkdir.plots(category = 'all', data_type = 'pca/K_reduced')
	data_path = get.data('pca', 'all')
	pca_dataset = h5py.File(data_path[0], 'r')
	specific_spectrum_index = np.where(pca_dataset['keys'][:] == data_file)[0]
	
	if specific_spectrum_index.shape[0] == 0:
		print 'Cannot find specific spectrum entered.'
		sys.exit()

	specific_spectrum_index = specific_spectrum_index[0]
	wavelength = pca_dataset['wavelength'][specific_spectrum_index,:]
	flux = pca_dataset['flux'][specific_spectrum_index,:]
	U = pca_dataset['U'][:,:]
	U_reduced = np.zeros(U.shape)
	for i in range(7):
		offset = 0
		for j in range(i+1):
			U_reduced[:,j] = U[:,j]

		coefficients_reduced = (flux.dot(U_reduced)).T
		K_reduced = (U_reduced.dot(coefficients_reduced)).T
		plt.figure()
		plt.grid()
		plt.plot(wavelength, flux, label = category)
		plt.plot(wavelength, K_reduced, label = 'sum(0:' + str(i) + ')', color = 'red')
		previous_single_K_reduced = 0
		for k in range(i+1):
			single_coefficients_reduced = (flux.dot(U_reduced[:,k])).T
			single_K_reduced = (U_reduced[:,k].dot(single_coefficients_reduced)).T
			if k == 0:
				offset += max(single_K_reduced) - min(min(K_reduced), min(flux))
			else:
				offset += max(single_K_reduced) - min(min(previous_single_K_reduced), min(flux))
			# offset += offset/50
			plt.plot(wavelength, single_K_reduced - offset, label = str(k), color = 'black')
			previous_single_K_reduced = single_K_reduced

		plt.xlabel('wavelength')
		plt.ylabel('flux')
		plt.title(category + '/' + data_file)
		if legend:
			plt.legend()
		if save:
			name = 'supernova_data/all/plots/pca/K_reduced/' + category + '_' + str(i) + '.eps'
			plt.savefig(name, format='eps', dpi = 3500)
			np.savetxt('supernova_data/all/plots/pca/K_reduced/' + category + '_coefficients_reduced.txt', coefficients_reduced[:6])
		if show:
			plt.show()
		plt.close()