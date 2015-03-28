import Graph,TestGraphs

maker = TestGraphs.MakeRandom(6)

(g1,g2) = maker.getNonIsoPair()

Graph.printGraph(g1,'first')

Graph.printGraph(g2,'second')
