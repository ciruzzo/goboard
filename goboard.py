import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import copy
import string
import sys

sys.path.append('sgflib1.0')
from sgflib import *

# abc to 123 map
dict = {}
for i,a in enumerate(list(string.ascii_lowercase)):
	dict[a] = i

class goboard(object):
	""" taken from http://stackoverflow.com/questions/24563513/drawing-a-go-board-with-matplotlib"""
	def __init__(self):
		fig = plt.figure(figsize=[8,8], facecolor=(1,1,.8))
		self.ax = fig.add_subplot(111, xticks=range(19), yticks=range(19), axis_bgcolor='none', position=[.1,.1,.8,.8])
		self.ax.grid(color='k', linestyle='-', linewidth=1)
		self.ax.xaxis.set_tick_params(bottom='off', top='off', labelbottom='off')
		self.ax.yaxis.set_tick_params(left='off', right='off', labelleft='off')

		self.stone = {}
		self.stone['B'] = mpatches.Circle((0,0), .45, facecolor='k', linewidth = 2, clip_on=False, zorder=10)
		self.stone['W'] = mpatches.Circle((0,0), .45, facecolor='w', linewidth = 2, clip_on=False, zorder=10)

	def put_stone(self, color, pos, last=False):
		s = copy.copy(self.stone[color])
		if last: s.set_edgecolor('r')
		s.center = pos
		self.ax.add_patch(s)

def sgfmove(file):
	def get_move(s):
		res = []
		while True:
			l = s.find('[')
			r = s.find(']')
			if l == -1 or r == -1: break
			p = s[l+1:r]
			if len(p) > 0: res.append(p)
			s = s[r+1:]
		return res

	def get_color(s):
		l = s.find('[')
		if l == -1: return ''
		else: return s[:l]
			
	def trans(node):
		color = get_color(node)
		p = get_move(node)
		
		ret = False
		if color == 'B' or color == 'W':
			ret = True
		elif color == 'AB':
			color = 'B'	
			ret = True
		elif color == 'AW':
			color = 'W'	
			ret = True
		else:
			pass
	
		if ret == True and len(p) > 0:
			pos = [(dict[x[0]], dict[x[1]]) for x in p]
			return True, color, pos
		else:
			return False, '', []

	src = open(file, 'r').read()
	col = SGFParser(src).parse()
	c = col.cursor()

	move = []
	while True:
		move = move+[(col,p) for ok,col,p in map(trans, map(str,c.node)) if ok]
		if c.atEnd: break
		c.next()
	return move

if __name__ == '__main__':
	color,pos =	trans(';B[ec]')
	g = goboard()
	g.put_stone(color, pos)
	plt.show()
