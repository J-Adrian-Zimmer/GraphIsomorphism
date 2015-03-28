import timeit,gc

# Warning: there are 20 separate isomorphism checks at a bit over 
# 30 minutes each

print "Timed testing of isomorphic random graphs with 800 nodes"

setup = \
""" 
from TestGraphs import MakeRandom
from GraphIsomorphism import checkIsomorphic

maker = MakeRandom(800)
(gph1,gph2) = maker.getIsoPair()
   
def isoAction(perm):
    print "found isomorphism, checking correctness"
    assert gph1.iso(gph2,perm), \
           'Final Iso check failed with ISO 800 Test'

def noIsoAction():
    raise Exception('Iso 800 Node Test determined not isomorphic!')

def failAction():
    raise Exception('Failure with Iso 800 Node Test')
"""

run = \
"""
gc.enable()

checkIsomorphic( 
   gph1, gph2, isoAction, noIsoAction, failAction
)
"""

print 'These are average number of seconds from 2 tests'
print ','.join( [ str(t/2) 
                  for t in timeit.repeat(
                            run,setup,repeat=5,number=2)
              ] )


print "Timed testing of non isomorphic random graphs with 800 nodes"

setup = \
""" 
from TestGraphs import MakeRandom
from GraphIsomorphism import checkIsomorphic

maker = MakeRandom(800)
(gph1,gph2) = maker.getNonIsoPair()
   
def isoAction(perm):
    raise Exception('NonIson 800 test reported ISO!')

def noIsoAction():
    print "found nonisomorphic pair"

def failAction():
    raise Exception('NonIso 800 test failed!')
gc.collect()
"""

run = \
"""
gc.enable()

checkIsomorphic( 
   gph1, gph2, isoAction, noIsoAction, failAction
)
"""

print ','.join( [ str(t/2) 
                  for t in timeit.repeat(
                            run,setup,repeat=5,number=2)
              ] )
print 'These are average number of seconds from 2 tests'

