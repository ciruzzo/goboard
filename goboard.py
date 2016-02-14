import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import copy

class goboard(object):
	""" taken from http://stackoverflow.com/questions/24563513/drawing-a-go-board-with-matplotlib"""
	def __init__(self):
		fig = plt.figure(figsize=[8,8], facecolor=(1,1,.8))
		self.ax = fig.add_subplot(111, xticks=range(19), yticks=range(19), axis_bgcolor='none', position=[.1,.1,.8,.8])
		self.ax.grid(color='k', linestyle='-', linewidth=1)
		self.ax.xaxis.set_tick_params(bottom='off', top='off', labelbottom='off')
		self.ax.yaxis.set_tick_params(left='off', right='off', labelleft='off')

		self.black_stone = mpatches.Circle((0,0), .45, facecolor='k', edgecolor=(.8,.8,.8, 1), linewidth = 2, clip_on=False, zorder=10)
		self.white_stone = copy.copy(self.black_stone)
		self.white_stone.set_facecolor((.9, .9, .9))
		self.white_stone.set_edgecolor((.5, .5, .5))

		self.black_last = copy.copy(self.black_stone)
		self.black_last.set_edgecolor('r')
		self.white_last = copy.copy(self.white_stone)
		self.white_last.set_edgecolor('r')

	def put_black(self,pos,last=False):
		if last:
			s1 = copy.copy(self.black_last)
		else:
			s1 = copy.copy(self.black_stone)
		s1.center = pos
		self.ax.add_patch(s1)
	def put_white(self,pos,last=False):
		if last:
			s2 = copy.copy(self.white_last)
		else:	
			s2 = copy.copy(self.white_stone)
		s2.center = pos
		self.ax.add_patch(s2)
	def put_stone(self, color, pos, last=False):
		if color == 'B':
			self.put_black(pos, last)
		else:
			self.put_white(pos, last)

def trans(node):
	import string
	d = {}
	for i,a in enumerate(list(string.ascii_lowercase)):
		d[a] = i
	color = node[1]
	pos = (d[node[3]], d[node[4]])
	return color,pos

def ismove(node):
	if len(node) != 6 or node[0]!= ';' or (node[1] != 'B' and node[1] != 'W'):
		return False
	else:
		return True 

def test():
	g = goboard()
	print (g.__doc__)
	for a,b in zip(range(19),range(19)):
		g.put_black((a,b), last=True)
	for a,b in zip(range(17,0,-1),range(19)):
		g.put_white((a,b), last=False)
	for a,b in zip(range(18,0,-1),range(19)):
		g.put_white((a,b), last=True)
	plt.show()

if __name__ == '__main__':
	color,pos =	trans(';B[ec]')
	g = goboard()
	g.put_stone(color, pos)
	plt.show()
