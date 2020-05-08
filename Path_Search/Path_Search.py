import re, sys
import queue
from queue import LifoQueue, PriorityQueue
sys.setrecursionlimit(10**6)

class _map():
    def __init__(self, source, destinationandcost, latlog):
        self.source = source
        self.destinationandcost = destinationandcost
        self.latlog = latlog
        
def inpmap():
    f = open("usroads.pl", "r")
    maps = f.read()
    maps = maps[maps.find("===\nroad")+4:]
    maps = maps[:maps.find("%")]
    f.close()
    g = open("maps.txt", "w")
    g.write(maps)
    g.close()
    f = open("usroads.pl", "r")
    maps = f.read()
    f.close()
    maps = maps[maps.find("===\ncity")+4:]
    h = open("latlog.txt", "w")
    h.write(maps)
    h.close()
    
def mapofworld():
    f = open('map.txt', 'r')
    maps = f.read()    
    f.close()
    sources = re.findall("\(\w+,", maps)
    destinations = re.findall(",\s\w+,", maps)
    pathcosts = re.findall('\s\d+', maps)
    g = open('latlog.txt', 'r')
    lalogf = g.read()
    g.close()
    cities = re.findall(r'\((\w+)', lalogf)
    latlog = re.findall(r'(\d+.\d+)|(-\d+.\d+)', lalogf)
    latlogseries = []
    for i in range(len(latlog)):
        if len(latlog[i][0]) != 0:
            latlogseries.append(latlog[i][0])
            continue
        latlogseries.append(latlog[i][1])
    
    lat_log = []
    i = 0
    while i < len(latlogseries):
        lat_log.append((float(latlogseries[i]),float(latlogseries[i+1]))) 
        i = i + 2
        
    __map = []
    for i in range(len(sources)): sources[i] = sources[i][1:-1]
    for j in range(len(destinations)): destinations[j] = destinations[j][2:-1]
    for k in range(len(pathcosts)): pathcosts[k] = int(pathcosts[k])
    for i in range(len(sources)): sources.append(destinations[i]), destinations.append(sources[i]), pathcosts.append(pathcosts[i])
    
    dictofmaps = {}
    for i in sources:  
        dictofmaps[i] = []

    current_source = sources[0]
    j = 0
    for i in sources:
        if i == current_source:
            dictofmaps[i].append((destinations[j], pathcosts[j]))
            j += 1
            continue
        current_source = i
        dictofmaps[i].append((destinations[j], pathcosts[j]))
        j += 1
    for l in range(len(cities)): 
        __map.append(_map(cities[l], dictofmaps[cities[l]], lat_log[l]))
    return __map
    
def get_problem():
    source = input('source: ')
    destination = input('destination: ')
    return source, destination

class current_location:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
    
    def __eq__(self, other):
        return True


def isgoal(source, destination): return source == destination


def depth_first_search(problem, alreadyvisited, path_cost, finalpath):
    global numnodes
    numnodes += 1
    if isgoal(problem.source, problem.destination): 
        finalpath.append(problem.source)
        return (finalpath, path_cost)
    frontier = LifoQueue()
      

    alreadyvisited.add(hash(problem.source))
    finalpath.append(problem.source)
    
    for i in MAP: 
        if i.source == problem.source:
            actions = i.destinationandcost
            break
        
    for act in actions:
        frontier.put(act)
        
    global maxqlen
    if frontier.qsize() > maxqlen:
        maxqlen = frontier.qsize()
            
    while not frontier.empty():
        act = frontier.get()
        child = current_location(act[0], problem.destination)
        if isgoal(child.source, child.destination): 
            finalpath.append(child.destination)
            path_cost += act[1]
            return (finalpath, path_cost)
        
        if hash(child.source) not in alreadyvisited:
            path_cost += act[1]
            alreadyvisited.add(hash(child.source))
            solution = depth_first_search(child, alreadyvisited, path_cost, finalpath)
            if solution[0] != "Failure":
                return solution
    
    return ("Failure", None)

def Astar(problem):
    path_cost = 0
    frontier = PriorityQueue()
    frontier.put((0, 0, problem))
    alreadyvisited = set()
    finalpath = []
    global maxqlen, numnodes
    while frontier.qsize() != 0:
        if frontier.qsize() > maxqlen:
            maxqlen = frontier.qsize()
            
        act = frontier.get()
        numnodes += 1
        currentloc = current_location(act[2].source, problem.destination)
        path_cost += act[1]
        finalpath.append(act[2].source)
        if isgoal(currentloc.source, currentloc.destination): 
            return (finalpath, path_cost)
        
        for i in MAP: 
            if i.source == currentloc.source:
                actions = i.destinationandcost
                break
        alreadyvisited.add(hash(currentloc.source))
        
        
        for act in actions:
            child = current_location(act[0], problem.destination)

                        
            if hash(child.source) not in alreadyvisited and child.source not in frontier.queue:
                frontier.put(((act[1] + sphericaldist(child)), act[1], child))

class childnode():
    def __init__(self, location, f, path_cost):
        self.location = location
        self.path_cost = path_cost
        self.f = f          

def rbfs(problem):
    path_cost = 0
    inf = float('inf')
    finalpath = []
    visited = set()
    return recursivebestfs(problem, childnode(problem.source, 0, 0), inf, finalpath, path_cost, visited)

def recursivebestfs(problem, node, flimit, finalpath, path_cost, visited):
    finalpath.append(node.location)
    visited.add(node.location)
    global numnodes
    numnodes += 1
    path_cost += node.path_cost
    if isgoal(node.location, problem.destination):
        return (finalpath, path_cost)
    successors = []
    for i in MAP:
        if i.source == node.location:
            for dnc in i.destinationandcost:
                if dnc[0] not in visited:
                    successors.append(childnode(dnc[0], 0, dnc[1]))
            break
    
    if len(successors) == 0:
        return ("Failure", float('inf'))
    
    for s in successors:
        s.f = max(s.path_cost + sphericaldist(current_location(s.location, problem.destination)), node.f)
    while len(successors) != 0:
        
        best = childnode(None, float('inf'), 0)
        for s in successors:
            if s.f < best.f:
                best = s
        
        successors.remove(best)
        if best.f > flimit:
            return ('Failure', best.f)
        
       
        alternative = childnode(None, float('inf'), 0)
        for s in successors:
            if s != best and s.f < alternative.f:
                alternative = s
        
        result = recursivebestfs(problem, best, min(flimit, alternative.f), finalpath, path_cost, visited)
        
        flimit = result[1]
        if result[0] != 'Failure':
            return result
    
    return ('Failure', flimit)
    
def sphericaldist(location):
    srclatlog = None
    dstlatlog = None
    for i in MAP:
        if i.source == location.source:
            srclatlog = i.latlog
        if i.source == location.destination:
            dstlatlog = i.latlog
    from math import sqrt, pi, cos
    global hflag
    if hflag == 0:
        return sqrt((69.5 * (srclatlog[0] - dstlatlog[0]))**2 + ((69.5 * cos(((srclatlog[0] + dstlatlog[0])/360 * pi)))*(srclatlog[1] - dstlatlog[1]))**2)
    else:
        return (abs(srclatlog[0] - dstlatlog[0]) + abs(srclatlog[1] - dstlatlog[1]))
    
def myheuristic(location):
    srclatlog = None
    dstlatlog = None
    for i in MAP:
        if i.source == location.source:
            srclatlog = i.latlog
        if i.source == location.destination:
            dstlatlog = i.latlog
    return (abs(srclatlog[0] - dstlatlog[0]) + abs(srclatlog[1] - dstlatlog[1]))


alreadyvisited = []

maxqlen = 0
numnodes = 0
hflag = None
        
def main():
    
    command = (sys.argv)
    algorithm = command[1]
    if int(command[2]) == 0 or int(command[2]) == 1:
        hflag = command[2]
    else:
        print("Error, heuristic should be either 0 or 1")
        exit()
        
    source = command[3]
    destination = command[4]
    cities = ['albanyGA', 'albanyNY', 'albuquerque', 'atlanta', 'augusta', 'austin', 'bakersfield', 'baltimore', 'batonRouge', 'beaumont', 'boise', 'boston', 'buffalo', 'calgary', 'charlotte', 'chattanooga', 'chicago', 'cincinnati', 'cleveland', 'coloradoSprings', 'columbus', 'dallas', 'dayton', 'daytonaBeach', 'denver', 'desMoines', 'elPaso', 'eugene', 'europe', 'ftWorth', 'fresno', 'grandJunction', 'greenBay', 'greensboro', 'houston', 'indianapolis', 'jacksonville', 'japan', 'kansasCity', 'keyWest', 'lafayette', 'lakeCity', 'laredo', 'lasVegas', 'lincoln', 'littleRock', 'losAngeles', 'macon', 'medford', 'memphis', 'mexia', 'mexico', 'miami', 'midland', 'milwaukee', 'minneapolis', 'modesto', 'montreal', 'nashville', 'newHaven', 'newOrleans', 'newYork', 'norfolk', 'oakland', 'oklahomaCity', 'omaha', 'orlando', 'ottawa', 'pensacola', 'philadelphia', 'phoenix', 'pittsburgh', 'pointReyes', 'portland', 'providence', 'provo', 'raleigh', 'redding', 'reno', 'richmond', 'rochester', 'sacramento', 'salem', 'salinas', 'saltLakeCity', 'sanAntonio', 'sanDiego', 'sanFrancisco', 'sanJose', 'sanLuisObispo', 'santaFe', 'saultSteMarie', 'savannah', 'seattle', 'stLouis', 'stamford', 'stockton', 'tallahassee', 'tampa', 'thunderBay', 'toledo', 'toronto', 'tucson', 'tulsa', 'uk1', 'uk2', 'vancouver', 'washington', 'westPalmBeach', 'wichita', 'winnipeg', 'yuma']
    if source not in cities or destination not in cities:
        print('Error: invalid name of cities, please try again from following list \n')
        for i in cities: print(i + '\n')
        exit()
    global maxqsize, numnodes   
    maxqsize = 0
    numnodes = 0
    if algorithm == 'DFS':
        finalpath = []
        path_cost = 0
        alreadyvisited = set()
        
        solution = depth_first_search(current_location(source, destination), alreadyvisited, path_cost, finalpath)
        
        print('Maximum length of queue was ' + str(maxqsize) + '\n')
        print('Total ' + str(numnodes) + ' cities were expanded in the process.\n')
        print('Path Cost : ' + str(solution[1]))
        print('Final path from ' + source +' to ' + destination + ' : ')
        print(solution[0])
            
    elif algorithm  == 'A*' or algorithm == 'Astar':
        solution = Astar(current_location(source, destination))
        
        print('Total ' + str(numnodes) + ' cities were expanded in the process.\n')
        print('Maximum length of queue was ' + str(maxqsize) + '\n')
        print('Path Cost : ' + str(solution[1]))
        print('Final path from ' + source +' to ' + destination + ' : ')
        print(solution[0])
    
    elif algorithm == 'RBFS':
        solution = rbfs(current_location(source, destination))
        
        print('Total ' + str(numnodes) + ' cities were expanded in the process.\n')
        print('Maximum length of queue was ' + str(maxqsize) + '\n')
        print('Path Cost : ' + str(solution[1]))
        print('Final path from ' + source +' to ' + destination + ' : ')
        print(solution[0])
        
    else:
        print("Error: Incorrect algorithm, please choose from : \n DFS, A*, and RBFS")
        exit()

if __name__ == '__main__':
    inpmap()
    MAP = mapofworld()
    main()