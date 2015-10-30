__author__ = 'Leon Liang'

import numpy as np, h5py, os, os.path, glob, sys
import get_data

def create_File(all_types):
	for data_dir in all_types:
		if not (os.path.isdir(data_dir + '/hdf5/')):
				os.mkdir(data_dir + '/hdf5/')

	for data_dir in all_types:
		data_type = data_dir.split('/')[1]
		f = h5py.File(data_dir + '/hdf5/' + data_type + '.hdf5', 'w')
		f.close()

def convert_HDF5():
	all_types = get_data.types(True)
	create_File(all_types)
	dataset = get_data.demeaned()
	for data in dataset:
		data_str = data.split('/')
		data_type = data_str[1]
		data_name = data_str[3]
		data_file = h5py.File('supernova_data/' + data_type + '/hdf5/' + data_type + '.hdf5', 'a')
		data_file_all = h5py.File('supernova_data/type_all/hdf5/type_all.hdf5', 'a')
		spectrum = np.loadtxt(data)
		data_file.create_dataset(data_name, data=spectrum)
		data_file_all.create_dataset(data_type + ':' + data_name + '.hdf5', data=spectrum)
		data_file.close()
		data_file_all.close()

if __name__ == '__main__':
	convert_HDF5()


