import sys
from os import listdir
from os.path import isfile, join

ds_name = sys.argv[1]
dirname = "datasets/" + ds_name
filter = sys.argv[2] if len(sys.argv) > 2 else ""

exclude_files = [
	'kaggle_songs.txt',
	'kaggle_users.txt',
	ds_name + '.txt',
	ds_name + '_ts.txt',
	ds_name + '_vs.txt',
	'MAP_popularity.txt',
	'item_listening_lengths.txt',
	'user_history_lengths.txt'
]

only_files = [f for f in listdir(dirname) if isfile(join(dirname, f))]
text_files = [f for f in only_files if f.endswith('.txt')]
result_files = [f for f in text_files if f not in exclude_files]
not_hybrids = [f for f in result_files if not f.startswith('MAP_hybrid')]
with_mnn = [f for f in not_hybrids if "mnn=" in f]

results = {}

for file in with_mnn:
	if not filter in file:
		continue
	try:
		ev_meth, algo, method, construction, alpha, mnn, q = file[:-4].split('_')
	except Exception, e:
		print "Error for:", file
		print str(e)
	alpha = "%.2f" % float(alpha.split('=')[1])
	q = q.split('=')[1]
	if ev_meth not in results:
		results[ev_meth] = {}
	if algo not in results[ev_meth]:
		results[ev_meth][algo] = {}
	if method not in results[ev_meth][algo]:
		results[ev_meth][algo][method] = {}
	if construction not in results[ev_meth][algo][method]:
		results[ev_meth][algo][method][construction] = {}
	if mnn not in results[ev_meth][algo][method][construction]:
		results[ev_meth][algo][method][construction][mnn] = {}
	if alpha not in results[ev_meth][algo][method][construction][mnn]:
		results[ev_meth][algo][method][construction][mnn][alpha] = {}
	if q not in results[ev_meth][algo][method][construction][mnn][alpha]:
		results[ev_meth][algo][method][construction][mnn][alpha][q] = {}
		
	f = open(join(dirname, file), 'r')
	fields = f.readline().rstrip().split(' ')
	results[ev_meth][algo][method][construction][mnn][alpha][q]['MAP'] = float(fields[1])
	fields = f.readline().rstrip().split(' ')
	if fields[0] == 'MrecR':
		results[ev_meth][algo][method][construction][mnn][alpha][q]['MrecR'] = float(fields[1])
	else:
		results[ev_meth][algo][method][construction][mnn][alpha][q]['MrecR'] = 0.0
	f.close()

for ev_meth in results:
	for algo in results[ev_meth]:
		for method in results[ev_meth][algo]:
			for construction in results[ev_meth][algo][method]:
				for mnn in results[ev_meth][algo][method][construction]:
					current = results[ev_meth][algo][method][construction][mnn]
					print '---------------------------------------------\n'
					print ev_meth, algo, method, construction, mnn, ':\n'
					print '---------------------------------------------\n'
					Qs = sorted(current[current.keys()[0]])
					print '\t' + '             '.join(Qs) + '\n'
					for alpha in sorted(current):
						print alpha + '\t' + '  '.join(["%.4f(%.4f)" % (current[alpha][q]['MAP'],current[alpha][q]['MrecR'])  for q in Qs]).replace('0.', '.') + '\n'
					
					maximum = 0.
					for alpha in sorted(current):
						for q in Qs:
							maximum = max(maximum, current[alpha][q]['MAP'])
					
					if algo == 'ucf':
						algorithm = 'User Based CF'
					elif algo == 'ucf2':
						algorithm = 'User Based CF 2'
					elif algo == 'icf':
						algorithm = 'Item Based CF'
					
					if ds_name == 'kaggle_visible_evaluation_triplets':
						ds = 'Dataset\\_1'
					elif ds_name == 'sample_1':
						ds = 'Dataset\\_2'
					elif ds_name == 'sample_2':
						ds = 'Dataset\\_3'

					with open("%s/%s_%s_%s_%s_%s.tex"%(dirname, ev_meth, algo, method, construction, mnn), 'w') as f_out:
						f_out.write("\\begin{table}\n")
						f_out.write("\\begin{center}\n")
						f_out.write("\\begin{tabular}{ | l ||")
						for q in Qs:
							f_out.write(" c |")
						f_out.write("}\n")
						f_out.write("\\hline\n")
						f_out.write('\\textbf{$\\alpha$} & ' + ' & '.join(["\\textbf{q=%s}"%(q) for q in Qs]) + ' \\\\\n')
						f_out.write("\\hline\n")
						for alpha in sorted(current):
							f_out.write('\\textbf{' + alpha + '}' + ' & ' + ' & '.join(["\\textbf{%.4f}$\\bullet$" % (current[alpha][q]['MAP']) if (current[alpha][q]['MAP'] == maximum) else "%.4f" % (current[alpha][q]['MAP'])  for q in Qs]) + '\\\\\n')
							f_out.write("\\hline\n")
						f_out.write("\\end{tabular}\n")
						f_out.write("\\caption{%s, %s, distance=%s, %s, max neighbours = %s, MAP for different values of $\\alpha$ and q}\n"%(ds, algorithm, method, construction, mnn.replace("mnn=", "")))
						f_out.write("\\label{table:MAP_%s_%s_%s_%s_%s}\n"%(ds.replace("\\", ""), algo, method, construction, mnn))
						f_out.write("\\end{center}\n")
						f_out.write("\\end{table}\n")
