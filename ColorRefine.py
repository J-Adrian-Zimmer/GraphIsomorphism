from Graph import Graph
from Coloring import Coloring
from ColorParams import ColorParams, PathParams
from BreadthFirstSearch import BreadthFirstSearch

class ColorRefine(Coloring):
   ''' Objects of this class are capable of refining
       automorphic colorings, as stored in the base
       class.
      
      An automorphic coloring is a partition of a 
      graph's nodes such that if an automorphism can 
      map a node x to a node y then x and y have the 
      same color.

      A refinement of a coloring is a subpartition.  The
      refine() method of this class returns (u,v) where
      v is a refinement and u and its size.  If the size 
      has not changed, there is no point in re-executing 
      refine().

      Letting n be the number of nodes: refine() will run
      n breadth first searches.  Because of ColorParams the
      memory requirements will be of order n**3.
   '''
   def __init__( 
          me,
          gph,           ## a graph as in Graph.py
          coloring = None,
                     ## default [0]*gph.size
                     ## coloring(n) is color of node n
          ncolors = None 
   ): 
      Coloring.__init__(me,gph,coloring,ncolors)
      me.gph = gph
      me.params = ColorParams(
                     me.gph.size,
                     range(me.gph.size)
                  )
      me.paths = None                        ## see refine
   
   def refine(me):
      ## set up param structure for this coloring
      for s in me.gph.iNodes:
         me.paths = PathParams(me.gph.size)
         for a in me.gph.adjIter(s):
            # every node adj to s is one shortest path
            # of length 1 from s
            me.paths.incrPathCount(1,a,1)

         BreadthFirstSearch(
            me.gph, 
            s, 
            lambda n,d: me.countColors(s,n,d),
            lambda n,d,a: True, 
            lambda n,d,a: me.countPaths(s,n,d,a) 
         )
         #printPathCounts(me.gph,s,me.paths)

      ## recolor 
      me.params.sort()
      i = 1
      me.ncolors = 0
      prv = me.params.sortedBox(0)
      while( i<me.gph.size ): 
         if me.params.sortedBox(i)!=prv: me.ncolors+=1
         prv = me.params.sortedBox(i)
         me.colors[me.params.gphIdx(i)] = me.ncolors
         i+=1
      me.ncolors+=1

   def countColors( me, source, node, dist ):
      me.params.incrColorCount(          ## counting colors
               source,                     ## at level dist
               dist,
               me.colors[node]
            )
      me.params.incrToColorCount(     ## counting colors of
               source,            ## end points of shortest
               dist,                ## paths ending at node
               me.colors[node],
               me.paths.pathCount(    ## this count was
                      dist,         ## with adjacencies
                      node
               )
            )
      return True

   def countPaths( me, source, node, dist, adj_node ):
      ## counts of paths of dist 1 initialized at outset
      ## now we fix the next dist out 
      me.paths.incrPathCount( ## counting shortest paths 
                 dist + 1,
                 adj_node,   
                 me.paths.pathCount(     ## this node's
                        dist,
                        node
                 )
              )
      return True

# Basic Test
if __name__=='__main__':

  from TestGraphs import mkTestGraph6

  def printColorParams(gph,title,colorParams):
      print "\n" + title
      for n in range(gph.size):
         print 'node ' + gph.toDeclared(colorParams.gphIdx(n)) + ':'
         for d in range(gph.size):
            print '  dist ' + str(d) +': '
            print '    color count: ' + \
                  colorParams.colorCounts(n,d)
            print '    path to color count: ' + \
                  colorParams.toColorCounts(n,d)
      print
  
  def printPathCounts(gph,source,pathParams):
      print "\nDistance Counts for "+gph.toDeclared(source)
      for d in range(gph.size):
         print '  dist ' + str(d) +': '
         print '    path counts: ' + \
               pathParams.pathCounts(d)
      print

  gph = mkTestGraph6()

  cr = ColorRefine(gph)
  cr.refine()
   
    
  #printColorParams(gph,'refinement based on', cr.params)

  assert cr.ncolors == 5
  assert cr.colors == [2,3,4,3,1,0]
  print "Basic ColorRefine Test Passed"


