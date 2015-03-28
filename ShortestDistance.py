import array

def _extract(ary,frm,upTo):
   sary = []
   for i in range(frm,upTo): sary.append(str(ary[i]))
   return ','.join(sary)

class ColorParams:
   '''  ColorParams is used to store structural information
        about colorings found from a breadth first search
        on every node.

        A coloring is a partition of the nodes such that
        if an automorphism exists from node x to node y
        then x and y have the same color.

        Two kinds of params are stored for each distance
        d from a node source:
           1) for each color numbers of nodes of that color
           2) for each color, number of shortest paths 
              ending at that color
       
        The parameters are placed in a 'box' and  organized 
        by node in two different ways:  by original node 
        number used in the graph and by sorted node number.  
        
        Sorting normalizes the params so they can be compared
        between graphs.
   '''

   def __init__(me,
      n,        ## the number of nodes we are working with
      gph_order ## gph_order(x) is the index of a node
                ## in the underlying graph
                ## gph_order defaults to an identity array
   ):
      me.n = n
      me.gph_order = gph_order if gph_order else range(n)
      me.box = \
         [ ( array.array('H',[0]*(n*2*n)), 
             gph_order[x]        ) for x in range(me.n) ]
         ## me.box[i][0] gives color counts
         ##    for which==0, counting color occurrences
         ## me.box[i][1] is index of node in original 
         ## graph
         ##
         ## dist*(2*me.n+) + which*n + count indexes
         ## into the params me.box[i][0]
      me.paths = None               ## see resetPathCount
   
   def gphIdx(me,node):  
       ''' returns original graph index of sorted node '''
       return me.box[node][1]

   def sortedBox(me,node):
      return me.box[node][0]
   
   def incrColorCount(me,source,dist,clr):
      ## for keeping track of number of nodes with
      ## given color dist away from source
      me.box[source][0][dist*2*me.n + clr] += 1

   def colorCounts(me,source,dist):
      return _extract( 
               me.box[source][0], 
               dist*2*me.n, 
               (dist*2+1)*me.n
             )
   
   def resetPathCount(me):
      me.paths = [ array.array('H',[0]*(me.n*me.n)) 
                         for x in range(me.n) ]
         ## me.paths[dist*me.n + node indexes] will give
         ## number of shortest paths from source to node
 
   def incrPathCount(me,source,dist,adj_node,incr):
      ## for keeping track of number of shortest paths 
      ## from source to adj_node
      me.paths[source][dist*me.n + adj_node] += incr 

   def pathCount(me,source,dist,end_node):
      ## provides counts for incrPathCount
      ##
      ## incrPathCount's adj_node should be adjacent
      ## to end_node
      return me.paths[source][dist*me.n + end_node] 

   def pathCounts(me,source,dist):
      n1 = dist*me.n
      return _extract( 
               me.paths[source], 
               n1,
               n1+me.n 
             )

   def incrToColorCount(me,source,dist,clr,incr):
      ## for keeping track of number of shortest paths 
      ## from source of length dist to color clr
      me.box[source][0][(dist*2+1)*me.n + clr] += incr 

   def toColorCounts(me,source,dist):
      n2 = (dist*2+1)*me.n
      return _extract( 
               me.box[source][0], 
               n2,
               n2+me.n 
             )
 
   def sort(me):
      me.box.sort( key=lambda x: x[0] ) 
   

## Basic Test
if __name__ == "__main__":

   def printColorParams(title,colorParams):
      print "\n" + title
      gphn = colorParams.n
      for n in range(gphn):
         print 'node ' + str(n) + ':'
         for d in range(gphn):
            print '  dist ' + str(d) +': '
            print '    color count: ' + \
                  colorParams.colorCounts(n,d)
            print '    path count: ' + \
                  colorParams.pathCounts(n,d)
            print '    path to color count: ' + \
                  colorParams.toColorCounts(n,d)
      print


   c = ColorParams(2,range(2))

   c.incrColorCount(0,0,0)
   c.incrColorCount(0,0,0)
   c.incrColorCount(0,1,0)
   c.incrColorCount(0,1,1)
   c.incrColorCount(1,1,0)

   c.incrPathCount(0,1,1,2)
   c.incrPathCount(1,1,1,2)
   
   c.incrToColorCount(0,0,0,3)
   c.incrToColorCount(1,1,1,2)
   c.incrToColorCount(1,1,1,5)
    
   printColorParams('original',c)

   c.sort()
   printColorParams('sorted',c)

   assert c.sortedBox(0)==array.array('H',[0,0,0,0,1,0,0,7])
   assert c.sortedBox(1)==array.array('H',[2,0,3,0,1,1,0,0])
   assert c.gphIdx(0)==1
   assert c.gphIdx(1)==0
   
   print 'Basic ColorParams Test Passed'


