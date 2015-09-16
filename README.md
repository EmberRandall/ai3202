# ai3202
New repo for AI homework

In assignment 2, I used the Euclidean distance as my second heuristic, with the equation
h = sqrt((x-endX)**2 + (y-endY)**2)
where endX and endY represent the coordinates of the goal square and x and y represent the coordinates of the current node.

Since the horse can move diagonally, I thought that this heuristic would provide good results, as it measures the diagonal distance.
In the end, using Euclidean distance provided identical results to using Manhattan distance.  It explored the same number of squares and discovered the same path.

The command line arguments for my program are --maze and --heur.  --maze takes in the filename of the world as a string: World1.txt or World2.txt.
The default maze is World1.txt, so if --maze is not provided, the program uses World1.
--heur takes an integer argument to determine the heuristic, where the default value of 0 represents the Manhattan distance, and any other integer represents the Euclidean distance