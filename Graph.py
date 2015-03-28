import array

def _push(ary,x):
   if x not in ary: ary.append(x)


class _AdjIter:

   def __init__(me,myOuter,x):
      me.i = -1
      me.links = myOuter.links[x]

   def __iter__(me):
      return me
          
   def next(me):
      me.i+=1
      if me.i>=len(me.links):
         raise StopIteration()
      else:
         return me.links[me.i]

class Graph:
   ''' Simple undirected graph with n nodes 
       
       Create with Graph(n,edge_list). Edges in this list 
       are pairs (but of course are seen as unordered).

       Nodes are treated as integers but may be entered
         as a list of values

       There are two methods

          toDeclared(x) -> original form of node x
          fromDeclared(x) -> integer form used herein

       And a set of iterators that iterate through
       a node's adjacencies

   '''
   
   def __init__(me,
          n,        ## number of nodes or list of nodes
          edges               ## list of pairs of nodes
            ## unnecessary to list both (x,y) and (y,x)
   ):
      if isinstance(n,int):
         me.size = n 
         me.nodes = me.iNodes = range(n) 
         me.links = [ [] for i in range(me.size) ]
                   ## [[]]*me.size copies the same empty array
         for (x,y) in edges:
            _push(me.links[x],y)
            _push(me.links[y],x)
      else:
         me.size = len(n)
         me.nodes = n
         me.iNodes = range( me.size )
         me.links = [ [] for i in range(me.size) ]
         for (x,y) in edges:
            ix = me.fromDeclared(x)
            iy = me.fromDeclared(y)
            _push(me.links[ix],iy)
            _push(me.links[iy],ix)
      
   def fromDeclared(me,x):
      try:
         return me.nodes.index(x)
      except:
         return None

   def toDeclared(me,i): return me.nodes[i]
   
   def adjIter(me,x):
      return _AdjIter(me,x)

   def relabelledClone(me,test=False):
       ## due to the size of the random seed, this
       ## will not produce random relabellings if 
       ## gph.size is much more than 2000
       import random
       random.seed( random.SystemRandom().random() )
       perm = range(me.size)
       random.shuffle(perm)
       gph2 = Graph( [ me.nodes[n] for n in perm], [] )
       for n in me.iNodes:
          gph2.links[perm[n]] = [ perm[v] for v in me.links[n] ]
       if test: assert me.iso(gph2,perm), \
                'test of relabelledClone failed'
       return gph2


   def iso(me,gph2,perm):
       if not isinstance(gph2,me.__class__):
          raise TypeError('Graph type expected')
       if me.size<>gph2.size:  return False
       for i in range(me.size):
          if me.links[i].sort() <> \
             [ perm[j] for j in gph2.links[perm[i]] ].sort():
            return False 
       return True
   
## Basic Test


def printGraph(gph,name):
       print name
       print ','.join(
              [ '('+str(x)+','+str(y)+')' \
                 for x,y in zip(gph.nodes,gph.iNodes) ]
             )
       for i in gph.nodes:
          j = gph.fromDeclared(i)
          print str(i) +':  ' + ','.join( 
                             [ str(gph.toDeclared(x)) \
                               for x in gph.links[j]  ]
                           )
   
def testIterator(gph,node):
   adjs = []   
   for n in gph.adjIter(node): adjs.append(n)
   assert sorted(adjs) == [1,2,3]
 
if __name__ == '__main__':
   from TestGraphs import mkTestGraph4,mkTestGraph4b
    
   gph = mkTestGraph4()
   assert gph.iso(mkTestGraph4b(),[0,2,1,3]), \
                        'test of iso() failed'
   gph.relabelledClone(True)

   assert gph.toDeclared(1)=='b'
   assert gph.fromDeclared('c')==2
   testIterator(gph,0)

   print 'Basic Graph Test Passed'

