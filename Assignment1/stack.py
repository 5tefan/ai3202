class CSCI3202_Stack():
	def __init__(self):
		self._store = []

	def push(self, item):
		self._store.append(item)

	def pop(self):
		return self._store.pop()

	def checkSize(self):
		return len(self._store)
