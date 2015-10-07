#Markov Decision Process

usage: python mdp.py [world file] [epsilon]

-----------
##World File
The world file may be any matrix of numbers representing a world where intry i, j is 
##### 0. An empty square
* (reward = 0)
  
##### 1. A mountain 
* (reward = -1)
  
##### 2. A wall 
* (not allowed to move)

##### 3. A snake
* (reward = -2)

##### 4. A barn
* (reward = +1)

#Effect of epsilon
The choice of the parameter epsilon does affect the solution path found.

Using World1MDP.txt:

For example, with epsilon up to 2.0, the path found is [(7, 0), (6, 0), (5, 0), (4, 0), (4, 1), (3, 1), (2, 1), (2, 2), (2, 3), (1, 3), (1, 4), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)]

For epsilon between 2.1 and 5, the path found is [(7, 0), (7, 1), (7, 2), (7, 3), (6, 3), (5, 3), (4, 3), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)]
