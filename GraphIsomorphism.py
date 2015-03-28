## GraphIsomorphism.py

from ColorRefine import ColorRefine
from TwoColorRefiner import TwoColorRefiner
     ## isoAction, noIsoAction, failAction, and 
     ## selectiveCheckIsDefinitive will be added to
     ## our TwoColorRefiner object
  
def checkIsomorphic(
   gph1,       # as in Graph.py
   gph2,       # as in Graph.py
   isoAction,  # is passed a list that isomorpically 
               # maps gph1.iNodes to gph2.iNodes 
   noIsoAction,
   failAction  # is passed automorphic colorings for
               # gph1 and gph2 so you can create your
               # own algorithmic extension to this and
               # base it on the best automorphic
               # colorings this algo could produce
):
   rfinr = TwoColorRefiner(gph1,gph2)
   rfinr.isoAction = isoAction
   rfinr.noIsoAction = noIsoAction
   rfinr.failAction = failAction
   rfinr.selectiveCheckIsDefinitive = True
        # see _selectiveCheck
   rfinr.setColors( 1, ColorRefine(gph1) )
   rfinr.setColors( 2, ColorRefine(gph2) )
   action = lambda: _definitiveCheck(rfinr)
   while action: action = action()
      # within O(gph.size**3) steps action will be
      # isoAction, noIsoAction, or failAction
      # these actions are expected to return None

def _refineAndReport(
        rfinr,
        repeatAction,
        unequalAction,
        failureAction
):
   if not rfinr.refine():     
      return failureAction
   elif rfinr.cr1<>rfinr.cr2:
      return unequalAction
   else:
      lbl = rfinr.isoLabelling()
      if lbl:
         return lambda: rfinr.isoAction(lbl)
      else:
         return repeatAction

def _definitiveCheck(rfinr):
   ''' _definitiveCheck refines automorphic colorings,
       that is colorings such that the existence of an
       automorphism mapping node x to node y means x and
       y have the same color

       the checks lead to a demonstration that two graphs 
       are or are not isomorphic==IF THAT ISN'T POSSIBLE
       _
   '''
   if rfinr.gph1.size!=rfinr.gph2.size:
      return rfinr.noIsoAction
   rfinr.setColors( 
          1, 
          ColorRefine( 
              rfinr.gph1,
              rfinr.cr1.colors,
              rfinr.cr1.ncolors
          ) )
   rfinr.setColors( 
          2, 
          ColorRefine( 
              rfinr.gph2,
              rfinr.cr2.colors,
              rfinr.cr2.ncolors
          ) )
   _continueDefinitiveCheck(rfinr)
   
def _continueDefinitiveCheck(rfinr):
   return _refineAndReport( 
         rfinr, 
         lambda: _continueDefinitiveCheck(rfinr) ,
         rfinr.noIsoAction,
         lambda: _selectiveCheck(rfinr)
   )

def _selectiveCheck(rfinr):
   ''' _selectiveCheck takes up where _definitiveCheck 
       leaves off
       
       _selectiveCheck works with colorings that 
       are intended to be automorphic but may not be  --
       this is due to the fact that we have somewhat
       arbitrarily assigned singleton colors

       a selective check can show two graphs are 
       isomorphic or it can report failure; only in one 
       case can it show two graphs are not isomorphic
   '''
   clrs1 = rfinr.colors(1)
   clrs1.affirmTentative()
   clrs2 = rfinr.colors(2)
   clrs2.affirmTentative()
   clr = clsr1.getFirstMultiNodeColor()
   assert clr>=0, \
          'Found potential iso in wrong place'
   nodes1 = clsr1.getNodes()
   nodes2 = clsr2.getNodes()
   assert len(nodes1)==len(nodes2) and \
          len(nodes1)>0, \
          'Found potential non iso in wrong place'
   clsr1.setTentativeColor(nodes1[0])
   rfinr.singleColorActParams = (clsr2,nodes2,0)
   _continueSelectiveCheck(rfinr,actParams),

def _continueSelectiveCheck(rfinr,actParams):
   i = rfinr.singleColorActParams[2]
   i_finished = i==len(nodes2)
   coloring_finished = rfinr.colors(1).color_size==rfinr.gph1.size
   if i_finished and coloring_finished: 
      return rfinr.failAction
   elif i_finished:     ## assign a new rfinr.gph1 singleton color
      if rfinr.selectiveCheckIsDefinitive:
         rfinr.selectiveCheckIsDefinitive = False
         # the first time we assign a single color to 
         # gph1 and check possible single color 
         # assignments in gph2 we can be sure no 
         # matching colors means not isomorphic  
         # after that we would have to back up and 
         # try again;  since we don't backup and try 
         # again a subsequent failure is a real failure 
         # of the algorithm
      noIsoAct = rfinr.noIsoAction \
               if rfinr.selectiveCheckIsDefinitive \
               else rfinr.failAction
      return _refineAndReport(
                 rfinr, 
                 lambda: _selectiveCheck(rfinr),
                 noIsoAct, 
                 rfinr.failAction
             )
   else:        ## try another gph2 node with this color
      clsr2.setTentativeColor(nodes2[i])
      rfinr.singleColorActParams[2] = i+1
      again =  lambda: _continueSelectiveCheck( rfinr )
      return _refineAndReport(
         rfinr,
         again,
         again,
         rfinr.failAction
      )


## Basic Test

if __name__=='__main__':
  
   ## test isomorphism of Petersen Graph ##
   
   from TestGraphs import mkPetersenGraph

   gph1 = mkPetersenGraph()
   gph2 = gph1.relabelledClone()


   def isoAction(perm):
       assert gph1.iso(gph2,perm), \
              'Failure 1 with Petersen Graph'

   def noIsoAction():
       raise Exception('Failure 2 with Petersen Graph')

   def failAction():
       raise Exception('Failure 3 with Petersen Graph')


   checkIsomorphic( 
      gph1, gph2, isoAction, noIsoAction, failAction
   )

   ## test nonismorphism of 6 and 6b ##
   
   from TestGraphs import mkTestGraph6, mkTestGraph6b

   gph1 = mkTestGraph6()
   gph2 = mkTestGraph6b().relabelledClone()


   def isoAction(perm):
       raise Exception('Failure 1 with Graphs 6 & 6b')

   def noIsoAction():
       pass    # the result we expect

   def failAction():
       raise Exception('Failure 3 with Graphs 6 & 6b')


   checkIsomorphic( 
      gph1, gph2, isoAction, noIsoAction, failAction
   )

   print "Graph Isomorphism Test Passed"

