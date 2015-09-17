import sys
import math

class World():
	def __init__(self, world_file):
		temp = open(world_file)
		self.world = [ x.split(" ") for x in temp.read().split("\n") if x ]
		self.size = ( len(self.world)-1, len(self.world[0])-1 )

	def get_size(self):
		return self.size
	
	def get_loc(self, loc):
		#get the type of obstacle at loc
		return int(self.world[loc[0]][loc[1]])

	def get_adjacent(self, loc):
		ret = []
		# this gives an initial result of the 8 grid points around loc
		for j in [-1, 1]:
			ret.append( [ (loc[0]+j, loc[1]), 10 ] )
			ret.append( [ (loc[0], loc[1]+j), 10 ] )
			for i in [-1, 1]:
				ret.append( [ (loc[0]+j, loc[1]+i), 14 ] )

		# then filter them to make sure they are valid
		return [x for x in ret if self.valid_loc(x[0])]
	

	def valid_loc(self, loc):
		#check if within bounds of world
		if loc[0] < 0 or loc[0] > self.size[0] or loc[1] < 0 or loc[1] > self.size[1]: 
			return False
		#also see if it is a wall
		if self.get_loc(loc) == 2:
			return False
		return True

class Heuristic():
	def __init__(self, world, goal=None):
		self.world = world
		self.size = self.world.get_size()
		self.goal = goal

	def est(self, loc):
		return abs(self.goal[0] - loc[0]) + abs(self.goal[1] - loc[1])

	def set_goal(self, goal):
		self.goal = goal

class Heuristic_SqrtDist(Heuristic):
	def __init__(self, world, goal=None):
		Heuristic.__init__(self, world, goal)

	def est(self, loc):
		idist = self.goal[0] - loc[0]
		jdist = self.goal[1] - loc[1]
		return math.sqrt( idist * idist + jdist * jdist )

class AStar():
	def __init__(self, world, heuristic):
		self.world = world
		self.heuristic = heuristic

	def search(self, start, goal):
		self.heuristic.set_goal(goal)
		olist = []
		clist = []
		#[self, parent, cost, uptocost]
		olist.append([start, start, 0, 0])
		while (len(olist) > 0):
			node = self.get_min_cost(olist)
			olist.remove(node)
			loc, parent, heuristic, cost = node
	#		print olist
	#		print "node %s" % node
			if (loc != goal):
				clist.append(node)
				for adj in self.world.get_adjacent(loc):
					adjloc, movecost = adj
					try:
						[ _[0] for _ in clist].index(adjloc)
					except ValueError:
						adjheuristic = self.heuristic.est(adjloc)
						adjnode = [adjloc, loc, adjheuristic + cost + movecost, cost + movecost]
						try:
							index = [ _[0] for _ in olist].index(adjloc)
							if olist[index][2] > adjnode[2]:
								olist[index][2] = adjnode
						except ValueError:
							olist.append(adjnode)
			else:
				path = []
				while (loc != start):
					loc, parent, heuristic, cost = node
					path.append(loc)
					cindex = [_[0] for _ in clist].index(parent)
					node = clist[cindex]
				return path[::-1]

	def get_min_cost(self, olist):
		res = olist[0]
		for entry in olist:
			if entry[2] < res[2]:
				res = entry
		return res


	

if __name__ == "__main__":
	usage = "python %s <map file> [heuristic]" % sys.argv[0] 
	try:
		which_map = sys.argv[1]
	except IndexError:
		print usage
	try:
		which_heuristic = sys.argv[2]
	except IndexError:
		which_heuristic = 0

	w = World(which_map)
	h = Heuristic(w)
	a = AStar(w, h)
	print a.search( (7, 0), (0, 9) )

	
	h2 = Heuristic_SqrtDist(w)
	b = AStar(w, h2)
	print a.search( (7, 0), (0, 9) )

"""
	print "testing world"
	w = World(which_map)
	print w.get_size()
	print w.get_loc( (0,0) )
	print w.get_adjacent( (0,0) )
	print w.get_adjacent( (3,3) )
	print w.get_adjacent( (8, 9) )
	print w.get_adjacent( (8,1) )
	print w.valid_loc( (7, 2) )
	print w.get_loc( (7, 2) )
	print w.world[7]
		

	print "testing heuristic"
	h = Heuristic(w, [0, w.get_size()[1]])
	print h.est((0, 0))
	print h.est((7, 0))
	print h.est((3, 3))
	print h.est((0, 9))
"""
	

