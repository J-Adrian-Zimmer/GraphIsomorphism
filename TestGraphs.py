from Graph import Graph

def mkTestGraph4():
   return Graph(
            ['a','b','c','d'],
            [ ('a','b'), 
              ('b','c'),
              ('c','a'),
              ('a','d')
            ]
         )

def mkTestGraph4b():    ## isomorphic with 4
     return Graph(
            ['a','c','b','d'],
            [ ('a','c'), 
              ('b','c'),
              ('b','a'),
              ('a','d')
            ]
         )

     return Graph(
            ['a','c','b','d'],
            [ ('a','c'), 
              ('b','c'),
              ('b','a'),
              ('a','d')
            ]
         )

def mk5Clique():
  return Graph(
       5,
       [ (x,y) for x in range(5) for y in range(5) ]
  )

def mkTestGraph6():
     return Graph(
               ['a','b','c','d','e','f'],
               [ ('a','b'), 
                 ('b','c'),
                 ('c','d'),
                 ('a','d'),
                 ('d','b'),
                 ('c','e')
               ]
            )

''' 
   Schematic of test graph 6

       a -- b    f
       |    |        (also edge between d and b)
       d -- c -- e

   rows of correct give number of shortest paths 
   from a source node to all nodes
'''

def mkTestGraph6b():  ## not isomorphic with 6
                      ## (d,b) edge replaced with
                      ## (a,c)
     return Graph(
               ['a','b','c','d','e','f'],
               [ ('a','b'), 
                 ('b','c'),
                 ('c','d'),
                 ('a','d'),
                 ('a','c'),
                 ('c','e')
               ]
            )


def mkPetersenGraph():
   return Graph(
       10,
       [ (0,1),(1,2),(2,3),(3,4),(4,0),    # outer polygon
         (5,6),(6,7),(7,8),(8,9),(9,5),    # inner polygon
         (0,5),(1,8),(2,6),(3,9),(4,7) ]   # btwn polygons
   )

class PossibleEdges:
   ## this keeps a list of edges (x,y) such that the ith 
   ## edge has x at 2*i position and y at 2*i+1 position

   ## the order of the edges in the list doesn't matter
   ## and changes with each restart

   from array import array

   def __init__(me,numNodes):
     me.totalNum = int( 0.5 + numNodes*(numNodes-1.0)/2.0 )
     me.edges = PossibleEdges.array('H',[0]*(2*me.totalNum))
     me.last_idx = me.totalNum-1
     edge_index = 0
     for i in range(numNodes):
        for j in range(i+1,numNodes):
           me.edges[ edge_index*2 ]   = i
           me.edges[ edge_index*2+1 ] = j
           edge_index += 1 
     assert edge_index-1 == me.last_idx

   def restart(me):
     me.last_idx = me.totalNum-1
   
   def remove(me,idx):
     idx2 = 2*idx
     lx2 = 2*me.last_idx
     x = me.edges[idx2]
     y = me.edges[idx2+1]
     me.edges[idx2] = me.edges[lx2]
     me.edges[idx2+1] = me.edges[lx2+1]
     me.edges[lx2] = x
     me.edges[lx2+1] = y
     me.last_idx -= 1
     return (x,y)
          
class MakeRandom:
   from random import SystemRandom,seed,randrange,randrange
   seed( SystemRandom().random() )

   def __init__(me,numNodes):
     me.numNodes = numNodes
     me.possible_edges = PossibleEdges(numNodes)
   
   def getEdges(me,numEdges):
     me.possible_edges.restart()
     assert numEdges > 0 and \
             numEdges < me.possible_edges.totalNum, (
               "MakeRandom: number of edges "
               "expected to be positive and less "
               " than total "
               "for an undirected graph without "
               "loops or multiple edges" 
            )
     
     count = 0
     # print 'generating ' + str(me.possible_edges.totalNum) + \
     #      ' edge pairs '
     edges = []
     while count<numEdges:
        i = MakeRandom.randrange(me.possible_edges.totalNum)
        edges.append(me.possible_edges.remove(i))
        count += 1 
     return edges     

   def getIsoPair(me,density=0.5 ):
       ## return two graphs with different labelling
       numEdges = int( 
          0.5 +  me.possible_edges.totalNum * density ) 
       print "making isometric Pair with " + \
             str(me.numNodes) + \
             " nodes and " + str(numEdges) + " edges."
       edges = me.getEdges(numEdges)
       gph1 = Graph(me.numNodes,edges)
       return (gph1,gph1.relabelledClone())


   def getNonIsoPair(me,density=0.5):
      ## return two graphs with different labelling
      ## they have same number of edges but one edge
      ## is different
      
      numEdges = int( 
          0.5 +  me.possible_edges.totalNum * density ) 
      print "making non isometric Pair with " + \
            str(me.numNodes) + \
            " nodes and " + str(numEdges) + " edges."
      edges = me.getEdges(numEdges+1)
       
      ## make graphs by removing a random edge
      i = MakeRandom.randrange(numEdges)
      j = i # for 2nd graph need random j different from i
      while j==i:  j = MakeRandom.randrange(numEdges)

      return ( 
              Graph(me.numNodes, edges[0:i] + edges[i+1:]),
               
              Graph(me.numNodes, edges[0:j] + edges[j+1:]).
                 relabelledClone() 
             )
