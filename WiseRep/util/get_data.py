__author__ = 'Leon liang'

'''
This Python file gets all of data using glob
and returns the data as a list of strings
that other functions can then utilize
'''

import glob

def trimmed(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/trimmed_data/*')
	else:
		return glob.glob('supernova_data/type*/trimmed_data/*')

def demeaned(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/demeaned_data/*')
	else:
		return glob.glob('supernova_data/type*/demeaned_data/*')

def deredshift(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/deredshift_data/*')
	else:
		return glob.glob('supernova_data/type*/deredshift_data/*')

def raw(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/raw_data/*')
	else:
		return glob.glob('supernova_data/type*/raw_data/*')

def linear(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/linear_rebin_data/*')
	else:
		return glob.glob('supernova_data/type*/linear_rebin_data/*')

def log(category = None):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/log_rebin_data/*')
	else:
		return glob.glob('supernova_data/type*/log_rebin_data/*')

def hdf5(category = None, type_all=False):
	if category is not None:
		return glob.glob('supernova_data/' + category + '/hdf5_data/*')
	else:
		if type_all:
			return glob.glob('supernova_data/type*/hdf5_data/*')
		else:
			types = glob.glob('supernova_data/type*/hdf5_data/*')
			types.remove('supernova_data/type_all/hdf5_data/type_all.hdf5')
			return types



def all_hdf5(category = None):
	return glob.glob('supernova_data/type_all/hdf5_data/*')
	# for testing purposes:
	# return glob.glob('test.hdf5')

def types(category = None, data_type = None, type_all=False):
	if category is not None:
		if data_type is not None:
			if data_type == 'trimmed':
				return trimmed(category)
			if data_type == 'demeaned':
				return demeand(category)
			if data_type == 'deredshift':
				return deredshift(category)
			if data_type == 'raw':
				return raw_data(category)
			if data_type == 'linear':
				return linear(category)
			if data_type == 'log':
				return log(category)
			if data_type == 'hdf5':
				return hdf5(category)
	if type_all:
		return glob.glob('supernova_data/type*')
	else:
		types = glob.glob('supernova_data/type*')
		types.remove('supernova_data/type_all')
		return types