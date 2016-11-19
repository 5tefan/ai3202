

class CSCI3202_Binary_Tree_Node():
	def __init__(self, key, parent=None, left=None, right=None):
		self.key = key
		self.parent = parent
		self.left = left
		self.right = right

	def addParent(self, parent):
		self.parent = parent

	def addChild(self, value):
		if self.left == None:
			self.left = CSCI3202_Binary_Tree_Node(value, self)
			return True
		elif self.right == None:
			self.right = CSCI3202_Binary_Tree_Node(value, self)
			return True
		else:
			print "Parent has two children, node not added"
			return False

	def removeChild(self, child):
		if self.left == child:
			self.left = None
			return True
		elif self.right == child:
			self.right = None
			return True
		return False

	def getLeft(self):
		return self.left

	def getRight(self):
		return self.right

	def getChildren(self):
		return [self.left, self.right]

	def getValue(self):
		return self.key

	def getParent(self):
		return self.parent

class CSCI3202_Binary_Tree():
	def __init__(self, key=None):
		""" Create a new binary tree with the root node optionally specified. """
		if key:
			self.root = CSCI3202_Binary_Tree_Node(key)
		else:
			self.root = None

	def add(self, value, parentValue = None):
		""" Add a node with specified value to the binary tree, under the parent
			with value parentValue. parentValue None to create root Node. """
		if self.root == None:
			# add a root node if there is none yet
			self.root = CSCI3202_Binary_Tree_Node(value)
		if self.root.getValue() == parentValue:
			# if root node has parentValue, try adding value as a node
			return self.root.addChild(value)
		else:
			# otherwise start recursive examining of children below 
			# root with addBelow root.
			for child in self.root.getChildren():
				tmp_add = self.addBelow(value, parentValue, child)
				if tmp_add:
					return tmp_add
		print "Parent not found"
		return False

	def addBelow(self, value, parentValue, root):
		""" The recursive version of add. Same as add, except for the extra
			parameter root which specifies which node to search under """
		if root == None:
			# return False, we must be at the end of the tree or something
			return False
		if root.getValue() == parentValue:
			# if we found the parentvalue, add child to that node
			return root.addChild(value)
		else:
			# otherwise, recusion to search the children
			for child in root.getChildren():
				tmp_add = self.addBelow(value, parentValue, child)
				if tmp_add:
					# only return if we actually add the node, 
					# otehrwise just let the function fall through
					return tmp_add

	def delete(self, value):
		""" Delete a node with value value. Delete starts from the root
			and then calls deleteBelow to recursively check down the tree. """
		if self.root == None:
			# return False, we must be at the end of the tree or something
			return False
		if self.root.getValue() == value:
			# we found the node! Make sure it doesn't have children and then let the
			# garbage collector take care of it.
			if self.root.getChildren()[0] == None and self.root.getChildren()[1] == None:
				self.root = None
				return True
			print "Node not deleted, has children"
			return False
		else:
			# otherwise begin traversing down recursively
			for child in self.root.getChildren():
				tmp_del = self.deleteBelow(value, child)
				if tmp_del:
					return tmp_del
		# again, fall through if nothing ends up being deleted
		print "Node not found"
		return False

	def deleteBelow(self, value, root):
		if root == None:
			# must have reached the end of a branch
			return False
		if root.getValue() == value:
			# we found the node! Make sure it doesn't have children and then let the
			# garbage collector take care of it.
			if root.getChildren()[0] == None and root.getChildren()[1] == None:
				return root.getParent().removeChild(root)
			else:
				print "Node not deleted, has children"
				return False
		else:
			# keep going down the branches recursively
			for child in root.getChildren():
				tmp_del = self.deleteBelow(value, child)
				if tmp_del:
					return tmp_del
		
	def printTree(self):
		""" Print the binary tree in pre-order traversal. printTree starts things off
			and then printBelow takes over with the recursion. """
		if self.root == None:
			return
		print self.root.getValue()
		for child in self.root.getChildren():
			self.printBelow(child)
		
	def printBelow(self, root=None):
		if root == None:
			return
		print root.getValue()
		for child in root.getChildren():
			self.printBelow(child)
			
	
		
