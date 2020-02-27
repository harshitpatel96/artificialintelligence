# Globe Puzzle Solution Search
### by Harshit Patel(@hpatel24)

The globe puzzle is a rubiks cube type puzzle with 30 tiles that can rotate in three axis.
Mathematically the axis were represented as (90, x) (y, 0/180) and (y, 90/27), where x is a number between 0 to 330 and y is a number between 0/90 to 180/270

Algorithms are implemented on a Python3 environment on a Windows machine
The problem state was taken from an mb file and preprocessed in python using inbuilt string manipulation functions.

configuring and running the code:

To execute the code use the following command line
python search.py <ALG> <FILE>
 
where ALG is one of BFS, Astar, or RBFS 
and FILE is input file name which would be initial state of puzzle

The program would ask the user to choose from three algorithms, that are Breadth First Search, A* Search, and Recursive Best First Search.
It uses the selected algorithm to solve the puzzle file.
After successfull completion of the puzzle, it would return the 
1. number of states expanded
2. max queue size
3. path cost
4. operations which one should use if they want to solve the puzzle on a real globe.
