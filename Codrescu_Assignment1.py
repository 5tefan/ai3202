#!/bin/python
# implemented with Python 2.7

"""	Stefan Codrescu stco8643
	Assignment 1: A review of basic data structures.
	CSCI 3202 Introduction to Artificial Intelligence
"""


import random


###########################################
# QUEUE
from queue import CSCI3202_Queue as q

# initialize
my_q = q()

# put integers 0 .. 19 into the queue
for i in range(20):
	my_q.put(i)

# get integers out of the queue
while not my_q.empty():
	print my_q.get()


###########################################
# STACK
from stack import CSCI3202_Stack as stack

# intialize
my_stack = stack()

#push integers 0 .. 19 to stack
for i in range(20):
	my_stack.push(i)

# pop integers from the stack
while my_stack.checkSize():
	print my_stack.pop()


###########################################
# BINARY TREE
from binary_tree import CSCI3202_Binary_Tree as bt

#initialize a binary tree with root node value -1
# and bt_contents to keep track of what we have added
# to the tree
bt_contents = []
my_bt = bt(-1)
bt_contents.append(-1)

# add integers 0 .. 9 to the tree and store
# what we have inserted with bt_contents
for i in range(5):
	print "adding %i to parent %i" % (i, bt_contents[-1])
	if my_bt.add(i, bt_contents[-1]):
		bt_contents.append(i)
	print "adding %i to parent %i" % (i+5, bt_contents[-2])
	if my_bt.add(i+5, bt_contents[-2]):
		bt_contents.append(i+5)

print "\nprinting tree: "
my_bt.printTree()
print " "

# using use the last 5 things we added, in reverse order, 
# remove them from the tree. This order will ensure that 
# the items can be removed because none of them will have
# children in this order
for i in bt_contents[-5:][::-1]:
	print "removing %i" % (i)
	if my_bt.delete(i):
		bt_contents.remove(i)

print "\nprinting tree: "
my_bt.printTree()
print " "


###########################################
# GRAPH
from graph import CSCI3202_Graph as g

#initiailze
my_g = g()

# add vertexes with values 0 .. 49
for i in range(50):
	my_g.addVertex(i)

# add edges between randomly selected vertecies
for i in range(200):
	rand_val1 = random.randint(0, 49)
	rand_val2 = random.randint(0, 49)
	my_g.addEdge(rand_val1, rand_val2)

#select 5 nodes and execute findVertex on each
find_five_base = random.randint(0, 44)
for i in range(find_five_base,find_five_base+5):
	my_g.findVertex(i)
	


