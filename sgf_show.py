import sys
sys.path.append('sgflib1.0')
from sgflib import *

def main():
	import sys
	import matplotlib.pyplot as plt
	import goboard as go

	if len(sys.argv) < 2:
		print "usage: %s sgf_file" % sys.argv[0]
		exit(1)
	srcpath = sys.argv[1]

	src = open(srcpath, 'r')
	sgfdata = src.read()
	col = SGFParser(sgfdata).parse()
	cstr = str(col)
	m = col[0].mainline()
	c = col.cursor()

	move = []
	while True:
		for m in map(str,c.node):
			ok,col,p = go.trans(m)
			if ok:
				move.append((col,p))
		
		if c.atEnd: break
		c.next()

	print len(move), move
	g = go.goboard()
	for i,m in enumerate(move):
		c,p = m
		for x in p:
			g.put_stone(c,x, i == len(move)-1)
	plt.show()
	
main()
