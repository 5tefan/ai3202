#A* Search

usage: python astar.py [world file] [heuristic]

The heuristic argument may be 0 or 1

For a value of 0, astar.py uses the Manhatten distance heurstic. 
- Manhatten distance = (x dist to goal) + (y dist to goal)

For a value of 1, astar.py uses the Pythagorean distance heuristic.
- Pythagorean distance = sqrt( (x dist to goal)^2 + (y dist to goal)^2 )

For World1.txt and World2.txt, heuristics 0 and 1 both perform equivalently. 

