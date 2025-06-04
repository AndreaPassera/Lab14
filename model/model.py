import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self.grafo=nx.DiGraph()
        self.idMap={}

    def getStore(self):
        return DAO.getStore()


    def buildGraph(self, store, maxG):
        nodes=DAO.getNodes(store)
        for n in nodes:
            self.idMap[n.order_id]=n
        self.grafo.add_nodes_from(nodes)

        trovati=DAO.getEdges(store,maxG)
        for e in trovati:
            n1=self.idMap[e[0]]
            n2=self.idMap[e[1]]
            self.grafo.add_edge(n1,n2,weight=e[2])


    def getGraphDetails(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def getCamminoMax(self,source):

        cammino=list(nx.bfs_tree(self.grafo,self.idMap[source]))
        cammino.remove(self.idMap[source])
        return cammino
