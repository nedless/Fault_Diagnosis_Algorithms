from des import *
from itertools import product

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
                label = line[:line.find(':')]
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

def generate_incmatrix_from_automate(G_prod, P1, P2):
    n = [i for i in G_prod.nodes()]
    n.sort()

    M1 = P1.get_marked()
    M2 = P2.get_marked()

    output = list(product(M1, M2))
    output = [str(list(n)) for n in output]
    node_list = list(G_prod.nodes())
    marked = []
    for node in output:
        if node in node_list:
            marked.append(node)

    inc_m = nx.adjacency_matrix(G_prod,n).todense().tolist()
    print(inc_m)
    events_ref = nx.get_edge_attributes(G_prod, 'label')

    for i in [n for n in events_ref.keys()]:        
        inc_m[n.index(i[0])][n.index(i[1])] = events_ref[i]
     
    new_m = []
    for i in range(len(inc_m)):
        new_m.append(['0' if x==0 else x for x in inc_m[i]])

    return [new_m, n, marked]

def generate_incmatrix_for_obs_automate(Obs):
    n = [i for i in Obs.nodes()]
    n.sort()
    

    inc_m = nx.adjacency_matrix(Obs,n).todense().tolist()
    print(inc_m)
    events_ref = nx.get_edge_attributes(Obs, 'label')

    for i in [n for n in events_ref.keys()]:        
        inc_m[n.index(i[0])][n.index(i[1])] = events_ref[i]
    
    new_m = []
    for i in range(len(inc_m)):
        new_m.append(['0' if x==0 else x for x in inc_m[i]])
    return [new_m, n]


def get_sigma(automate):        
        events = nx.get_edge_attributes(automate, 'label')

        sigma = ""
        for e in events.values():
            sigma += e + ","
        sigma = sigma[:-1]
        sigma = list(dict.fromkeys(sigma.split(","))) #removing duplicates
        sigma.sort()
        return sigma
def get_adjacencies(G, node):
    
    G_neigh = list(G.neighbors(node))
    mapping = nx.get_edge_attributes(G, 'label')

    adj = {}
    l =[]
    for n in G_neigh:
        l.append(n)
    x = []
    for i in l:
        x = list(set(x[:]).union(set(i.split(","))))
    for n in x: 
        if mapping[(node,n)].find(',')>-1:
            for k in mapping[(node,n)].split(','):
                adj[k] = n    
        else:   
            adj[mapping[(node,n)]] = n
    return adj

def get_adjacencies_events(G, node):    
    G_neigh = list(G.neighbors(node))
    mapping = nx.get_edge_attributes(G, 'label')

    adj = {}
    for n in G_neigh:
        adj[n] = mapping[(node,n)]
    
    x = []
    for i in list(adj.values()):
        x = list(set(x[:]).union(set(i.split(","))))

    return x

def iterat(G_prod, G1, G2, actual_node):
    ev_G1 = f.get_adjacencies_events(G1, actual_node[0])
    ev_G2 = f.get_adjacencies_events(G2, actual_node[1])
    ev_common = [value for value in ev_G1 if value in ev_G2]

    if len(ev_common) == 0:
        return G_prod

    G1_map = f.get_adjacencies(G1, actual_node[0])
    G2_map = f.get_adjacencies(G2, actual_node[1])    

    for ev in ev_common:
        next_node = [G1_map[ev], G2_map[ev]]
        if not (str(actual_node),str(next_node)) in list(G_prod.edges()):
            G_prod.add_edge(str(actual_node),str(next_node), label = ev)
        else:
            label = nx.get_edge_attributes(G_prod, 'label')[(str(actual_node),str(next_node))]
            if ev == label:
                continue
            G_prod.remove_edge(str(actual_node),str(next_node))
            G_prod.add_edge(str(actual_node),str(next_node), label = label+','+ev)

        if actual_node == next_node:
            continue
        G_prod = iterat(G_prod,G1, G2, next_node)
    
    return G_prod


def iterat_parallel(G_parallel, G1, G2, sigma_sync, actual_node):
    ev_G1 = f.get_adjacencies_events(G1, actual_node[0])
    ev_G2 = f.get_adjacencies_events(G2, actual_node[1])
    ev_possible = list(set(ev_G1).union(set(ev_G2)))
    

    if len(ev_possible) == 0:
        return G_parallel

    G1_map = f.get_adjacencies(G1, actual_node[0])
    G2_map = f.get_adjacencies(G2, actual_node[1])
    #G1_map = {v: k for k, v in G1_map.items()}
    #G2_map = {v: k for k, v in G2_map.items()}

    for ev in ev_possible:
        if (ev in sigma_sync):
            if (ev in ev_G1) and (ev in ev_G2):
                next_node = [G1_map[ev], G2_map[ev]]    
            else:
                continue
        elif (ev in ev_G1):
                next_node = [G1_map[ev], actual_node[1]]    
        elif (ev in ev_G2):
                next_node = [actual_node[0], G2_map[ev]]    
        else:
            continue
        print(str(actual_node) + '----'+ev+'---->' +str(next_node))
        if not (str(actual_node),str(next_node)) in list(G_parallel.edges()):
            G_parallel.add_edge(str(actual_node),str(next_node), label = ev)
        else:
            label = nx.get_edge_attributes(G_parallel, 'label')[(str(actual_node),str(next_node))]
            if ev == label:
                continue
            G_parallel.remove_edge(str(actual_node),str(next_node))
            G_parallel.add_edge(str(actual_node),str(next_node), label = label+','+ev)

        if actual_node == next_node:
            continue
        G_parallel =  iterat_parallel(G_parallel.copy(), G1, G2, sigma_sync, next_node)
    
    return G_parallel

def iterat_observer(Obs, G, sigma_uo, mapping, actual_nodes):
    ev_possible = []    
    for i in actual_nodes:
        [ev_possible.append(x) for x in f.get_adjacencies_events(G, i)]
        
    if len(ev_possible) == 0:
        return Obs

    state = actual_nodes[:]
    ev_obs_possible = []
    for node in state:
        ev_possible = f.get_adjacencies_events(G, node)
    
        for ev in ev_possible:
            if (ev in sigma_uo):
                if not mapping[node][ev] in state:
                    state.append(mapping[node][ev])                
            else:
                if not ev in ev_obs_possible:
                    ev_obs_possible.append(ev)
    
    Obs = f.compute_next_obs(Obs, ev_obs_possible, G, sigma_uo, mapping, state)
    return Obs    
    
def compute_next_obs(Obs, ev_obs_possible, G, sigma_uo, mapping, state):
            
    for ev in ev_obs_possible:
        actual_nodes = []
        for node in state:
            try:
                actual_nodes.append(mapping[node][ev])
            except Exception:
                pass
        if actual_nodes == []:
            continue
        
        if not (str(state),str(actual_nodes)) in list(Obs.edges()):
            Obs.add_edge(str(state), str(actual_nodes), label= ev)
        else:
            label = nx.get_edge_attributes(Obs, 'label')[(str(state),str(actual_nodes))]
            if ev == label:
                continue
            Obs.remove_edge(str(state), str(actual_nodes))
            Obs.add_edge(str(state), str(actual_nodes), label = label+','+ev)
        if state == actual_nodes:
            continue
        Obs = f.iterat_observer(Obs,G,sigma_uo,mapping, actual_nodes)
    
    return Obs

