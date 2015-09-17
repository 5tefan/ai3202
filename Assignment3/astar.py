import sys
import math

class World():
	def __init__(self, world_file):
		temp = open(world_file)
		self.world = [ x.split(" ") for x in temp.read().split("\n") if x ] 	# read file into a matrix of values
		self.size = ( len(self.world)-1, len(self.world[0])-1 ) 				# row x cols (0 indexed) matrix style notation

	def get_size(self):
		return self.size
	
	def get_loc(self, loc):
		# matrix value at loc, 0 is empty, 1 is mountain, 2 is wall
		return int(self.world[loc[0]][loc[1]])									

	def get_adjacent(self, loc):
		ret = []
		# this gives an initial result of the 8 grid points around loc
		for j in [-1, 1]:
			ret.append( [ (loc[0]+j, loc[1]), 10 ] )
			ret.append( [ (loc[0], loc[1]+j), 10 ] )
			for i in [-1, 1]:
				ret.append( [ (loc[0]+j, loc[1]+i), 14 ] )

		# then filter them to make sure they are valid, ie no walls or out of bounds
		return [(x[0], x[1] + self.get_loc(x[0])*10) for x in ret if self.valid_loc(x[0])]
	

	def valid_loc(self, loc):
											#check if within bounds of world
		if loc[0] < 0 or loc[0] > self.size[0] or loc[1] < 0 or loc[1] > self.size[1]: 
			return False
		if self.get_loc(loc) == 2:			#also see if it is a wall
			return False
		return True

class Heuristic():
	def __init__(self, world, goal=None):
		self.world = world
		self.size = self.world.get_size()
		self.goal = goal

	def est(self, loc):
		# compute the heuristic estimate for a given location
		return abs(self.goal[0] - loc[0]) + abs(self.goal[1] - loc[1])

	def set_goal(self, goal): #helper fn
		self.goal = goal

class Heuristic_SqrtDist(Heuristic): 			#subclass Heuristic		
	def __init__(self, world, goal=None):
		Heuristic.__init__(self, world, goal)

	def est(self, loc):							#override with new estimate
		idist = self.goal[0] - loc[0]
		jdist = self.goal[1] - loc[1]
		return math.sqrt( idist * idist + jdist * jdist )

class AStar():
	def __init__(self, world, heuristic):
		self.world = world
		self.heuristic = heuristic

	def search(self, start, goal):
		self.heuristic.set_goal(goal)
		olist = []											# list of open nodes
		clist = []											# list of closed nodes
		#the format of olist entries is [selfloc, parentloc, heuristic+upto, uptocost]
		olist.append([start, start, 0, 0])
		while (len(olist) > 0):
			node = self.get_min_cost(olist)					# get the minimum heuristic cost open nodes
			olist.remove(node)								# remove that node from the open list
			loc, parent, heuristic, cost = node				# explode values to more descriptive names
	#		print olist
	#		print "node %s" % node
			if (loc != goal):								# go until we find the goal
				clist.append(node)							# add current node to closed since we are evaluating it
				for adj in self.world.get_adjacent(loc):			# evaluate all valid nodes adjacent to current
					adjloc, movecost = adj							# self.world.get_adj returns valid adjacent nodes and the move cost 
																	# 	associated with moving there from current loc
					try:											# hacky way to see if adjloc is in the closed list
						[ _[0] for _ in clist].index(adjloc)
					except ValueError:								# if not in the closed list, then evaluate this adjacent node
						adjheuristic = self.heuristic.est(adjloc)	# get the heuristic estimate for this adjacent node
						adjnode = [adjloc, loc, adjheuristic + cost + movecost, cost + movecost] # create the new open list entry
						try:												# using the same shortcut above to see if our adjloc is 
							index = [ _[0] for _ in olist].index(adjloc)	# already in the open list.
							if olist[index][2] > adjnode[2]:				# if so, replace it if cost is less from our new angle
								olist[index][2] = adjnode
						except ValueError:
							olist.append(adjnode)						# otherwise it wasnt in the open list and needs to be added
			else: 										# executed after goal is found, this finds what the final path was
				path = []								# hold the path as we go back through the closed list to see what path
				while (loc != start):					# go until we find the start
					loc, parent, _, _ = node			# explode values to more descriptive names again, dont care about cost and heuristic along way
					path.append(loc)					# add loc to path, 
					cindex = [_[0] for _ in clist].index(parent)	# find location of parent in closed
					node = clist[cindex] 				# set node to parent entry in closed list for next loop
				return [path[::-1], cost]				# return the path (need to reverse to get start to goal order and total cost)

	def get_min_cost(self, olist):
		# find the minimum heuristic value in open list
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
		if which_heuristic not in [0, 1]: raise IndexError("invalid heuristic")
	except IndexError:
		which_heuristic = 0

	w = World(which_map)

	if which_heuristic == 0:
		h = Heuristic(w)
	elif which_heuristic == 1:
		h = Heuristic_SqrtDist(w)

	a = AStar(w, h)
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
	

