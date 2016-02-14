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
		move.append(str(c.node)) 
		if c.atEnd: break
		c.next()

	move = filter(go.ismove, move)
	print len(move), move
	g = go.goboard()
	for i,m in enumerate(move):
		c,p = go.trans(m)
		g.put_stone(c,p, i == len(move)-1)
	plt.show()
	
main()
