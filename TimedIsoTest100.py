import timeit,gc



print "Timed testing of isomorphic random graphs with 100 nodes"

setup = \
""" 
from TestGraphs import MakeRandom 
from GraphIsomorphism import checkIsomorphic

maker = MakeRandom(100)

(gph1,gph2) = maker.getIsoPair()
   
def isoAction(perm):
    assert gph1.iso(gph2,perm), \
           'Final Iso check failed with ISO 100 Test'

def noIsoAction():
    raise Exception('Iso 100 Node Test determined not isomorphic!')

def failAction():
    raise Exception('Failure with Iso 100 Node Test')
"""

run = \
"""
gc.enable()

checkIsomorphic( 
   gph1, gph2, isoAction, noIsoAction, failAction
)
"""

print 'These are average number of seconds from 20 tests'
print ','.join( [ str(t/20) 
                  for t in timeit.repeat(
                            run,setup,repeat=20,number=20)
              ] )


