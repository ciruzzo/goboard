import sys
import goboard as go


if __name__ == '__main__':
	import matplotlib.pyplot as plt

	if len(sys.argv) < 2:
		print "usage: %s sgf_file (limit)" % sys.argv[0]
		exit(1)

	move = go.sgfmove(sys.argv[1])

	if len(sys.argv) > 2:
		num = int(sys.argv[2])
	else:
		num = len(move)

	move = move[:num]

	g = go.goboard()
	[[g.put_stone(c,x,i==len(move)-1) for x in p] for i,(c,p) in enumerate(move)]
	plt.show()
	
