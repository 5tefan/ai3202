import argparse

class BaeNode():
	def __init__(self, parents = None, children = None):
		if parents:
			self.parents = parents
		else:
			self.parents = []

		if children:
			self.children = children
		else:
			self.children = []

	def get_parents(self):
		return self.parents

	def get_children(self):
		return self.children

	def set_parents(self, parents):
		self.parents = parents

	def add_parent(self, parent):
		self.parents.append(parent)

	def set_children(self, children):
		self.children = children

	def add_child(self, child):
		self.children.append(child)

class BaeNet():
	def __init__(self):
		self.priori = []

	def add_priori(self, pri):
		

def check_01(p):
	return ((p >= 0) and (p <= 1))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-g", help="conditional probability")
	parser.add_argument("-j", help="joint probability")
	parser.add_argument("-m", help="marginal probability")
	parser.add_argument("-p", help="set a prior for pollution or smoking", nargs=2)
	args = parser.parse_args()
	
	_P = .1 #P(pollution) = .1
	_S = .3 #P(smoker) = .3
	if args.p:
		try:
			if (args.p[0] in ('P', 'S') and check_01(float(args.p[1]))):
				if args.p[0] == 'P':
					_P = float(args.p[1])
				else:
					_S = float(args.p[1])
			else:
				raise ValueError
		except ValueError:
			parser.error("-p must be followed by P or S then a probability")

	if args.g:
		print args.g
