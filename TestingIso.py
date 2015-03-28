import TestGraphs 
from GraphIsomorphism import checkIsomorphic

print "Testing graph with 10 nodes"

maker = TestGraphs.MakeRandom(10)
(gph1,gph2) = maker.getIsoPair()

   
def isoAction(perm):
    assert gph1.iso(gph2,perm), \
           'Failure iso test10'

def noIsoAction():
    raise Exception('Failure with test10 ')

def failAction():
    raise Exception('Failure with test10')

checkIsomorphic( 
   gph1, gph2, isoAction, noIsoAction, failAction
)

maker = TestGraphs.MakeRandom(10)
(gph1,gph2) = maker.getNonIsoPair()

def isoAction(perm):
    raise Exception('Failure with non iso test10')

def noIsoAction():
    pass    # the result we expect

def failAction():
    raise Exception('Failure with non iso test10')


checkIsomorphic( 
   gph1, gph2, isoAction, noIsoAction, failAction
)

print "Testing graph with 100 nodes"

maker = TestGraphs.MakeRandom(100)
(gph1,gph2) = maker.getIsoPair()

   
def isoAction(perm):
    assert gph1.iso(gph2,perm), \
           'Failure iso test100'

def noIsoAction():
    raise Exception('Failure with test100 ')

def failAction():
    raise Exception('Failure with test100')

checkIsomorphic( 
   gph1, gph2, isoAction, noIsoAction, failAction
)

maker = TestGraphs.MakeRandom(100)
(gph1,gph2) = maker.getNonIsoPair()

def isoAction(perm):
    raise Exception('Failure with non iso test100')

def noIsoAction():
    pass    # the result we expect

def failAction():
    raise Exception('Failure with non iso test100')


checkIsomorphic( 
   gph1, gph2, isoAction, noIsoAction, failAction
)

print "Testing graph with 500 nodes"

maker = TestGraphs.MakeRandom(500)
(gph1,gph2) = maker.getIsoPair()

   
def isoAction(perm):
    assert gph1.iso(gph2,perm), \
           'Failure iso test500'

def noIsoAction():
    raise Exception('Failure with test500 ')

def failAction():
    raise Exception('Failure with test500')

checkIsomorphic( 
   gph1, gph2, isoAction, noIsoAction, failAction
)

maker = TestGraphs.MakeRandom(500)
(gph1,gph2) = maker.getNonIsoPair()

def isoAction(perm):
    raise Exception('Failure with non iso test500')

def noIsoAction():
    pass    # the result we expect

def failAction():
    raise Exception('Failure with non iso test500')


checkIsomorphic( 
   gph1, gph2, isoAction, noIsoAction, failAction
)

print 'Testing Graphs of size 10, 500, and 500 passed'

