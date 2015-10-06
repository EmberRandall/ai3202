# ai3202
New repo for AI homework

In assignment 2, I used the Euclidean distance as my second heuristic, with the equation:

h = sqrt((x-endX)^2 + (y-endY)^2)

where endX and endY represent the coordinates of the goal square and x and y represent the coordinates of the current node.

Since the horse can move diagonally, I thought that this heuristic would provide good results, as it measures the diagonal distance.
In the end, using Euclidean distance provided identical results to using Manhattan distance.  It explored the same number of squares and discovered the same path.

The command line arguments for my program are --maze and --heur.  --maze takes in the filename of the world as a string: World1.txt or World2.txt.
The default maze is World1.txt, so if --maze is not provided, the program uses World1.
--heur takes an integer argument to determine the heuristic, where the default value of 0 represents the Manhattan distance, and any other integer represents the Euclidean distance

In assignment 5, increasing epsilon to 90 changed the path slightly: the original path went from (4,6) to (4,7) to (3,7),
while the changed path went from (4,6) to (3,6) to (3,7).  Increasing epsilon again to 460 caused a radically different path,
which went up first and then through the mountains at the top.  I found these values by running my evaluation code for epsilons from
0.5 to 500, with varying step sizes.  When the program found an epsilon value that changed the path, I ran the code again with a smaller
step size to narrow in on the correct value.  Of course, these epsilon values are far larger in practice than they would be in a real usage
of this algorithm.