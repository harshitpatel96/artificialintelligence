# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:16:57 2019

@author: HARSHIT
"""
# Created by Harshit Patel on a Windows 8.1 Machine #
# Date 10/15/2019 #
# Developed and tested on Python version 3.5.1 #

# import necessary libraries
import numpy as np
import queue
import time
import sys


# constructor for constraint satisfaction problem definition
# constructor only used for problem definition purpose
# variable and domain are used in other functions
# constraint is only for representation purpose it is not used anywhere
class QueenGraph:
    def __init__(self, variables, domain):
        self.variables = variables
        self.domain = domain
        self.constraints = [((self.variables['Q'+str(i+1)] != self.variables['Q'+str(j+1)]) and (self.variables['Q'+str(i+1)]-self.variables['Q'+str(j+1)] != (i+1)-(j+1))) for i in range(len(self.variables)) for j in range(len(variables)) if i!= j]

# checks if current assignment is complete i.e. when the all variables are assigned a value and are satisfying constraints
def complete(assignment, n):
    if len(assignment) == n:
        constraints = [((assignment['Q'+str(i+1)] != assignment['Q'+str(j+1)]) and (assignment['Q'+str(i+1)]-assignment['Q'+str(j+1)] != (i+1)-(j+1))) for i in range(n) for j in range(n) if i != j]
        if constraints.count(False) == 0: # even if there is one constraint which is not satisfied it is wrong solution
            return True
    return False
    
# intiailization function (followed algorithm as provided in book)
def BackTrackingSearch(csp, ALG):
    return BackTrack({}, csp, ALG) # input blank assignment to csp

# main BackTrack function
def BackTrack(assignment, csp, ALG):
    # check if current assigment is complete
    if complete(assignment, len(csp.variables)):
        return assignment
    
    infered_key = set() # stores key for variables whose domain is reduced to singleton set after inference
    var = select_unassigned_var(csp, assignment) # select unassigned variable
    
    for value in csp.domain[var]: # for each value in domain of variable
        qdom = dict(csp.domain) # temp variable to store current domain of problem (used to restore domain in case of backtrack due to failure)
        if consistent(value, assignment, var): # checks if value is consistent with assignment
            assignment[var] = value # if consistent then assign var = value
            inferences = Inference(csp, var, value, assignment, ALG) # take inference using user specified algorithm
            
            if inferences != 'failure': # if inference is NOT failure (i.e. domains are not same as before)
    
                for k in csp.domain.keys(): # for each variable
                
                    if k in assignment: # if that variable is already assigned some value than ignore it and move to next variable
                        continue
                    
                    if k != var: # if variable k is not the same as variable (the one selected earlier) then do this
                        if len(csp.domain[k]) == 1: # if length of variable k is reduced to singleton set then add it to assignment if it is consistent with it
                            new_val = csp.domain[k].pop() 
                            csp.domain[k].add(new_val) # restore domain of that variable (because I used pop I have to restore it)
                            if consistent(new_val, assignment, k): # if value is consistent with assignment then add it to assignment
                                assignment[k] = csp.domain[k].pop()
                                csp.domain[k].add(assignment[k])
                                infered_key.add(k) # add k to infered_key 
                                # (to keep track of variables assigned via 
                                # inference vs inferences assigned 
                                # via BackTracking)
                            
                result = BackTrack(assignment, csp, ALG) # go forward in tree
                if result != 'failure': # if BackTrack result is a success (i.e. a result state)
                    # call global variables
                    global ResCount
                    global n
                    global RFile
                    
                    ResCount += 1 # add 1 to no. of results found
                    resArr = np.zeros((n,n)) # ressArr is a numpy array and 
                    # would be used to represent assignment in form of 0's and 
                    # 1's where 1 means queen is placed at that place
                    
                    for k in assignment.keys(): # add 1 to queens position defined by assignment
                        i = int(k[1:])-1
                        resArr[i][assignment[k]-1] = 1
                    
                    # line 91 to 97 writes ouptput to RFile
                    f = open(RFile, 'a')
                    f.write('Solution ' + str(ResCount) + ': \n')
                    for i in range(n):
                        f.write('Q'+str(i+1)+':' + str(assignment['Q'+str(i+1)]) + ' ')
                    f.write('\n')
                    f.write(str(resArr) + '\n' + '\n')
                    f.close()
                    
                    # if 2*n solutions found then return failure
                    if ResCount == 2*len(csp.variables):
                        return 'failure'
                # if 2*n solutions found then return failure (did the same 
                # thing twice because when it would backtrack then this would 
                # return failure instead of finding new results)
                if ResCount == 2*len(csp.variables):
                    return 'failure'
                
                global BT
                csp.domain = qdom # reseting the domain when backtracked 
                # (just to make sure algorithm is on track)
                BT = BT+1 # count no. backtrack up by one
                
            assignment.pop(var) # remove variable = value from assignment
            for p in infered_key: # remove all inferences from assignment
                assignment.pop(p)
            infered_key = set() # reset infered_key directory 
            # (so that it does not do unwanted pops and cause errors)
            
    return 'failure'

# this function checks if variable = value is consistent with assignment           
def consistent(value, assignment, var):
    if len(assignment) != 0: # to make sure that when assignment is 
        # empty (initial assignment) then the function returns True
        for key in assignment.keys(): # check if var = value is consistent with
            # each var in assignment
            if key != var:
                if (assignment[key] == value) or (abs(assignment[key]-value) == abs(int(key[1:])-int(var[1:]))):
                    return False
            
    return True

# select unassigned variable in csp based on minimum remaining values heuristic
def select_unassigned_var(csp, assignment):
    # in case of blank assignment (initial assignment) it would choose Q1
    k = 'Q1'
    
    # for each variable if it is not in assignment choose it if it has shortest 
    # domain of all
    for key in csp.domain.keys():
        flag = True #not present in assignment
        if key in assignment.keys():
            flag = False #present in assignment
        if key != k and flag:
            if len(csp.domain[key])< len(csp.domain[k]):
                k = key
    
    return k
# I have choosen not to order domain values in order to save time on 
# my algorithm

# Inference calls algorithms as given by user (only FOR or MAC)
def Inference(csp, var, value, assignment, ALG):
    if ALG == 'FOR':
        return FOR(csp, var, value, assignment)
    elif ALG == 'MAC':
        return MAC(csp, var, value, assignment)
    else:
        print('Error: ALG mismatch')
        return 'failure'

# Forward checking algorithm
def FOR(csp, var, value, assignment):
    qdom = dict(csp.domain) # saving current csp domain to reset it in case FOR fails
    
    # for each value in current domain if that value is not consistent with 
    # current assignment then remove it.
    for k in csp.domain.keys():
        flag = True # k not in assignment
        cd = set(csp.domain[k])
        if k in assignment.keys():
            flag = False # k present in assignment
        if k != var and flag:
            for i in csp.domain[k]:
                if (value == i) or (abs(int(var[1:]) - int(k[1:])) == (abs(value - i))):
                    cd.remove(i)
                    
            if len(cd) == 0: # in case if domain of some variable becomes empty
                # then return failure and reset csp domain
                csp.domain = qdom
                return 'failure'
            
            csp.domain[k] = cd # in case of success update csp domain
            
    return 'success'

# Maintaining Arc Consistency algorithm
def MAC(csp, var, value, assignment):
    neighbours = queue.Queue() # a queue to store binary constrained nodes
    n = [('Q'+str(i+1), var) for i in range(len(csp.variables)) if ('Q'+str(i+1) != var) and ('Q'+str(i+1) not in assignment)]
    # above line generates neighbours of var
    
    # add all of them to queue
    for i in n:
        neighbours.put(i)
    
    XiDom = dict(csp.domain) # saving current var domain to reset it in case MAC fails
    
    while (neighbours.empty() ==  False):
        X = neighbours.get() # pop a node from queue

        if revise(csp, X[0], X[1], var, value): # if domain is revised then go inside
            
            if len(csp.domain[X[0]]) == 0: # if revision caused empty domain then reset it and return failure
                csp.domain = XiDom
                return 'failure'
            
            # below line generates neighbour of variable whose domain just got changed
            neighbours_Xi = {('Q'+str(i+1), X[0]) for i in range(len(csp.variables)) if ('Q'+str(i+1) != X[0]) and ('Q'+str(i+1) not in assignment)} 
            
            # add all of those neighbours to queue
            for i in neighbours_Xi:
                neighbours.put(i)
                
    return 'success'

# function revise makes a revision on variable Xi's domain
def revise(csp, Xi, Xj, var, value):
    revised = False # initialize revision flag to false
    nXi = set(csp.domain[Xi]) # nXi is domain of variable Xi
    
    for i in csp.domain[Xi]:
        Rflag = [] # Rflag list is used to keep track that value i in domain 
        # of Xi is not consistent with ANY of the value in domain of Xj
        
        if Xj == var:
            domain = {value} # if Xj is assigned variable itself then its domain is value itself
        else: 
            domain = csp.domain[Xj] # else it is domain of that variable
         
        # for each value in domain check if current value is consistent
        for j in domain:
            if (i == j) or (abs(i-j) == abs(int(Xi[1:])-int(Xj[1:]))):
                Rflag.append(True)
                continue
            Rflag.append(False)
        
        
        if Rflag.count(False) == 0: # if Xi = i is not consistent with ALL j in Xj then and only then remove it
            nXi.remove(i)
            revised = True


    csp.domain[Xi] = nXi # update domain of Xi
    return revised
    
    
def main():
    
    # Global variables that are used throughout the program
    global n # no. of queens
    global ResCount # no. of results found (to cut-off program execution at 2*n results)
    global BT # counter for no. of BackTracking Steps
    global result_flag # result flag to indicate the program that it found at least one result, if it is True than the computer knows that it found one result and resets domain of every variable
    global RFile # it is declared globally so that we can use it in writing solutions to a file
    
    # Taking from user
    ALG = sys.argv[1]
    n = int(sys.argv[2])
    CFile = sys.argv[3]
    RFile = sys.argv[4]
    
    # initialising global variables
    ResCount = 0
    BT = 0
    result_flag = False
    
    # This code writes Variables, Domains and Constraints to input CFile
    f = open(CFile, 'w')
    f.write('Variables: Domain' + '\n')
    for i in range(n):
        f.write('Q'+str(i+1)+' : ')
        for j in range(n):
            if j == 0:
                f.write("{")
            if j != n-1:
                f.write(str(j+1) + ', ')
                continue
            f.write(str(j+1) + "}")
    
        f.write('\n' + '\n')
    
    for i in range(n):
        for j in range(n):
            if i != j:
                f.write('Q' + str(i+1) + ' not in same column/row as Q' + str(j+1) + ' \n i.e. Q' + str(i+1) + ' != Q' + str(j+1) + '\n \n')
                f.write('Q' + str(i+1) + ' not in same diagonal as Q' + str(j+1) + ' \n i.e. abs(i - j) != abs(Q'+ str(i+1) + ' - Q' + str(j+1) + ') \n \n')
                    
    f.close()
        
    f = open(RFile, 'w')
    f.write("") # initializes empty RFile, in case there is a file with same name it overwrites it
    f.close()

    # declaring constraint satisfaction problem
    variables = {'Q'+str(i+1): 0 for i in range(n)}
    domain = {'Q'+str(i+1): {j+1 for j in range(n)} for i in range(n)}
    problem = QueenGraph(variables, domain)
    
    # initialize time
    start_time = time.time()
    BackTrackingSearch(problem, ALG)
    total_time  = time.time() - start_time
    print("It found %d solutions for this problem" % ResCount)
    print("It took %s seconds to find solutions to this problem" % total_time)
    print("It BackTracked %d times" % BT)
    print("(: (: (: Cheers!!!!!!!!!! :) :) :)")
    f = open(RFile, 'a')
    f.write("\nIt found " + str(ResCount) + " solutions for this problem")
    f.write("\nIt took " + str(total_time) + " seconds to find solutions to this problem")
    f.write("\nIt BackTracked " + str(BT) + " times")
    f.write("\n (: (: (: Cheers!!!!!!!!!! :) :) :)")
    f.close()


# Run the program
if __name__ == '__main__':
    main()