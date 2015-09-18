#A* Search

usage: python astar.py [world file] [heuristic]

-----------
##World File
The world file may be any matrix of numbers representing a world where intry i, j is 
##### 0. An empty square
* (cost = 10 horizontal or vertical, 14 diagonal)
  
##### 1. A mountain 
* (cost += 10)
  
##### 2. A wall 
* (not allowed to move)

##Heuristic
The heuristic argument may be an integer between 0 and 4 to instruct the program to use one of the following heuristics:  
#### 0. Manhatten Distance
* Manhatten distance = abs(x dist to goal) + abs(y dist to goal)  
* Chosen for ease of implementation
* World1.txt: Evaluated locations: 60, Path cost: 130
* World2.txt: Evaluated locations: 38, Path cost: 144
  
#### 1. Pythagorean Distance
* Pythagorean distance = sqrt( (x dist to goal)^2 + (y dist to goal)^2 )  
* Chosen because it gives a more *exact* direct line distance.
* World1.txt: Evaluated locations: 60, Path cost: 130
* World2.txt: Evaluated locations: 58, Path cost: 144
  
#### 2. Horizontal Distance
* Horizontal Distance = abs(x dist to goal)
* Chosen to see if an even simpler heuristic is effective
* World1.txt: Evaluated locations: 59, Path cost: 130
* World2.txt: Evaluated locations: 57, Path cost: 144
  
#### 3. Vertical Distance
* Vertical Distance = abs(y dist to goal)
* Chosen to compare/contrast with Horizontal Distance
* World1.txt: Evaluated locations: 60, Path cost: 130
* World2.txt: Evaluated locations: 58, Path cost: 144
  
#### 4. No Distance
* No Distance = 0
* Implemented to see if search would still work. 
* World1.txt: Evaluated locations: 60, Path cost: 130
* World2.txt: Evaluated locations: 58, Path cost: 144
  
------------

It looks as if Horizontal Distance is the negligibly optimal heuristic here. I think this might because the map is wider horizontal than so the horizontal heuristic motivates the algorithm to move in the correct direction.

