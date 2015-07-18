#What:

A class that implements an algorithm for finding isomorphisms between two undirected graphs.  Variations of this algorithm have been in my mind since I finished my Ph.D. thesis in graph theory 45 years ago.  My career deviated from graph theory but I have returned to this problem now and then.  I have not been able to find a variation I could prove correct and show is polynomial time.  This version is O(N<sup>3</sup>) but may report failure to know whether the two graphs are isomorphic.   It has not failed on the random graphs I have tried.  My randomization and testing programs are included for your examination.  It may be that a more systematic approach to finding a counter example would work where my randomized graphs have not.  It is quite apparent that I am not the person to do that or carry this line of thinking forward.

#Usage:

from Graph import Graph
from GraphIsomorphism import checkIsomorphic

'''
checkIsomorphic works on two undirected graphs, gph1 and gph2

Execution ends with one of three procedures you write:

def isoAction(perm):
    # executed if an isomorphism is found
    # perm is explained below

def noIsoAction():
    # executed if graphs are not isomorphic

def failAction():
    # executed if algorithm fails
    # this has yet to happen
    # see the tests folder

checkIsomorphic requires a graph created with this way

gph = Graph(n,edges)

where n is either the number of nodes or a list of nodes and edges
is a list of edges.   Although the algorihm has been written for
undirected graphs, edges are specified as ordered pairs (x,y).  Here
x and y are in range(n) if n is an int or chosen from n if n is a
list of nodes.   It is not necessary to enter both (x,y) and (y,x)
but it will not hurt to do so.

The Graph constructor maps the nodes on to range(<number of nodes>)
and works solely with 16 bit integers.  See the toDeclared and
fromDeclared functions in Graph.py for conversions between internal
form and your node names.

When an isomorphism is found it is returned as a vector perm of
values from range(<number of nodes>).  Each node v in the first
graph passed to checkIsomorphic is mapped by perm(v) to the node in
the second isomorphism.  Conversion from and to your node names is
something you will have to arrange for.

Once the graphs gph1 and gph2 as well as the three functions
described above have been established you run checkIsomorphic this
way.  (Examples can be found in the tests folder) 
'''

gc.enable()

checkIsomorphic( 
   gph1, gph2, isoAction, noIsoAction, failAction
)
'''

[J Adrian Zimmer](http://www.jazimmer.net)
