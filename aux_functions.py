from des import *

def load_input():
        with open('input.txt', 'r') as myfile:
            input = myfile.read()
        with open('marked_states.txt', 'r') as myfile:
            marked = myfile.read()
        return parse2des(input, marked)

def parse2des(input, marked):
    #Parsing incidence matrix
    gg = input.split("\n\n-\n\n")
    des_list = []

    for g in gg:        
        inc = []
        inc = g.split("\n")
        inc_matrix = []
        for line in inc:
            if line.find(':')>0:
                label = line[:line.find(':')-1]
                settings = create_settings_list(line[line.find(':')+1:])
                continue
            inc_matrix.append(line.strip().split(";"))
        G = des(inc_matrix, settings[0], label, settings[1])
        des_list.append(G)
    return des_list

def create_settings_list(states):
    ref = []
    marked = []
    for s in states[1:-1].split(","):
        if s.find('*')>-1:            
            marked.append(s[:-1])
            ref.append(s[:-1])
        else:
            ref.append(s)
    return [ref[:], marked[:]]
def get_marked(marked):
    mm = marked.split("\n")
    m_dict = {}
    for m in mm:
        label = m[:m.find(":")]
        mar = [s for s in m[m.find(":")+1:].split(",")]
        m_dict[label] = mar
    return m_dict

def generate_incmatrix_from_automate(G):
    n = [i for i in G.nodes()]
    n.sort()

    inc_m = nx.adjacency_matrix(G,n).todense().tolist()
    print(inc_m)
    events_ref = nx.get_edge_attributes(G, 'label')

    for i in [n for n in events_ref.keys()]:        
        inc_m[n.index(i[0])][n.index(i[1])] = events_ref[i]
     
    return [n, inc_m]

def get_adjacencies(G, node):
    
    G_neigh = list(G.neighbors(node))
    mapping = nx.get_edge_attributes(G, 'label')

    adj = {}
    for n in G_neigh:
        adj[n] = mapping[(node,n)]
    return adj

def get_adjacencies_events(G, node):    
    G_neigh = list(G.neighbors(node))
    mapping = nx.get_edge_attributes(G, 'label')

    adj = {}
    for n in G_neigh:
        adj[n] = mapping[(node,n)]
    return list(adj.values())

def iterat(G_prod, G1, G2, actual_node):
        ev_G1 = f.get_adjacencies_events(G1, actual_node[0])
        ev_G2 = f.get_adjacencies_events(G2, actual_node[1])
        ev_common = [value for value in ev_G1 if value in ev_G2]

        if len(ev_common) == 0:
            return G_prod

        G1_map = f.get_adjacencies(G1, actual_node[0])
        G2_map = f.get_adjacencies(G2, actual_node[1])
        G1_map = {v: k for k, v in G1_map.items()}
        G2_map = {v: k for k, v in G2_map.items()}

        for ev in ev_common:
            next_node = [G1_map[ev], G2_map[ev]]
            try:
                G_prod.add_edge(str(actual_node),str(next_node), label = ev)
            except TypeError:
                label = nx.get_edge_attributes(G_prod, 'label')[(str(actual_node),str(next_node))]
                G_prod.remove_edge(str(actual_node),str(next_node))
                G_prod.add_edge(str(actual_node),str(next_node), label = label+','+ev)

            if actual_node == next_node:
                continue
            G_prod = iterat(G_prod,G1, G2, next_node)
        
        return G_prod