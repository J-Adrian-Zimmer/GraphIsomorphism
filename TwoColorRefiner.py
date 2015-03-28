from ColorRefine import ColorRefine

class TwoColorRefiner:

   def __init__(me,graph1,graph2):
      me.gph1 = graph1
      me.cr1 = ColorRefine(graph1)
      me.gph2 = graph2
      me.cr2 = ColorRefine(graph2)

   def coloring(me,gphnum):
      return me.cr1 if gphnum==1 else me.cr2
  
   def setColors(me,gphnum,coloring):
      if gphnum==1: me.cr1.setColors(coloring.colors)
      else:         me.cr2.setColors(coloring.colors) 
   
   def refine(me):
      cn1 = me.cr1.ncolors
      cn2 = me.cr2.ncolors
      me.cr1.refine()
      me.cr2.refine()
      return cn1 < me.cr1.ncolors or \
             cn2 < me.cr2.ncolors

   def isoLabelling(me):
     if me.cr1.ncolors<>me.gph1.size  or  cr1<>cr2:
       return None       ##  returning None if no iso yet
     ## when color size is graph size there will exactly
     ## one color for each node
     fromColor = cr2.getColors2Nodes()
     return [ fromColor[cr1.getColor(i)] \
              for i in me.gph1.iNodes ] 

   def unequalColorRefines(me):
      return cr1<>cr2 


