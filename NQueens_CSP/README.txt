The program solves famous NQueens problem using BackTracking with Forward Checking or Maintaining Arc Consistency Inference Algorithms.

In order to use this code, the system requirements are:
- O/S - Any
- Python3
- Python3 libraries - Numpy, sys, time, queue
In order to use this code, please follow given steps:

1. open terminal
2. open path where the NQueens file is stored
3. Enter the following line in terminal:
	python NQueens.py ALG N CFile RFile
	where ALG is one of FOR or MAC
		N is no. of queens
	     CFile is the file to which you want to write constraints
	     RFile is the file to which you want all outputs

Open successful execution of code. 
The code would generate two files CFile and RFile
1. CFile - contains all the variables, domains, and constraints of the constraint satisfaction problems for NQueens for no. of queens = N
2. RFile - contains result, i.e. all the possible placements that the algorithm found for this problem.
(**Note: This program is capped at a total of 2*N outputs for any given N. So it may or may not return all possible solution depending upon N)

3. It would also show following three things:
	i. No. of solutions found
       ii. Time taken to find those solutions
      iii. No. of times the algorithm had to backtrack.

The code is well written. It also has ample amount of comments, to walk you through it.