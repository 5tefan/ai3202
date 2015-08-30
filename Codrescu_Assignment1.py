


###########################################
# QUEUE
from queue import CSCI3202_Queue as q

# initialize
my_q = q()

# put integers 0 .. 19 onto the stack
for i in range(20):
	my_q.put(i)

# get integers off the stack
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





