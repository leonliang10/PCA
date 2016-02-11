__author__ = 'Leon Liang'

'''
This Python File serves as a command processing
file that takes all inputs from users and calls
corresponding functions from other files
'''

import optparse, sys
import util.trim as trim
import util.deredshift as deredshift
import util.demean as demean
import util.rebin as rebin
import util.pca as pca
import util.plot as plt

parser = optparse.OptionParser()
parser.add_option("--trim", dest = "trim")
parser.add_option("--deredshift", dest = "deredshift")
parser.add_option("--demean", dest = "demean")
parser.add_option("--rebin", dest = "rebin")
parser.add_option("--rebin_type", dest = "rebin_type")
parser.add_option("--pca", dest = "pca")
parser.add_option("--category", dest = "category")
parser.add_option("--wave_range", dest = "wave_range")
parser.add_option("--min_wave", dest = "min_wave")
parser.add_option("--max_wave", dest = "max_wave")
parser.add_option("--components", dest = "components")
parser.add_option("--resolution", dest = "resolution")
parser.add_option("--legend", dest = "legend")
parser.add_option("--plot", dest = "plot")
parser.add_option("-n", dest = "n_comp")
parser.add_option("--n_coefs", dest = "n_coefs")
parser.add_option("-s", dest  = "save")
parser.add_option("--show", dest  = "show")



(opts, args) = parser.parse_args()

components = [[0,1]]
category = None
legend = True
n = 6
resolution = 2000
save = True
rebin_type = 'log'
show = False
compare = None
min_wave = 4000
max_wave = 8000
num_coefs = 80

if opts.category:
	category = opts.category.split('[')[1].split(']')[0].split(',')
if opts.components:
	comps = opts.components.split('[')[1].split(']')[0].split(',')
	if len(comps) % 2 > 0:
		print 'Please enter an even number of principal components you want to analysis'
		sys.exit()
	else:
		components = []
		for i in range(0, len(comps) - 1, 2):
			cx = int(comps[i])
			cy = int(comps[i + 1])
			components.append([cx, cy])
if opts.rebin_type:
	if opts.rebin_type == 'linear':
		rebin_type = 'linear'
	else:
		rebin_type = 'log'
if opts.wave_range:
	min_wave = float(opts.wave_range[0])
	max_wave = float(opts.wave_range[1])
else:
	if opts.min_wave:
		min_wave = float(opts.min_wave)
	if opts.max_wave:
		max_wave = float(opts.max_wave)
if opts.n_comp:
	n = int(opts.n_comp)
if opts.resolution:
	resolution = int(opts.resolution)
if opts.save:
	if opts.save == 'False':
		save = False
if opts.legend:
	if opts.legend == 'False':
		legend = False
if opts.n_coefs:
	num_coefs = int(opts.n_coefs)
if opts.show:
	show = True

if not (opts.trim or opts.deredshift or opts.demean or opts.rebin or opts.pca or opts.plot):
	trim.trim(min_wave, max_wave, category)
	deredshift.deredshift(category)
	demean.demean_flux(category)
	rebin.run(min_wave, max_wave, resolution, category, rebin_type)
	pca.run(category, rebin, n)
	plt.pcomponents(category, components, legend, save, show)

else:
	if opts.trim:
		trim.trim(min_wave, max_wave, category)
	if opts.deredshift:
		deredshift.deredshift(category)
	if opts.demean:
		demean.demean_flux(category)
	if opts.rebin:
		rebin.run(min_wave, max_wave, resolution, category, rebin_type)
	if opts.pca:
		pca.run(category, rebin, n)
	if opts.plot:
		if opts.plot.lower() == 'raw':
			plt.raw(category)
		elif opts.plot.lower() == 'deredshift':
			plt.deredshift(category)
		elif opts.plot.lower() == 'rebin':
			plt.rebin(category, rebin_type)
		elif opts.plot.lower() == 'coefficients':
			plt.coefficients(category, rebin_type, num_coefs, legend, save, show)
		elif opts.plot.lower() == 'u':
			plt.U_matrix(category, legend, save, show)
		else:
			plt.pcomponents(category, components, legend, save, show)
				