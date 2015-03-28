from Graph import Graph

class Coloring:
   ''' Coloring keeps track of the coloring of a graph (as in
       Graph.py).  The coloring is simply a range(ncolors)
       of numbers.  What is special about this class
       is that supports refinements of automorphic colorings.

       With this class you can get a list of all the nodes
       colored with a specified color and tentatively recolor
       a node with a new color.
   ''' 
   def _setColor(me, node,clr):
       me.colors[node] = clr

   def __init__(me,gph,colors=None,numColors=None):
       me.gph = gph
       # me.colors maps each node to its color
       # 
       if colors:
          me.setColors(colors,numColors)
       else:
          me.colors = [ 0 for x in range(gph.size) ]
          me.ncolors = 1
       ## singleton colors are arbitrarily assigned and 
       ## may be revoked
       me.singleton = None           # is none when there is no
                                     # tentative singleton color
                                     # otherwise this is the node
                                     # given the singleton color
                                     # (which will be the highest
                                     # color number available)
       me.singleton_old_color = None # if singleton coloration is
                                     # revoked, this is the color
                                     # the node returns to

   def setColors(me,colors,numColors=None):
      me.colors = colors
      if numColors:
         me.numColors = numColors
      else:
         me.numColors = max(me.colors)+1 

   def getColor(me,node):
       return me.colors[node]

   def getFirstMultiNodeColor(me):
      i = 0
      while i<me.ncolors and len(me.nodes[i])==1:
         i += 1
      return -1 if i==me.ncolors else i

   def affirmTentative(me):
      me.singleton = None

   def setTentativeSingleton(me,node):
      if  me.singleton:  
         me.ncolors-=1
         me.colors[node] = me.singleton_old_color
      me.singleton = node
      me.singleton_old_color = me.colors[node]
      me.colors[node] = me.ncolors
      me.ncolors += 1
  
   def __eq__(me, other):
        if isinstance(other, me.__class__):
            return me.ncolors==other.ncolors and \
                   me.colors==other.colors
        else:
            return False

   def __ne__(me, other):
        return not me.__eq__(other)

   def getColors2Nodes(me):
      ## for use when me.numColors==gph.size
      ## that is, when an isomorphism has been found
      cc = sorted(
              zip(range(me.gph.size),me.colors),
              key= lambda p: p[1]
           )             
      return [ p[0] for p in cc]
          
# Basic Coloring Test

if __name__=='__main__':
   from TestGraphs import mkTestGraph4
   gph = mkTestGraph4()
   c = Coloring(gph)
   c.setTentativeSingleton(3)
   c.affirmTentative()
   c.setTentativeSingleton(0)
   c.affirmTentative()
   c.setTentativeSingleton(2)
   assert c.colors == [2,0,3,1]
   assert c.getColors2Nodes() == [1,3,0,2] 

   print "Basic Coloring Test Passed"
