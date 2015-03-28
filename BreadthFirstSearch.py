from Graph import Graph
from collections import defaultdict

class BreadthFirstSearch:

   def __init__(
      me,
      gph,    ## graph as in Grapy.py
      source, ## node to start bfs
      process,    ## called once for every node
                  ## process(
                  ##   node,   
                  ##   dist  -- node's distance from source
                  ## )
      processSame,## called once for every edge whose end
                  ## nodes are same distance from source
                  ## processSame(
                  ##   node, 
                  ##   dist,     -- distance from source of
                  ##                          -- both nodes
                  ##   adjacent_node   -- other end of edge
                  ## )
      processOut  ## called once for every edge that leads
                  ## outward from source
                  ## processOut(
                  ##   node, 
                  ##   dist, -- node's distance from source
                  ##   adjacent_node   -- other end of edge
                  ##             -- distance will be dist+1
                  ## )
   ):
      #print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++'
      me.process = process
      me.processSame = processSame
      me.processOut = processOut
      me.gph = gph
      me.cur_level = -1;
      me.dists = defaultdict( lambda: me.cur_level+1 )
                 ## process_a_node adjusts me.cur_level 
                 ## so that default is always correct 
                 ## cool!
      
      ## set up breadth first queue
      ## this should be faster than outofbox stuff
      me.q = [None]*(gph.size*gph.size)
             ## array queue that will never wrap
      me.q[0] = source
      me.qF = 0;  ## front index
      me.qN = 1;  ## next empty cell index
      me.onQ = [False] * gph.size
                  ## nodes onQ immediately after they
                  ## have been processed as an adjacency
                  ## marking happens as nodes are put 
                  ## on queue for normal processing 
      me.onQ[source] = True
      
      # here's the entire action
      while me.process_a_node(): pass
   
   def enQ(me,node):
      me.q[me.qN] = node
      me.qN += 1

   def deQ(me):
      me.qF += 1
      return me.q[me.qF-1]
   
   def frontQ(me):
      return None if me.emptyQ() \
                  else me.q[me.qF]

   def emptyQ(me):
      return me.qF==me.qN

   def process_a_node(me):
      ## preq: not emptyQ  
      ##       defaultdict has assigned dists[frontQ] 
      cur = me.deQ()
      me.cur_level = me.dists[cur]
      client_wants_continue = me.process(cur,me.cur_level)
      #gd = lambda z: me.gph.toDeclared(z)
      #adjs = []
      #for a in me.gph.adjIter(cur): adjs.append(a)
      #print gd(cur) + "'s adjacencies: " + \
      #      ','.join( [ gd(a) for a in adjs ] )
      for adj in me.gph.adjIter(cur):
        if client_wants_continue:
           if me.dists[adj]==me.cur_level and  adj<cur:
              client_wants_continue = \
                 me.processSame(cur, me.cur_level, adj)
           elif me.dists[adj] == me.cur_level + 1:
              client_wants_continue = \
                 me.processOut(cur, me.cur_level, adj)
           if not me.onQ[adj]:
             me.enQ(adj)
             me.onQ[adj] = True
      return client_wants_continue and not me.emptyQ()
       

## Basic Test, We will make shortest path matrices
if __name__=='__main__':

  from TestGraphs import mkTestGraph6

  gph = mkTestGraph6()

  correct = [ 
# source a
   [  [0, 0, 0, 0, 0, 0],
      [0, 1, 0, 1, 0, 0],     # distance 1
      [0, 0, 2, 0, 0, 0],
      [0, 0, 0, 0, 2, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0]  ],
# source b  
   [  [0, 0, 0, 0, 0, 0],
      [1, 0, 1, 1, 0, 0],     # distance 1
      [0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0]  ],
# source c
   [  [0, 0, 0, 0, 0, 0],
      [0, 1, 0, 1, 1, 0],     # distance 1
      [2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0]  ],
# source d
   [  [0, 0, 0, 0, 0, 0],
      [1, 1, 1, 0, 0, 0],     # distance 1
      [0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0]  ],
# source e
   [  [0, 0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0, 0],     # distance 1
      [0, 1, 0, 1, 0, 0],
      [2, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0]  ],
# source f
   [  [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],     # distance 1
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0]  ]
  ]   

  def printDistances(source):  ## uncomment below to use
     print 'distances from ' + gph.toDeclared(source)  
     for dest in gph.iNodes:
        print '  distance ' + str(dest)+ ': ' + \
              str( numshortestpaths[source][dest] )
 
  numshortestpaths = \
    [ [ [0 for node in gph.iNodes]  
               for node in gph.iNodes ]
                   for node in gph.iNodes ]

  process_count = 0
  processing = None

  def processOut( source, node, dist, adj_node ): 
      numshortestpaths[source][dist+1][adj_node] \
            +=  numshortestpaths[source][dist][node]
      return True
 
  def process( x,y ): 
     global process_count
     #print 'processing ' + gph.toDeclared(x) + ' at ' + str(y)
     process_count += 1 
     return True
  
  def processSame( x,y,z): 
     global processing
     gd = lambda z: gph.toDeclared(z)
     #print 'chord-like: ' + gd(x) +',' + gd(y)
     if processing in ['a','c','e']:
        assert (gd(x)=='b' and gd(z)=='d') or \
               (gd(z)=='b' and gd(x)=='d') 
     else:
        assert gd(x)=='b' or gd(y)=='b'
     return True


  for source in gph.iNodes:
     processing = gph.toDeclared(source)
     for a in gph.adjIter(source):
        numshortestpaths[source][1][a] = 1

     #print '+++++++++++++++++++++++++'
     BreadthFirstSearch( 
          gph, 
          source, 
          process,
          processSame,
          lambda n,d,a: processOut(source,n,d,a) 
     )
   
  for s in gph.iNodes:
     #printDistances(s)
     for d in gph.iNodes:
        assert numshortestpaths[s][d]==correct[s][d], \
               ' problem with ' + gph.toDeclared(s) + \
               ' at distance ' + str(d) 

  assert process_count==26
  ## that's nodes a-e five times each and node f once

  print "Basic BreadthFirstSearch Test Passed"          
