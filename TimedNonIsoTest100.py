import timeit,gc

print "Timed testing of non isomorphic random graphs with 100 nodes"

setup = \
""" 
from TestGraphs import MakeRandom
from GraphIsomorphism import checkIsomorphic

maker = MakeRandom(100)
(gph1,gph2) = maker.getNonIsoPair()
   
def isoAction(perm):
    raise Exception('NonIson 100 test reported ISO!')

def noIsoAction():
    pass

def failAction():
    raise Exception('NonIso 100 test failed!')
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


