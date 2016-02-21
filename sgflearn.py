import sys
import os
import goboard as go
import pickle
import matplotlib.pyplot as plt

def create_data_from_sgf(pfile):
	if len(sys.argv) < 2:
		print "usage: %s sgf_dir" % sys.argv[0]
		exit(1)

	data = {}
	for path, dirs, files in os.walk(sys.argv[1]):
		for file in files:
			if ".sgf" in file:
				f = path+'/'+file
				try:
					move = go.sgfmove(f)
					data[f] = move[:10]
				except:
					print "failed", f

	with open(pfile, 'wb') as handle:
	  pickle.dump(data, handle)

	print "number of files", len(data)
	
def read_pickle_data(pfile):
	with open(pfile, 'rb') as handle:
	  data = pickle.load(handle)

	for f in data.keys():
		print f, data[f]
	print "number of loaded data: ", len(data)


def create_array(seq):
	b = [0] * (19*19)
	for (c,m) in seq:
		if c == 'B':
			x = 1
		elif c == 'W':
			x = 2
		else:
			print "bad color", c
			exit(1)
		for px,py in m:
			b[px*19+py] = x
	return b


if __name__ == '__main__':
	pfile = 'data.pickle'
#	create_data_from_sgf(pfile)
	read_pickle_data(pfile)
	

#	g = go.goboard()
#	[[g.put_stone(c,x,i==len(move)-1) for x in p] for i,(c,p) in enumerate(move)]
#	plt.show()
	
