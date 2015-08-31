class CSCI3202_Graph():
	def __init__(self):
		self.graph = {}

	def addVertex(self, value):
		""" Add a vertex to the graph represented by our dictionary. """
		try:
			self.graph[value]
			print "Vertex already exists"
			return False
		except KeyError:
			self.graph[value] = []
			return True

	def addEdge(self, value1, value2):
		""" Add an edge between verticies with value1 and value2. """
		if value1 == value2:
			return False
		try:
			vertex1 = self.graph[value1]
			vertex2 = self.graph[value2]
			if value2 not in vertex1:
				vertex1.append(value2)
				vertex2.append(value1)
			return True
		except KeyError:
			print "One or more verticies not found"
			return False

	def findVertex(self, value):
		""" Print the values of the adjacent verticies to vertex with value value. """
		try:
			print "Vertex %s is adjacent to %s" % (value, self.graph[value])
		except KeyError:
			"Vertex not found"

