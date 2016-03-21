import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import copy
import string
import sys
sys.path.append('sgflib1.0')
from sgflib import *

# abc... to 123... map
dict = {}
for i,a in enumerate(list(string.ascii_lowercase)):
	dict[a] = i

class goboard(object):
	""" taken from http://stackoverflow.com/questions/24563513/drawing-a-go-board-with-matplotlib"""
	def __init__(self):
		boardcolor = (1,1,.8)
		fig = plt.figure(figsize=[8,8], facecolor=boardcolor)
		self.ax = fig.add_subplot(111, xticks=range(19), yticks=range(19), axis_bgcolor='none', position=[.1,.1,.8,.8])
		self.ax.grid(color='k', linestyle='-', linewidth=1)
		self.ax.xaxis.set_tick_params(bottom='off', top='off', labelbottom='off')
		self.ax.yaxis.set_tick_params(left='off', right='off', labelleft='off')

		self.stone = {}
		self.stone['B'] = mpatches.Circle((0,0), .45, facecolor='k', linewidth = 2, clip_on=False, zorder=10)
		self.stone['W'] = mpatches.Circle((0,0), .45, facecolor='w', linewidth = 2, clip_on=False, zorder=10)
		self.stone['T'] = mpatches.Circle((0,0), .45, facecolor=boardcolor, linewidth = 2, clip_on=False, zorder=10, edgecolor='g')

		self.bd = [['e' for i in range(19)] for j in range(19)]
		self.take = {}
		self.take['B'] = 0
		self.take['W'] = 0

	def put_stone(self, color, pos, last=False):
		s = copy.copy(self.stone[color])
		if last: s.set_edgecolor('r')
		s.center = pos
		self.ax.add_patch(s)
		self.enter_stone(color,pos)
		if color != 'T':
			self.take[color] += self.try_take(color,pos)
		if last:
			print "agehama: black %d, white %d" % (self.take['B'], self.take['W'])

	def print_status(self):
		print self.bd
	def enter_stone(self,color,pos):
		self.bd[pos[0]][pos[1]] = color
	def neighbor(self, p):
		for vx,vy in [[1,0],[0,1],[-1,0],[0,-1]]:
			x,y = p[0]+vx, p[1]+vy
			if x < 0 or y < 0 or x > 18 or y > 18:
				continue
			yield [x,y]
	def color(self, p):
		return self.bd[p[0]][p[1]]
	
	def count_dame(self, p, visited, col):
		res = 0
		for q in self.neighbor(p):
			cq = self.color(q)
			if cq == col:
				if visited[q[0]][q[1]] == False:
					visited[q[0]][q[1]] = True
					res += self.count_dame(q, visited, col)
			elif cq == 'e':
				res += 1
		return res
	
	def take_stone(self, p, visited, col):
		res = 0
		for q in self.neighbor(p):
			cq = self.color(q)
			if cq == col:
				if visited[q[0]][q[1]] == False:
					visited[q[0]][q[1]] = True
					res += self.take_stone(q, visited, col)
			res += 1
			self.put_stone('T', p)
			self.enter_stone('e',p)
		return res
		
	def try_take(self,color,p):
		taken = 0
		for q in self.neighbor(p):
			# could be already taken, along with other stones	
			cq = self.color(q)
			if (cq == 'B' or cq == 'W') and (cq != color):
				v = [[False for i in range(19)] for j in range(19)]
				v[q[0]][q[1]] = True
				dame = self.count_dame(q, v, cq)
				if dame == 0:
					for i in range(19):
						for j in range(19):
							if v[i][j]:
								self.put_stone('T',[i,j])
								self.enter_stone('e',[i,j])
								taken += 1
		return taken

# returns move(point,color) from a file
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

def test(move, point, shouldbe):
	g = goboard()
	for c,p in move:
		[g.put_stone(c,x) for x in p]

	v = [[False for i in range(19)] for j in range(19)]
	v[point[0]][point[1]] = True
	
	dame = g.count_dame(point, v, 'B')
	print "dame for", point, dame , "should be", shouldbe

	if dame == 0:
		v = [[False for i in range(19)] for j in range(19)]
		v[point[0]][point[1]] = True
		g.take_stone(point, v, 'B')
	plt.show()

if __name__ == '__main__':
#	move, shouldbe = [('B', [(16,0)]), ('B', [(16, 3)]), ('W', [(3, 15)]), ('B', [(2, 3)]), ('W', [(15, 15)]), ('B', [(16, 13)]), ('W', [(13, 16)]), ('B', [(15, 9)]), ('W', [(13, 3)]), ('B', [(15, 2)]), ('W', [(4, 3)])], 0
	move1, shouldbe = [('B',[(1,0)]),('W',[(1,1)]),('B',[(2,0)]),('B',[(2,1)]),('W',[(2,2)]), ('W',[(3,0)]),('W', [(3,1)])], 1
#	move2, shouldbe = [('B',[(1,0)]),('W',[(1,1)]),('B',[(2,0)]),('B',[(2,1)]),('W',[(3,0)]),('W', [(3,1)])], 2

	test(move1, (1,0), shouldbe)

