#!/usr/bin/env python
import argparse
import heapq
import math

def readMaze(fileName):
    f = open(fileName,'r')
    maze = []
    line = f.readline()
    while line != "":
        maze.append(line.split())
        line = f.readline()
    for i in range(0,len(maze)):
        for j in range(0,len(maze[i])):
            maze[i][j] = Node(i, j, int(maze[i][j]))
    return maze

# get the distance from square a to square b
def getDistance(ax, ay, bx, by, typ):
    return 10 + int(ax != bx and ay != by) * 4 + typ * 10

class Node:
    def __init__(self, x, y, typ):
        self.x = x
        self.y = y
        self.typ = typ
        self.parent = None
        self.costToStart = 0
        self.f = 0
    
    def updateParent(self, newParent, heuristic):
        self.parent = newParent
        self.costToStart = newParent.costToStart + getDistance(self.x, self.y, newParent.x, newParent.y, self.typ)
        self.f = self.costToStart + heuristic(self.x, self.y)
    

class Search:
    def __init__(self, maze, h):
        self.maze = maze
        self.endX = 0
        self.endY = len(maze[0]) - 1
        self.openList = []
        self.closedList = []
        # sort by smallest f value
        heapq.heapify(self.openList)
        if (h == 0):
            self.heuristic = self.manhattan
        else:
            self.heuristic = self.euclid
        self.start = maze[len(maze) - 1][0]
    
    def manhattan(self, x, y):
        return abs(x - self.endX) + abs(y - self.endY)
    
    def euclid(self, x, y):
        return math.sqrt((x - self.endX)**2 + (y - self.endY)**2)
    
    # return a list of the valid adjacent squares
    def getAdjacent(self, node):
        nodes = []
        for i in range(node.x - 1, node.x + 2):
            for j in range(node.y - 1, node.y + 2):
                if (i >= 0 and i < len(self.maze) and j >=0 and
                    j < len(self.maze[i]) and not(i == node.x and j == node.y)):
                    if (maze[i][j].typ != 2):
                        adj = maze[i][j]
                        nodes.append(adj)
        return nodes
    
    # print the final path, starting at the end and traversing backwards
    def printPath(self, node):
        cost = 0
        while not(node.x == self.start.x and node.y == self.start.y):
            print "Path node at",node.x,",",node.y
            cost += getDistance(node.x, node.y, node.parent.x, node.parent.y, node.typ)
            node = node.parent
        print "Path node at",node.x,",",node.y
        print "Cost is", cost

    def search(self):
        heapq.heappush(self.openList, (self.start.f, self.start))
        locs = 0
        while (len(self.openList) > 0):
            f, node = heapq.heappop(self.openList)
            locs += 1
            self.closedList.append(node)
            if (node.x == self.endX and node.y == self.endY):
                print "%i locations evaluated" % locs
                self.printPath(node)
                break;
            adjNodes = self.getAdjacent(node)
            for n in adjNodes:
                if not(n in self.closedList):
                    if ((n.f, n) in self.openList):
                        if (n.costToStart > node.costToStart + getDistance(n.x, n.y, node.x, node.y, n.typ)):
                            n.updateParent(node, self.heuristic)
                    else:
                        n.updateParent(node, self.heuristic)
                        heapq.heappush(self.openList, (n.f, n))

    
if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--maze", help="Maze one or maze 2",
                           type=str, default="World1.txt", required=False)
    argparser.add_argument("--heur", help="Heuristic to use",
                           type=int, default=0, required=False)
    args = argparser.parse_args()
    
    maze = readMaze(args.maze)
    search = Search(maze, args.heur)
    search.search()
