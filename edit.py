into.opy
Commented:
# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
import heapq

def search(maze, searchMethod):
    print(maze.getStart())
    print(maze.getDimensions())
    print(maze.getObjectives())
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)

#helper function to backtrack a path from the goal state
def getPath(start, state, visited):
    if state.point == start:
      return [start]
    else:
      return getPath(start,visited[str(state.point)+str(state.obj)][0],visited) + [state.point]

def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    queue = [state(maze.getStart(),maze.getObjectives(),0)]  #holds frontier
    objs = maze.getObjectives()
    visited = {} #entry is str(point)+str(obj): (previous state, best cost to that state)
    savevis = [] #comprehensive list of visited maze locations
    start = maze.getStart()
    done = False
    total = 0
    while not done:
        total+=1
        curr = queue.pop()

        if curr.point not in savevis:
          savevis.append(curr.point)

        #process each neighbor and check if we've reached the goal
        for neighbor in maze.getNeighbors(curr.point[0],curr.point[1]):
            n = state(neighbor,curr.obj.copy(),curr.cost+1)
            if neighbor in n.obj:
                n.obj.remove(neighbor)
            skey = str(n.point)+str(n.obj)
            if skey in visited.keys():
                if visited[skey][1] > n.cost:
                    visited[skey] = (curr,n.cost)
                if visited[skey][1] <= n.cost:
                    continue
            else:
                visited[skey] = (curr,n.cost)
            if len(n.obj) == 0:
                sol = getPath(maze.getStart(),n,visited)
                done = True
            queue.insert(0,n)
    print(total)
    return sol, len(savevis)


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0

class gstate:
    def __init__(self,point,obj,cost):
        self.point = point
        self.obj= obj
        self.cost = cost
    def __lt__(self, other):
        try:
            return manhattan(self.point,self.obj[0]) < manhattan(other.point, other.obj[0])
        except:
            return self



def greedy(maze):
    # TODO: Write your code here
    heap = [gstate(maze.getStart(),maze.getObjectives(),h(maze.getStart(),maze.getObjectives(),0))]
    heapq.heapify(heap)
    objs = maze.getObjectives()
    visited = {} #entry is str(point)+str(obj): (previous state, best cost to that state)
    savevis = []
    start = maze.getStart()
    done = False
    sol = []
    while not done:
        curr = heapq.heappop(heap)
        if curr.point not in savevis:
            savevis.append(curr.point)
        for neighbor in maze.getNeighbors(curr.point[0],curr.point[1]):
            n = gstate(neighbor,curr.obj.copy(),curr.cost+1)
            if neighbor in n.obj:
                n.obj.remove(neighbor)
            skey = str(n.point)+str(n.obj)
            if skey in visited.keys():
                if visited[skey][1] > n.cost:
                    visited[skey] = (curr,n.cost)
                if visited[skey][1] <= n.cost:
                    continue
            else:
                visited[skey] = (curr,n.cost)
            if len(n.obj) == 0:
                sol = getPath(maze.getStart(),n,visited)
                done = True
            heapq.heappush(heap,n)
    return sol, len(savevis)

def manhattan(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])



def h(point, obj, cost):
    if len(obj) == 0:
        return cost
    z = max([manhattan(point, i) for i in obj])


    y= []
    z = 0
    for i in range(len(obj)-1):
        d = [manhattan(point, i) for i in obj]
        if 0 in d:
            d.remove(0)
        z+=(min(d))
        z = sum(y)
    return z + cost

class state:
    def __init__(self,point,obj,cost):
        self.point = point
        self.obj= obj
        self.cost = cost
    def __lt__(self, other):
        return self.cost + h(self.point,self.obj,self.cost) < other.cost + h(other.point,other.obj,other.cost)



def astar(maze):
    # TODO: Write your code here
    dlen = {}
    def permute(objs): #permute and djikstra are MST
        if len(objs) == 1:
            return [[objs[0]], []]
        else:
            temp = []

            new = objs.copy()
            new.remove(objs[0])
            x = permute(new)
            temp = temp + x
            temp = temp + [[objs[0]] + i for i in x]
            return temp

    def h(point, obj, cost):

        d = [manhattan(point,i) for i in obj]
        obj.sort()
        if len(d) == 0:
            return dlen[str(obj)]
        return dlen[str(obj)] + min(d)

    class state:
        def __init__(self,point,obj,cost): #point, remaining objectives, and cost so far
            self.point = point
            self.obj= obj
            self.cost = cost
        def __lt__(self, other): #to work with heaps
            return self.cost + h(self.point,self.obj,self.cost) < other.cost + h(other.point,other.obj,other.cost)

    def djikstra(p):
        added = []
        edges =[]
        for i in range(len(p)):
            for j in range(len(p)):
                if i ==j:
                    continue
                edges.append((manhattan(p[i],p[j]), i, j))
        heapq.heapify(edges)
        connected = {}
        for i in range(len(p)):
            connected[i] = [i]
        done = False
        cost = 0
        if len(p)<= 1:
            return 0
        while True:
            if len(connected[0]) == len(p):
                break

            e = heapq.heappop(edges)
            if e[2] in connected[e[1]]:
                continue
            else:
                temp = connected[e[1]]
                connected[e[1]].append(connected[e[2]])
                connected[e[2]].append(temp)
                cost+=e[0]
        return cost


    perms = permute(maze.getObjectives())
    for p in perms:
        temp = p.copy()
        temp.sort()
        dlen[str(temp)] = djikstra(p.copy())

    #starts with start state, the objectives are original, h
    heap = [state(maze.getStart(),maze.getObjectives(),h(maze.getStart(),maze.getObjectives(),0))]
    heapq.heapify(heap)
    objs = maze.getObjectives()
    print("objs ", len(objs))
    visited = {} #entry is str(point)+str(obj): (previous state, best cost to that state)
    savevis = [] #comprehensive list of visited maze locations by all paths
    start = maze.getStart()
    done = False
    sol = []
    total = 0
    hit = []
    while not done:
        if len(heap) == 0:
            print('search failed')
            done = True #bookkeeping
        curr = heapq.heappop(heap)
        skey = str(curr.point) + str(curr.point) 
        if skey in visited.keys():
            if visited[skey][1] <= curr.cost:
                continue
        total+=1 #bookkeeping
        if curr.point not in savevis:
            savevis.append(curr.point)
        for neighbor in maze.getNeighbors(curr.point[0],curr.point[1]):
            n = state(neighbor,curr.obj.copy(),curr.cost+1)
            if neighbor in n.obj: #if that neighbor is a pellet,
                hit.append(neighbor)
                n.obj.remove(neighbor) #remove the pellet from the objectives of that state
            skey = str(n.point)+str(n.obj) #key for dictionary
            if skey in visited.keys():     #backtrack to find path at the end, this is the way of keeping track of the previous state with the lowest cost
                if visited[skey][1] > n.cost: #if its the worst state, skip
                    visited[skey] = (curr,n.cost)
                if visited[skey][1] <= n.cost:
                    continue
            else:
                visited[skey] = (curr,n.cost) #if state has reached all of teh objectives, backtrack
            if len(n.obj) == 0:
                sol = getPath(maze.getStart(),n,visited) #backtrack
                done = True
            heapq.heappush(heap,n)
    print(hit)
    return sol, len(savevis)

