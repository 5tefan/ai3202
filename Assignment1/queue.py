import Queue

class CSCI3202_Queue(Queue.Queue):
	def __init__(self):
		Queue.Queue.__init__(self)

	def put(self, item):
		if isinstance(item, (int, long)):
			Queue.Queue.put(self, item)
			return True
		return False

