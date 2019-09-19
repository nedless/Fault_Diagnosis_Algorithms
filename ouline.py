import networkx as nx
def generate_incmatrix_from_automate(G):
    n = [i for i in G.nodes()]
    n.sort()

    inc_m = nx.adjacency_matrix(G,n).todense().tolist()
    print(inc_m)
    events_ref = nx.get_edge_attributes(G, 'label')

    for i in [n for n in events_ref.keys()]:        
        inc_m[int(i[0])-1][int(i[1])-1] = events_ref[i]

def get_adjacencies(G, node):

    G_neigh = list(G.neighbors(node))
    mapping = nx.get_edge_attributes(G, 'label')

    adj = {}
    for n in G_neigh:
        adj[n] = mapping[(node,n)]
    return adj



