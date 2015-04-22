import sys, getopt

def main(argv):
	inputfile = ''
	n = 10
	
	try:
		opts, args = getopt.getopt(argv, "hn:")
	except getopt.GetoptError:
		print 'head.py -n <lines> file'
		sys.exit(2)
		
	for opt, arg in opts:
		if opt == '-h':
			print 'head.py -n <lines> file'
		elif opt == '-n':
			n = int(arg)
	
	inputfile = args[0]
	
	f_in = open(inputfile, 'r')
	for i in range (0, n):
		print(f_in.readline()),
	f_in.close()


if __name__ == "__main__":
	main(sys.argv[1:])