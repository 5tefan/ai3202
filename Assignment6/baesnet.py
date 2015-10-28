import argparse
import operator
import re

def check_01(p):
	return ((p >= 0) and (p <= 1))

def prod(iterable):
	return reduce(operator.mul, iterable, 1)

class BaeNode():
	def __init__(self, name):
		self.name = name
		self.parent_names = []
		self.parent_nodes = []
		self.cpt = {} #conditional probability table, enforce key sort() invariant

	def __repr__(self):
		return "%s: {%s}"%(self.name, self.cpt)

	def add_conditional(self, cond, prob):
		self.cpt[cond] = prob

	def add_parent(self, parent):
		self.parent_names.append(parent.name.upper())
		self.parent_nodes.append(parent)

class BaeNet():
	def __init__(self, file_name, show_dist=False):
		self.node_names = []
		self.nodes = []
		self.show_dist = show_dist
		file_lines = [ l for l in open(file_name).read().split('\n') if l and l[0] != "#" ]
		for each in file_lines:
			self.set_cpt(each, True)

	def joint(self, node_names):
		node_names = self.sort_nodes(node_names)[::-1]
		prod_arr = []
		distprint = []
		for i in range(len(node_names)):
			consider = node_names[i:]
			xi = consider[0] #x_i
			node = self.nodes[ self.node_names.index(xi.upper()) ] #node of x_i
			parents = []
			for rem in consider[1:]:
				if rem.upper() in node.parent_names:
					parents.append(rem)
			parents.sort()
			key = ",".join(parents)
			try:
				cpt_val = node.cpt[key]
				if key:
					distprint.append( "P(%s|%s)"%(xi,key) )
				else:
					distprint.append( "P(%s)"%(xi) )
				if xi.islower():
					prod_arr.append(1-node.cpt[key])
				else:
					prod_arr.append(node.cpt[key])
			except:
				pass
		if self.show_dist:
			print "= " + " * ".join( distprint )
		 	print "= " + " * ".join( [ str(f) for f in prod_arr ] )
		return prod(prod_arr)

	def marginal(self, node_names):
		node_names = self.sort_nodes(node_names)
		node_position = self.node_names.index( node_names[0].upper() )
		sum_over = []
		distprint = []
		sum_over_nodes = [x for x in self.get_all_parents(node_names[-1].upper()) if x not in node_names.upper()]
		if sum_over_nodes:
			lsum = len(sum_over_nodes) ** 2 if len(sum_over_nodes) > 1 else 2
			for i in range( lsum ): #generate all permuataions of the parents
				binrep = bin(i)[2:].zfill(len(sum_over_nodes))
				perm = []
				for j in range(len(sum_over_nodes)):
					perm.append( (sum_over_nodes[j].lower() if binrep[j] == "1" else sum_over_nodes[j]) )
				perm.insert( node_position, node_names )
				perm = "".join(perm)
				if self.show_dist:
					distprint.append(perm)
					print "P(%s)"%(perm)
				sum_over.append( self.joint(perm) )
		else: #case where asking for marginal of a priori
			distprint.append(node_names)
			sum_over.append( self.joint(node_names) )
		if self.show_dist:
			print "P(%s)"%node_names
			print "= " + " + ".join( [ "P(%s)"%perm for perm in distprint ] )
			print "= " + " + ".join( [ str(f) for f in sum_over ] )
		return sum(sum_over)

	def conditional(self, of, given):
		return self.marginal(given + of)/self.marginal(given)

	def sort_nodes(self, node_names):
		nodes = list(node_names)
		try:
			nodes.sort( key=lambda x: self.node_names.index(x.upper()) )
		except:
			print "ERROR: bad request"
			print "One of requested variables not found"
			exit(-1)
		return "".join(nodes)

	def get_all_parents(self, node_name):
		node = self.nodes[ self.node_names.index(node_name.upper()) ]
		ret = []
		stack = []
		stack.extend(node.parent_nodes)
		while stack:
			node = stack.pop(0)
			ret.append(node.name)
			stack.extend(node.parent_nodes)
		return ret[::-1]
		
	def check_line(self, line):
		""" make sure the text entry is well formed to specify a node in the network """
		check = re.match("[a-zA-Z](/[a-zA-Z,]*[a-zA-Z])*:0*(.\d+)?", line)
		return True if check else False
		
	def set_cpt(self, line_input, errexit=False):
		if self.check_line(line_input):
			#node name and create node
			node_name = line_input.split(":")[0].split("/")[0]
			if node_name.upper() not in self.node_names:
				self.node_names.append(node_name.upper())
				node = BaeNode(node_name.upper())
				self.nodes.append(node)
			else:
				node = self.nodes[ self.node_names.index(node_name.upper()) ]
	
			#if it is conditional, add parents
			try: #to parse conditionals
				conds = line_input.split(":")[0].split("/")[1].split(",")
				for cond in conds:
					try: #to see if the node has the parent already
						node.parent_names.index(cond.upper())
					except: #if not, create it
						try: #to find the parent node
							parent = self.nodes[ self.node_names.index(cond.upper()) ]
							node.add_parent( parent )
						except:
							print "ERROR: Bad input"
							if errexit:
								print "ensure parent defined before child nodes"
								exit(-1)
							print "couldn't find conditional parent nodes"
				conds.sort()
				key = ",".join(conds)
				value = float(line_input.split(":")[1])
				node.add_conditional(key, value)
			except: #else there are no conditionals, is a priori
				value = float(line_input.split(":")[1])
				node.add_conditional("", value)
		

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("input_file", help="text file specification of the network")
	parser.add_argument("-d", help="show distributions", action="store_true")
	parser.add_argument("-c", help="conditional probability")
	parser.add_argument("-j", help="joint probability")
	parser.add_argument("-m", help="marginal probability")
	parser.add_argument("-p", help="set a priori or a cpt table entry", nargs=2)
	args = parser.parse_args()

	if args.d:
		net = BaeNet(args.input_file, True)
	else:
		net = BaeNet(args.input_file)
	
	if args.p:
		net.set_cpt(":".join(args.p))

	if args.c:
		c = args.c.split("/")
		print "P(%s)\n= %s" % (args.c, net.conditional(c[0], c[1]))

	if args.j:
		print "P(%s)" % args.j
		print "= %f" % net.joint(args.j)

	if args.m:
		print "= %f" % net.marginal(args.m)
