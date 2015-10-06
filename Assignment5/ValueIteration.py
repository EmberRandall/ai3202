#!/usr/bin/env python
import argparse
import heapq
import math
from numpy import arange

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

class Node:
    def __init__(self, x, y, typ):
        self.x = x
        self.y = y
        self.typ = typ
        self.parent = None
        self.utility = 0 if typ != 2 else float("-inf")
        self.reward = 0
        if (typ == 1):
            self.reward = -1
        elif (typ == 2):
            self.reward = float("-inf")
        elif (typ == 3):
            self.reward = -2
        elif (typ == 4):
            self.reward = 1
        elif (typ == 50):
            self.reward = 50
    

class Search:
    def __init__(self, maze, gamma, epsilon):
        self.maze = maze
        self.gamma = gamma
        self.eps = epsilon
        self.endX = 0
        self.endY = len(maze[0]) - 1
        self.openList = []
        self.closedList = []
        # sort by smallest f value
        heapq.heapify(self.openList)
        self.start = maze[len(maze) - 1][0]
    
    def iterate(self):
        err = float("inf")
        while (err > self.eps * (1 - self.gamma) / self.gamma):
            max_err = 0.0
            for i in range(0, len(self.maze)):
                for j in range(len(self.maze[i])-1, -1, -1):
                    if (maze[i][j].typ != 2):
                        oldUtil = maze[i][j].utility
                        maze[i][j].utility = maze[i][j].reward + self.gamma * self.getMaxMove(i, j)
                        if (abs(oldUtil - maze[i][j].utility) > max_err):
                            max_err = abs(oldUtil - maze[i][j].utility)
            err = max_err
    
    def getUtility(self, x, y):
        if (x >= 0 and x < len(self.maze) and y >= 0 and y < len(self.maze[x])):
            if (self.maze[x][y].utility > float("-inf")):
                return self.maze[x][y].utility
        return 0.0
    
    def getMaxMove(self, x, y):
        moves = []
        moves.append(0.8 * self.getUtility(x - 1, y) + 0.1 * self.getUtility(x, y + 1) + 0.1 * self.getUtility(x, y - 1))
        moves.append(0.8 * self.getUtility(x + 1, y) + 0.1 * self.getUtility(x, y + 1) + 0.1 * self.getUtility(x, y - 1))
        moves.append(0.8 * self.getUtility(x, y + 1) + 0.1 * self.getUtility(x + 1, y) + 0.1 * self.getUtility(x - 1, y))
        moves.append(0.8 * self.getUtility(x, y - 1) + 0.1 * self.getUtility(x + 1, y) + 0.1 * self.getUtility(x - 1, y))
        #print "x=",x,"y=",y,"moves are ",moves
        return max(moves)
    
    # return a list of the valid adjacent squares
    def getAdjacent(self, node):
        nodes = []
        if (node.x > 0):
            nodes.append(self.maze[node.x - 1][node.y])
        if (node.y > 0):
            nodes.append(self.maze[node.x][node.y - 1])
        if (node.x + 1 < len(self.maze)):
            nodes.append(self.maze[node.x + 1][node.y])
        if (node.y + 1 < len(self.maze[node.x])):
            nodes.append(self.maze[node.x][node.y + 1])
        return nodes
    
    # print the final path, starting at the end and traversing backwards
    def printPath(self, node):
        current = [(0,9),(1,9),(2,9),(2,8),(2,7),(3,7),(4,7),(4,6),(5,6),(6,6),(7,6),(7,5),(7,4),(7,3),(7,2),(7,1),(7,0)]
        #current = [(0,9),(1,9),(2,9),(2,8),(2,7),(3,7),(3,6),(4,6),(5,6),(6,6),(7,6),(7,5),(7,4),(7,3),(7,2),(7,1),(7,0)]
        i = 0
        while not(node.x == self.start.x and node.y == self.start.y):
            print "Path node at", node.x, ",", node.y
            print "Utility of node is", node.utility
            if (current[i] != (node.x, node.y)):
                print "new path found, eps is",self.eps
            node = node.parent
            i += 1
        print "Path node at", node.x, ",", node.y
        print "Utility of node is", node.utility
    
    def printMaze(self):
        for i in range(0, len(maze)):
            s = ""
            for j in range(0, len(maze[i])):
                s += "%.2f " % maze[i][j].utility
            print s
    
    def search(self):
        self.iterate()
        heapq.heappush(self.openList, (-self.start.utility, self.start))
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
                    if not ((-n.utility, n) in self.openList):
                        heapq.heappush(self.openList, (-n.utility, n))
                        n.parent = node

    
if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--maze", help="Maze name",
                           type=str, default="World1MDP.txt", required=False)
    argparser.add_argument("--eps", help="Size of epsilon to use",
                           type=float, default=0.5, required=False)
    args = argparser.parse_args()
    
    maze = readMaze(args.maze)
    search = Search(maze, 0.9, args.eps)
    search.search()
    #search.printMaze()
