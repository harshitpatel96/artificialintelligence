# Path Search

This program is a path finding program which finds the path between two cities on a map given to the program using a prolog file.

It can use one of the three Search algorithms from BFS, A* and IDFS.

You can run the program from command line using following line:

    python path_search.py algo src dst
    
where, `algo` is name of the algorithm (i.e. BFS, Astar, or IDFS)
`src` is the name of the source
`dst` is the name of the destination

For example, the following code would find the path from New york city to New jersey city using Astar algorithm.

    python path_search.py Astar NewYork NewJersey
    
