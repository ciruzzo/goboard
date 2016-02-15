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

	src = open(sys.argv[1], 'r').read()
	col = SGFParser(src).parse()
#	cstr = str(col)
#	m = col[0].mainline()
	c = col.cursor()

	move = []
	while True:
		move = move+[(col,p) for ok,col,p in map(go.trans, map(str,c.node)) if ok]
		if c.atEnd: break
		c.next()

	g = go.goboard()
	[[g.put_stone(c,x,i==len(move)-1) for x in p] for i,(c,p) in enumerate(move)]
	plt.show()
	
main()
