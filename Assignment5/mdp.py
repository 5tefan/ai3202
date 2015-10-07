#!/bin/python

# implemented in Python 2.7 by Stefan Codrescu, see 
# http://www.policyalmanac.org/games/aStarTutorial.htm
# http://www.microveggies.com/csci/index.php/9-csci-3202-lecture-notes/28-lecture-7-8-informed-search-a-heuristics
# for an intro to A* search

import sys
import os
import math
import copy
import numpy

numpy.set_printoptions(linewidth=500, precision=3)

class World(): 
	# this class deals with the world from the txt file, use Utility_world when the matrix representation
	# with utility values already exists
	def __init__(self, world_file):
		try:
			if os.path.isfile(world_file): ##if input is a filename, import it
				temp = open(world_file)
				self.world = [ x.split(" ") for x in temp.read().split("\n") if x ] 	# read file into a matrix of values
			else:
				raise ValueError
		except ValueError:					## otherwise it better be the matrix of our world already created
			self.world = world_file
		self.size = ( len(self.world)-1, len(self.world[0])-1 ) 				# row x cols (0 indexed) matrix style notation

	def get_size(self):
		return self.size
	
	def get_loc(self, loc):		# matrix value at loc, 0 is empty, 1 is mountain, 2 is wall
		return int(self.world[loc[0]][loc[1]])									

	def get_reward(self, loc):
		if (not self.valid_loc(loc)):
			return 0
		point = self.get_loc(loc)
		if point == 1:		# is mountain
			return -1.
		elif point == 2:		# is a wall
			return 0
		elif point == 3:		# is a snake
			return -10.
		elif point == 4: 		# is a barn
			return 1.
		else:
			return point
	
	def get_adjacent(self, loc):
		ret = []
		for j in [-1, 1]:		# this gives the (up to) 4 valid moves l, r, u, d possible from loc
			ret.append( (loc[0], loc[1]+j) )
			ret.append( (loc[0]+j, loc[1]) )
		# skip this for now because dont need cost in mdp
		# then filter them to make sure they are valid, ie no walls or out of bounds
		# and also add the correct cost
		return [(x, self.get_loc(x)) for x in ret if self.valid_loc(x)]

	def valid_loc(self, loc):			#check if within bounds of world
		if loc[0] < 0 or loc[0] > self.size[0] or loc[1] < 0 or loc[1] > self.size[1]: 
			return False
		if self.get_loc(loc) == 2:			#also see if it is a wall
			return False
		return True

	def set_world(self, world):
		try: 
			if os.path.isfile(world): ##if input is a filename, import it
				temp = open(world)
				self.world = [ x.split(" ") for x in temp.read().split("\n") if x ] 	# read file into a matrix of values
		except:							## otherwise it better be the matrix of our world already created
			self.world = world
		self.size = ( len(self.world)-1, len(self.world[0])-1 ) 				# row x cols (0 indexed) matrix style notation

class Utility_World(World):
	def __init__(self, world):
		World.__init__(self, world)

	def valid_loc(self, loc):
		if loc[0] < 0 or loc[0] > self.size[0] or loc[1] < 0 or loc[1] > self.size[1]: 
			return False
		if self.get_loc(loc) == 0:			#also see if it is a wall
			return False
		return True
		
	def get_adjacent(self, loc):
		ret = []
		for j in [-1, 1]:		# this gives the (up to) 4 valid moves l, r, u, d possible from loc
			ret.append( (loc[0], loc[1]+j) )
			ret.append( (loc[0]+j, loc[1]) )
		# skip this for now because dont need cost in mdp
		# then filter them to make sure they are valid, ie no walls or out of bounds
		# and also add the correct cost
		return [(x, -self.get_loc(x)) for x in ret if self.valid_loc(x)]
		

class Heuristic():
	def __init__(self, world, goal=None):
		self.world = world
		self.size = self.world.get_size()
		self.goal = goal

	def set_goal(self, goal): 	# helper fn
		self.goal = goal

	def est(self, loc):			# compute the heuristic estimate for a given location
		return 0;

class Heuristic_ManhattenDist(Heuristic): 			#subclass Heuristic		
	def __init__(self, world, goal=None):
		Heuristic.__init__(self, world, goal)

	def est(self, loc):							#override with new estimate
		return abs(self.goal[0] - loc[0]) + abs(self.goal[1] - loc[1])

class AStar():
	def __init__(self, world, heuristic):
		self.world = world
		self.heuristic = heuristic

	def search(self, start, goal):
		self.heuristic.set_goal(goal)
		olist = []; clist = []								# lists containing open and closed nodes
		olist.append([start, start, 0, 0])					# the format of olist entries is [selfloc, parentloc, heuristic+upto, uptocost]
		while (len(olist) > 0):
			node = self.get_min_cost(olist)					# get the minimum heuristic cost open nodes
			olist.remove(node)								# remove that node from the open list
			loc, parent, heuristic, cost = node				# explode values to more descriptive names
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
				print "Number of locations evaluated: %d" % len(clist)   # <-- ugh, this line is ugly :(
				path = []								# hold the path as we go back through the closed list to see what path
				while (loc != start):					# go until we find the start
					loc, parent, _, _ = node			# explode values to more descriptive names again, dont care about cost and heuristic along way
					path.append(loc)					# add loc to path, 
					cindex = [_[0] for _ in clist].index(parent)	# find location of parent in closed
					node = clist[cindex] 				# set node to parent entry in closed list for next loop
				return [path[::-1], cost]				# return the path (need to reverse to get start to goal order and total cost)
		return [None, None] 		# in the case that no path was found

	def get_min_cost(self, olist):
		# find the minimum heuristic value in open list
		res = olist[0]
		for entry in olist:
			if entry[2] < res[2]:
				res = entry
		return res

class MDP():
	def __init__(self, world, epsilon):
		self.epsilon = epsilon
		self.gamma = 0.9
		self.world = world
		self.size = self.world.get_size()
		self.debug = False ##use for debugging


	def value_iterate(self):
		u = [] 							# utilities for all the states
		up = numpy.zeros((self.size[0] + 1, self.size[1] + 1))		# u' or uprime, next iteration utilities
		if self.debug:
			direction = numpy.zeros((self.size[0] + 1, self.size[1] + 1))
		sigma = float("Inf") 	# max change of any utility during an iteration
		while ( sigma >= self.epsilon * ( 1 - self.gamma) / self.gamma ):
			u = copy.deepcopy(up);
			up = numpy.zeros((self.size[0] + 1, self.size[1] + 1))		
			sigma = 0
			for state in self.get_all_valid_states():
				moves = self.get_adjacent(state)
				max_move = ( moves[0], float("-Inf") )
				for move in moves:
					diff = ( move[0] - state[0], move[1] - state[1] ) 	# which direction move are we going?
																	# this next line gives the two directions left and
																	# right the direction we went along with the prob
																	# that we move that direction
					consider = [ [ ( int( not (diff[0] & 1) ) * i, int( not (diff[1] & 1) ) * i ), .1] for i in [-1, 1] ]
					consider.append( [ diff, .8 ] )					# add the original move (prob .8)
																	# then calculate absolute pos these moves yeild
					consider = [ [ (state[0] + con[0][0], state[1] + con[0][1]), con[1] ] for con in consider ] 
																	# find the utility of this state
					move_utility = sum( [ con[1] * u[ con[0] ] for con in consider if self.world.valid_loc(con[0]) ] )
					if (move_utility > max_move[1]):						# update max uitlity if necessary
						max_move = ( move, move_utility )

				max_utility = self.world.get_reward( state ) + self.gamma * max_move[1]
				up[ state ] = max_utility

				if self.debug:
					diff = ( max_move[0][0] - state[0], max_move[0][1] - state[1] ) 	# which direction move are we going?
					if (diff == (-1, 0)):
						direction[ state ] = 0
					elif (diff == (0, 1)): 
						direction[ state ] = 1
					elif (diff == (1, 0)): 
						direction[ state ] = 2
					elif (diff == (0, -1)): 
						direction[ state ] = 3

				if (abs(up[state] - u[state]) > sigma):
					sigma = abs(up[state] - u[state])
		if self.debug:
			print direction
		return up

	def get_all_valid_states(self):
		ret  = []
		for i in range(self.size[0]+1):
			for j in range(self.size[1]+1):
				if self.world.valid_loc( (i, j) ):
					ret.append( (i, j) )
		return ret
				
	def get_adjacent(self, loc):
		ret = []
		for j in [-1, 1]:		# this gives the (up to) 4 valid moves l, r, u, d possible from loc
			ret.append( (loc[0], loc[1]+j) )
			ret.append( (loc[0]+j, loc[1]) )
		return ret

if __name__ == "__main__":
	usage = "python %s <map file> [epsilon]" % sys.argv[0] 
	try:
		which_map = sys.argv[1]
	except IndexError:
		print usage
	try:
		epsilon = float(sys.argv[2])
	except IndexError:
		epsilon = float(1./2.)

	w = World(which_map)
	m = MDP(w, epsilon)
	up = m.value_iterate()
	
	print up
	nw = Utility_World(up)
	h = Heuristic_ManhattenDist(nw)
	a = AStar(nw, h)
	path, cost = a.search( (7, 0), (0, 9) )
	print "Path found: %s\nPath cost: %d" % (path, cost)
	

	


