    # -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 02:05:34 2019

@author: HARSHIT
"""

#import queue
from collections import deque #double ended queue
import queue
from math import inf, floor

# input file parser
def can_opener(fname):
    with open(fname, 'r') as f:
        data = f.readlines()
    
    initial_state_dict = {} # in dictionary format
    initial_state = [] # in list format
    goal_state_dict = {} # in dict format
    goal_state = [] # in list format    
    
    for k in range(len(data)-2):
        i1 = data[k+1].find(', (')
        i2 = data[k+1].find('),')
        i3 = data[k+1].find('t')
        i4 = data[k+1].find('))')
        initial_state_dict['tile' + str(k+1)] = data[k+1][i1+2:i2+1] # extracting current state from problem in dictionary format
        goal_state_dict['tile' + str(k+1)] = data[k+1][i3+1:i4+1] # extracting goal state from the problem
        i_sep_init = initial_state_dict['tile' + str(k+1)].find(',') # finds , which seperates lat and long
        i_end_init = initial_state_dict['tile' + str(k+1)].find(')') # finds ) which ends the current state dep
        i_sep_goal = goal_state_dict['tile' + str(k+1)].find(',') # similarly for goal states
        i_end_goal = goal_state_dict['tile' + str(k+1)].find(')') # and for end poistion of goal state
        initial_state.append((int(initial_state_dict['tile' + str(k+1)][1:i_sep_init]), int(initial_state_dict['tile'+str(k+1)][i_sep_init+1:i_end_init])))
        goal_state.append((int(goal_state_dict['tile' + str(k+1)][1:i_sep_goal]), int(goal_state_dict['tile' + str(k+1)][i_sep_goal+1:i_end_goal])))
       
    return initial_state, goal_state
    
# Action class, contains functions that calculates what happens when a particular action is performed
class action:
    def incEquator(initial_state):
        new_state = []
        for i in range(len(initial_state)):           
            if initial_state[i][0] == 90:
                new_state.append((90, (initial_state[i][1] + 30)%360))
            else: 
                new_state.append(initial_state[i])
                
        return new_state
    
    def decEquator(initial_state):
        new_state = []
        for i in range(len(initial_state)):
            
            if initial_state[i][0] == 90:
                new_state.append((90, (initial_state[i][1] - 30)%360))
            else: 
                new_state.append(initial_state[i])
                
        return new_state
    
    def inc0180(initial_state):
        new_state = []
        for i in range(len(initial_state)):
            if initial_state[i] == (0, 0):
                new_state.append((30, 180))
            elif initial_state[i] == (180, 180):
                new_state.append((150, 0))
            elif initial_state[i][1] == 0:
                new_state.append((initial_state[i][0] - 30, 0))
            elif initial_state[i][1] == 180:
                new_state.append((initial_state[i][0] + 30, 180))
            else:
                new_state.append(initial_state[i])
                
        return new_state
    
    def dec0180(initial_state):
        new_state = []
        for i in range(len(initial_state)):
            if initial_state[i] == (30, 180):
                new_state.append((0, 0))
            elif initial_state[i] == (150, 0):
                new_state.append((180, 180))
            elif initial_state[i][1] == 0:
                new_state.append((initial_state[i][0] + 30, 0))
            elif initial_state[i][1] == 180:
                new_state.append((initial_state[i][0] - 30, 180))
            
            else:
                new_state.append(initial_state[i])
                
        return new_state
    
    def inc90270(initial_state):
        new_state = []
        for i in range(len(initial_state)):
            if initial_state[i] == (30, 90):
                new_state.append((0, 0))
            elif initial_state[i] == (0, 0):
                new_state.append((30, 270))
            elif initial_state[i] == (150, 270):
                new_state.append((180, 180))
            elif initial_state[i] == (180, 180):
                new_state.append((150, 90))
            elif initial_state[i][1] == 90:
                new_state.append((initial_state[i][0] - 30, 90))
            elif initial_state[i][1] == 270:
                new_state.append((initial_state[i][0] + 30, 270))
            
            else:
                new_state.append(initial_state[i])
             
        return new_state
    
    def dec90270(initial_state):
        new_state = []
        for i in range(len(initial_state)):
            if initial_state[i] == (30, 270):
                new_state.append((0, 0))
            elif initial_state[i] == (0, 0):
                new_state.append((30, 90))
            elif initial_state[i] == (150, 90):
                new_state.append((180, 180))
            elif initial_state[i] == (180, 180):
                new_state.append((150, 270))
            elif initial_state[i][1] == 90 and initial_state[i] != (0, 0):
                new_state.append((initial_state[i][0] + 30, 90))
            elif initial_state[i][1] == 270 and initial_state[i] != (180, 180):
                new_state.append((initial_state[i][0] - 30, 270))
            
            else:
                new_state.append(initial_state[i])
             
        return new_state

# parent constructor for node 
class parent(object):
    def __init__(self, state, parent, path_cost, action):
        self.state = state
        self.parent =  parent
        self.path_cost = path_cost
        self.action = action
    
    def __lt__(self, other):
        return ((self.state, self.path_cost, self.action) < (other.state, other.path_cost, other.action))

    def __le__(self, other):
        return ((self.state, self.path_cost, self.action) <= (other.state, other.path_cost, other.action))

    def __gt__(self, other):
        return ((self.state, self.path_cost, self.action) > (other.state, other.path_cost, other.action))

    def __ge__(self, other):
        return ((self.state, self.path_cost, self.action) >= (other.state, other.path_cost, other.action))

    def __repr__(self):
        return "%s %s" % ((self.state, self.path_cost, self.action))
    
# parent constructor to use in RBFS, it contains an extra element f
class parent1(object):
    def __init__(self, state, parent, path_cost, action, f):
        self.state = state
        self.parent =  parent
        self.path_cost = path_cost
        self.action = action
        self.f = f
        
    def __iter__(self):
            return self.parent
    
    def __next__(self):
        return self.parent.parent
    
    def __lt__(self, other):
        return ((self.state, self.path_cost, self.action) < (other.state, other.path_cost, other.action))

    def __le__(self, other):
        return ((self.state, self.path_cost, self.action) <= (other.state, other.path_cost, other.action))

    def __gt__(self, other):
        return ((self.state, self.path_cost, self.action) > (other.state, other.path_cost, other.action))

    def __ge__(self, other):
        return ((self.state, self.path_cost, self.action) >= (other.state, other.path_cost, other.action))

    def __repr__(self):
        return "%s %s" % ((self.state, self.path_cost, self.action))

# Child constructor for child node
class child_node_constructor(object):
    def __init__(self, state, parent, path_cost, action):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.action = action
    
    def __lt__(self, other):
        return ((self.state, self.path_cost, self.action) < (other.state, other.path_cost, other.action))

    def __le__(self, other):
        return ((self.state, self.path_cost, self.action) <= (other.state, other.path_cost, other.action))

    def __gt__(self, other):
        return ((self.state, self.path_cost, self.action) > (other.state, other.path_cost, other.action))

    def __ge__(self, other):
        return ((self.state, self.path_cost, self.action) >= (other.state, other.path_cost, other.action))

    def __repr__(self):
        return "%s %s" % ((self.state, self.path_cost, self.action))


# Child constructor to use in RBFS, it contains an extra element f
class child_node_constructor1():
    
    def __init__(self, state, parent, path_cost, action, f):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.action = action
        self.f = f

    def __lt__(self, other):
        return ((self.state, self.path_cost, self.action) < (other.state, other.path_cost, other.action))

    def __le__(self, other):
        return ((self.state, self.path_cost, self.action) <= (other.state, other.path_cost, other.action))

    def __gt__(self, other):
        return ((self.state, self.path_cost, self.action) > (other.state, other.path_cost, other.action))

    def __ge__(self, other):
        return ((self.state, self.path_cost, self.action) >= (other.state, other.path_cost, other.action))

    def __repr__(self):
        return "%s %s" % ((self.state, self.path_cost, self.action))
            

                 
# function to find what a particular action does on initial state
def child_node(parent, act):
    if act == 'incEquator':
        new_state = action.incEquator(parent.state)
    elif act == 'decEquator':
        new_state = action.decEquator(parent.state)
    elif act == 'inc0180':
        new_state = action.inc0180(parent.state)
    elif act == 'dec0180':
        new_state = action.dec0180(parent.state)
    elif act == 'inc90270':
        new_state = action.inc90270(parent.state)
    elif act == 'dec90270':
        new_state = action.dec90270(parent.state)
    path_cost = parent.path_cost + 1
    child = child_node_constructor(new_state, parent, path_cost, act)

    return child
    
# function to find what a particular action does on initial state (for RBFS)
def child_node1(parent, act, f):
    if act == 'incEquator':
        new_state = action.incEquator(parent.state)
    elif act == 'decEquator':
        new_state = action.decEquator(parent.state)
    elif act == 'inc0180':
        new_state = action.inc0180(parent.state)
    elif act == 'dec0180':
        new_state = action.dec0180(parent.state)
    elif act == 'inc90270':
        new_state = action.inc90270(parent.state)
    elif act == 'dec90270':
        new_state = action.dec90270(parent.state)
    path_cost = parent.path_cost + 1
    child = child_node_constructor1(new_state, parent, path_cost, act, f)

    return child
    
# Breadth First Search Algorithm
def breadth_first_search(initial_state):
    path_cost = 0
    parent_node = parent(initial_state, parent, path_cost, 0)

    if goal_test(parent_node.state) == True :
        print("The puzzle is solved (initial state itself is goal state) path_length = 0, path_cost = 0, sequence of action = NA")
        return parent_node
    possible_actions = ['incEquator', 'decEquator', 'inc0180', 'dec0180', 'inc90270', 'dec90270']
    frontier = deque()
    qsize = len(frontier)
    frontier.append(parent_node)

    explored_nodes = []

    while 1:
        if frontier:
            pass
        else:
            print("Failure")
            return 0
        qsizecurrent =  len(frontier)
        if qsizecurrent > qsize:
            qsize = qsizecurrent
            
        node1 = frontier.popleft()
        
        explored_nodes.append(hash(str(node1.state)))

        for act in range(len(possible_actions)):
            
            flag_explored_nodes = False # used for checking if child is present in explored nodes
            flag_frontier = False # used for checking if child is present in queue
            
            child = child_node(node1, possible_actions[act])

            # check if child is present in explored_states                
            if hash(str(child.state)) in explored_nodes:
                flag_explored_nodes = True # that is when child state is present in 
            
            # check if child is present in queue
            if child in frontier:
                    flag_frontier = True

            # if child is not present either in explored_nodes or in frontier then execute this
            if (flag_explored_nodes == False) and (flag_frontier == False):

                if goal_test(child.state):
                    print("The puzzle is solved after exploring " + str(len(explored_nodes)) + " states. The maximum size of queue was " + str(qsize))
                    return child
            
                frontier.append(child)

            
# A star search algorithm
def A_star_search(initial_state):
    path_cost = 0
    parent_node = parent(initial_state, 0, path_cost, 0)

    frontier = queue.PriorityQueue()
    temp = queue.PriorityQueue()
    qsize = frontier.qsize()
    frontier.put((0, parent_node)) # path_cost = 0
    possible_actions = ['incEquator', 'decEquator', 'inc0180', 'dec0180', 'inc90270', 'dec90270']
    
    explored_nodes = []
    while(1):
        if frontier.empty() == True:
            return print('Failure')
        
        if frontier.qsize() > qsize:
            qsize = frontier.qsize()
            
        node1 = frontier.get()

        if goal_test(node1[1].state) ==  True:
            print('The puzzle is solved after exploring ' + str(len(explored_nodes)) + ' nodes and the maximum size of queue was ' + str(qsize) )
            return node1[1]
        
        explored_nodes.append(hash(node1[1]))
        for act in possible_actions:
            flag_explored_nodes = False
            flag_frontier = False
            
            child = child_node(node1[1], act)
            if hash(child) in explored_nodes:
                flag_explored_nodes = True
                
            
            for i in range(frontier.qsize()):
                temp1 = frontier.get()
                temp.put(temp1)
                if temp1[1].state == child.state:
                    flag_frontier = True
                    break
            
            length = temp.queue
            length = len(length)
            for j in range(length):
                temp2 = temp.get()
                frontier.put(temp2)
                
            temp = queue.PriorityQueue()
            
            if flag_frontier == False and flag_explored_nodes == False: 
                h = heuristic_function(child.state)
                frontier.put((child.path_cost + h, child))
                #frontier.put((node['path_cost'], node))
            
            elif (flag_frontier == True) and (node1[0] > child.path_cost + h):
                for l in range(frontier.qsize()):
                    temp2 = frontier.get()
                    if temp2[1].state == child.state:
                        continue
                    else:
                        temp.put(temp2)
                for r in range(temp.qsize()):
                    temp2 = temp.get()
                    frontier.put(temp2)

# Heuristic Function
def heuristic_function(current_state):
    globe_junctions = [(90, 0), (90, 180), (90, 90), (90, 270), (0, 0), (180, 180)]
    h = list()
    h_to_junct = []
    for i in range(len(current_state)):
        for j in range(len(goal_state)):

            if current_state[i] == goal_state[j]:
                for s in globe_junctions:
                    if goal_state[i][0] == goal_state[j][0] == 90:
                        h_to_junct.append((abs(goal_state[i][1] - s[1]) + abs(s[1] - goal_state[j][1])))#%360)
                    elif goal_state[i][1] ==  goal_state[j][1]:
                        h_to_junct.append(abs(goal_state[i][0] - s[0]) + abs(s[0] - goal_state[j][0]))
                    elif (goal_state[i][1] != goal_state[j][1]):
                        h_to_junct.append(abs(goal_state[i][0] - s[0]) + abs(s[0] - goal_state[j][0]))
                    
                h.append(floor(min(h_to_junct)))
    
    return sum(h)/12


# Goal Test
def goal_test(initial_state):
    if initial_state == goal_state:
        return True
    else:
        return False

# Recursive Best First Search Algorithm
def recursive_best_first_search(initial_state):
    parent_node = parent1(initial_state, 0, 0, 0, 0)
    inf = float('inf')
    result =  RBFS(parent_node.state, parent_node, inf)
    print(result)
    return result

def RBFS(current_state, parent_node, f_limit):
    possible_actions = ['incEquator', 'decEquator', 'inc0180', 'dec0180', 'inc90270', 'dec90270']
    print(parent_node.action)
    if goal_test(current_state) == True:
        return parent_node
    
    successors = []
    for act in possible_actions:
        child = child_node1(parent_node, act, parent_node.f)
        successors.append(child)
        
    if len(successors) == 0:
        return('Failure', inf)
      
    for s in successors:
        h = heuristic_function(s.state)
        s.f = max(s.path_cost + h, s.f)
    
    while 1:
        best = successors[0]
        for l in successors:
            if l.f < best.f:
                best = l
                
        if best.f > f_limit:
            return "Failure", best.f
        
        q = []
        for p in successors:
            if best.f == p.f:
                continue
            q.append(p.f)
            
        alternative = min(q)
                
        result, best.f = RBFS(best.state, best, min(f_limit, alternative))
        if result ==  "Failure":
            continue
        else:
            return result

print("Please select the algorithm you want to use to solve the puzzle: ")
print("1. Breadth First Search")
print("2. A* Search")
print("3. Recursive Best First Search")
print("................................")


inp = input(': ')
print("The puzzle used over here is Puzzle2-0")
print(" ")

#get initial and goal state
initial_state, goal_state = can_opener("D:/NCSU/Semester_1/CSC520_AI/Assign2Files/Assign2Files/PathN-7.mb")
goal_hash = hash(str(goal_state))

if inp == '1':
    Result = breadth_first_search(initial_state)
elif inp == '2':
    Result = A_star_search(initial_state)
elif inp == '3':
    Result = recursive_best_first_search(initial_state)
else:
    print("Error: please print numbers 1, 2 or 3 only: ")
    from sys import exit
    exit()
    
path = []
c = Result
for i in range(Result.path_cost):
    path.append(c.action)
    c = c.parent

print('Path cost to reach goal state is ' + str(Result.path_cost))

for i in range(len(path)):
    i = i+1
    if path[-i] == 'incEquator':
        state = 'Increment Equator'
    elif path[-i] == 'decEquator':
        state = 'Decrement Equator'
    elif path[-i] == 'inc0180':
        state = 'Increment Longitude 0-180'
    elif path[-i] == 'dec0180':
        state = 'Decrement Longitude 0-180'
    elif path[-i] == 'inc90270':
        state = 'Increment Longitude 90-270'
    elif path[-i] == 'dec90270':
        state = 'Decrement Longitude 90-270'
    
    print(str(i) +'. '+ state)