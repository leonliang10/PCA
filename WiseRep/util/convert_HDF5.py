__author__ = 'Leon Liang'

import h5py, util.mkdir as mkdir

# def create_File(all_types):
# 	for data_dir in all_types:
# 		if not (os.path.isdir(data_dir + '/hdf5_data/')):
# 				os.mkdir(data_dir + '/hdf5_data/')

# 	for data_dir in all_types:
# 		data_category = data_dir.split('/')[1]
# 		f = h5py.File(data_dir + '/hdf5_data/' + data_category + '.hdf5', 'w')
# 		f.close()

# def convert_HDF5():
# 	all_types = get_data.types(type_all=True)
# 	create_File(all_types)
# 	dataset = get_data.log()
# 	for d in dataset:
# 		data_str = d.split('/')
# 		data_category = data_str[1]
# 		data_name = data_str[3]
# 		data_file = h5py.File('supernova_data/' + data_category + '/hdf5_data/' + data_category + '.hdf5', 'a')
# 		data_file_all = h5py.File('supernova_data/type_all/hdf5_data/type_all.hdf5', 'a')
# 		spectrum = np.loadtxt(d)
# 		data_file.create_dataset(data_name, data = spectrum)
# 		data_file_all.create_dataset(data_category + ':' + data_name + '.hdf5', data=spectrum)
# 		data_file_all.close()
# 		data_file.close()

def create(data_category, data_name, data_type, spectrum):
	mkdir.data(data_category)
	data_file = h5py.File('supernova_data/' + data_category + '/data/' + data_type + '.hdf5')
	data_file.create_dataset(data_name, data = spectrum)
	data_file.close()
		
if __name__ == '__main__':
	convert_HDF5()