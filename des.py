import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
from networkx.drawing.nx_agraph import to_agraph 
from random import shuffle,randint
import linecache
import aux_functions as f


class des:

    def __init__(self, inc_matrix, states, label, marked):        
        self.inc_matrix = inc_matrix
        self.states = states
        self.label = label
        self.marked = marked

        self.automate = self.define_des()
        self.generate_figure(self.automate)
        
        #deepth-first search
        self.time = 0
        self.color = []
        self.n_time = []

    def __repr__(self):        
        return self.label + '\n'  + str(self.inc_matrix)
    def get_automate(self):
        return self.automate
    def get_inc_matrix(self):
        return self.inc_matrix
    def get_label(self):
        return self.label
    def get_state_list(self):
        return self.states
    def get_marked(self):
        return self.marked
    def generate_figure(self, G,sufix='', label='',layout='dot', shape='circle'):                
        A = to_agraph(G)
        if label == '':
            label = self.label

        A.node_attr['shape']= shape
        for mark in self.marked:
            m = A.get_node(mark)
            m.attr['shape'] = 'doublecircle'
        A.layout(layout)                                                                 
        A.draw(label + sufix + '.png')
    
    def generate_strongly_figure(self,strongList,layout='dot'):
        A = to_agraph(self.automate) 
        A.node_attr['shape']='circle'

        for mark in self.marked:
            m = A.get_node(mark)
            m.attr['shape'] = 'doublecircle'            
        for con in strongList:
            color = linecache.getline('color_list.txt', randint(1, 129))[:-1]
            for v in con:
                n = A.get_node(v)
                n.attr['color']= color
        A.layout(layout)                                                                 
        A.draw(self.label + '_strongly' + '.png')

    def define_des(self):                        
        G = nx.DiGraph()
        for j in range(len(self.inc_matrix)):
            for k in range(len(self.inc_matrix[j])):
                if self.inc_matrix[j][k] != '0':
                    G.add_edge(self.states[j], self.states[k], label = self.inc_matrix[j][k])
        return G
    
    def get_transpose(self):
        inc_matrix_t = [list(i) for i in zip(*self.inc_matrix)]

    def breadth_first_search(self, initial=0):
        color = []
        for i in range(len(self.inc_matrix)):
            color.append('w')
                
        color[initial] = 'g'
        new_color = color[:]
        deepth = 0
        result = {}
        while (True):            
            
            color = new_color[:]
            chk = 0

            for pivot in range(len(self.inc_matrix)):
                if color[pivot] != 'g':
                    chk += 1
                    if chk == len(self.inc_matrix):
                        return self.bfs_result(result, color)
                    else:
                        continue 
                inc = self.inc_matrix[pivot]
            
                for i in range(len(inc)):
                    if inc[i] != '0':
                        if color[i] == 'w':
                            new_color[i] = 'g'
                
                result[self.states[pivot]] = str(deepth)                
                new_color[pivot] = 'b'

            deepth += 1
    def bfs_result(self, result, color):
        for i in range(len(color)):
            if color[i] == 'w':
                result[self.states[i]] = '*'
        
        mapping = {}
        for k in result.keys():
            mapping[k] = k + '(' + result[k] + ')'
        
        mark_bckp = self.marked[:]
        for i in range(len(self.marked)):
            self.marked[i] = mapping[self.marked[i]]
            
        G_bfs = nx.relabel_nodes(self.automate, mapping)
        self.generate_figure(G= G_bfs, sufix='_bfs')
        
        self.marked = mark_bckp[:]
        r = (G_bfs, result)
        return r
    
    def  deepth_first_search(self):
        self.color = []
        self.time = 0
        self.n_time = []
        choice_list = []

        for i in range(len(self.inc_matrix)):
            self.color.append('w')
            choice_list.append(i)
            self.n_time.append('*')
        
        for i in range(len(self.inc_matrix)):            
            choice_list = list(filter( \
                lambda a: self.color[a] == 'w',  choice_list))
            if len(choice_list) == 0:
                break
            shuffle(choice_list)            
            if self.color[choice_list[0]] == 'w':
                self.dfs_visit(choice_list[0])
        
        return self.dfs_result(self.n_time)

    def dfs_visit(self, c):
        self.time += 1
        self.n_time[c] = str(self.time) + '/'
        self.color[c] = 'g'

        for j in range(len(self.inc_matrix[c])):
            if self.inc_matrix[c][j] != '0' and self.color[j]=='w':
                self.dfs_visit(j)
        
        self.color[c] = 'b'
        self.time += 1
        self.n_time[c] = self.n_time[c] + str(self.time)

    def dfs_result(self, n_time):
        
        mapping = {}
        for i in range(len(n_time)):
            mapping[self.states[i]] = self.states[i] + '('+ n_time[i] +')'
        
        marked_bckp = self.marked[:]
        for j in range(len(self.marked)):
            self.marked[j] = mapping[self.marked[j]]  
        
        G_dfs = nx.relabel_nodes(self.automate, mapping)
        self.generate_figure(G=G_dfs, sufix='_dfs')
        self.marked = marked_bckp[:]
        r = (G_dfs, n_time)
        return r

    def top_sort(self):
        r = self.deepth_first_search()
        
        top = []
        for n in r[1]:
            top.append(n[n.index('/')+1:])
        
        s = top[:]
        s.sort(reverse=True)

        marked = self.marked

        corresp = {}
        for i in range(len(s)):
            k = top.index(s[i])
            corresp[str(i)] = self.states[k]

        rev_corresp = inv_map = {v: k for k, v in corresp.items()}
        for j in range(len(marked)):
            marked[j] = rev_corresp[marked[j]]

        keys = [k for k in corresp.keys()]
        
        keys.sort()

        new_inc_matrix = []
        for k in keys:
            new_row = []
            for j in range(len(keys)):
                new_row.append(self.inc_matrix[self.states.index(corresp[k])][self.states.index(corresp[str(j)])])
            
            new_inc_matrix.append(new_row)
        
        G_topsorted = des(new_inc_matrix, keys, 'G_topsorted', marked)
        return G_topsorted

    def strongly_connected(self):
        stack = []
        for i in range(len(self.inc_matrix)):
            self.color.append('w')
            self.n_time.append('*') #not used
        
        for j in range(len(self.inc_matrix)):
            if self.color[j]=='w':
                self.fill_sort(j, stack)
        
        #Gr = self.get_transpose()
        inc_matrix_bckp = self.inc_matrix[:]
        self.inc_matrix = [list(i) for i in zip(*self.inc_matrix)]

        for i in range(len(self.inc_matrix)):
            self.color[i] = 'w'
        
        result = []
        while(stack):
            i = stack.pop()
            if self.color[i]=='w':
                self.dfs_visit(i)
            r=[]
            for v in range(len(self.color)):
                if self.color[v] == 'b':
                    self.color[v] = 'r'
                    r.append(self.states[v])
            
            if len(r) > 0:
                result.append(r)
        
        self.inc_matrix = inc_matrix_bckp[:]
        print(result) 
        self.generate_strongly_figure(result)
        return result

    
    def fill_sort(self, c, stack):
        self.color[c] = 'g'
        for j in range(len(self.inc_matrix[c])):
            if self.inc_matrix[c][j] != '0' and self.color[j]=='w':
                self.fill_sort(j, stack)
        stack = stack.append(c)
    
    def get_accessible_part(self, initial = 0, draw = True, rev = False):
        #assuming that the initial node is the node '1'
        r = self.breadth_first_search(initial)
        result = r[1]

        noAc = []
        Ac = []
        for c in result.keys():
            if result[c] != '*':
                Ac.append(c)
            else:
                noAc.append(c)
        if draw:
            self.generate_accessible_figure(noAc, self.automate, 'Ac('+self.label+')')
        if rev:
            return noAc
        return Ac

        
    def generate_accessible_figure(self, noAc, G, label='',layout='dot'):        
        A = to_agraph(G)
        A.node_attr['shape']='circle'
        for mark in self.marked:
            m = A.get_node(mark)
            m.attr['shape'] = 'doublecircle'
        
        A.remove_nodes_from(noAc)

        A.layout(layout)                                                                 
        A.draw(label + '.png')

    def get_coaccessible_part(self, draw = True):
        all_nodes = self.automate.nodes()

        co_chk = False
        CoAc = []
        for node in all_nodes:
            if not(node in CoAc):
                node_Ac = self.get_accessible_part(self.states.index(node),False)                
                for mark in self.marked:
                    if mark in node_Ac:
                        CoAc.append(node)                        
                        co_chk = True
                        break
                        
        noCoAc = []
        for node in all_nodes:
            if not(node in CoAc):
                noCoAc.append(node)
        if draw:
            self.generate_accessible_figure(noCoAc, self.automate, 'CoAc('+self.label+')')

        return CoAc
    
    
    def __mul__(D1, D2):
        noAc_G1 = D1.get_accessible_part(draw = False, rev = True)
        noAc_G2 = D2.get_accessible_part(draw = False, rev = True)
        
        G1 = D1.get_automate()
        G2 = D2.get_automate()

        G1.remove_nodes_from(noAc_G1)
        G2.remove_nodes_from(noAc_G2)

        #sigma_G1 = G1.get_sigma(G1)
        #sigma_G2 = G2.get_sigma(G2)
        #sigma_prod = [value for value in sigma_G1 if value in sigma_G2]

        G_prod = nx.DiGraph()
        mapping = nx.get_edge_attributes(G1, 'label')
        inv_map = {v: k for k, v in mapping.items()}

        
        G1_states = D1.get_state_list()
        G2_states = D2.get_state_list()
        actual_node = [G1_states[0],G2_states[0]]

        G_prod.add_node(str(actual_node))
        G_prod = f.iterat(G_prod,G1, G2, actual_node)


        settings= f.generate_incmatrix_from_automate(G_prod, D1,D2)
        P = des(settings[0], settings[1], \
             D1.get_label() + '*' + D2.get_label(), settings[2])

        return P

    def __floordiv__(D1, D2):
            
        noAc_G1 = D1.get_accessible_part(draw = False, rev = True)
        noAc_G2 = D2.get_accessible_part(draw = False, rev = True)
        
        G1 = D1.get_automate()
        G2 = D2.get_automate()

        G1.remove_nodes_from(noAc_G1)
        G2.remove_nodes_from(noAc_G2)

        sigma_G1 = f.get_sigma(G1)
        sigma_G2 = f.get_sigma(G2)
        sigma_sync = [value for value in sigma_G1 if value in sigma_G2]

        G_parallel = nx.DiGraph()
        mapping = nx.get_edge_attributes(G1, 'label')
        inv_map = {v: k for k, v in mapping.items()}
        
        G1_states = D1.get_state_list()
        G2_states = D2.get_state_list()
        actual_node = [G1_states[0],G2_states[0]]

        G_parallel.add_node(str(actual_node))
        G_parallel = f.iterat_parallel(G_parallel.copy(),G1, G2, sigma_sync, actual_node)

        settings= f.generate_incmatrix_from_automate(G_parallel, D1,D2)
        P = des(settings[0], settings[1], \
             D1.get_label() + '||' + D2.get_label(), settings[2])

        return P
    
    def Observer(self, sigma_o):        
        noAc = self.get_accessible_part(draw = False, rev = True)
        
        G = self.get_automate()        
        G.remove_nodes_from(noAc)        

        sigma = f.get_sigma(G)
        sigma_uo = []
        for ev in sigma:
            if not (ev in sigma_o):
                sigma_uo.append(ev)

        Obs = nx.DiGraph()
        mapping = nx.get_edge_attributes(G, 'label')
        inv_map = {v: k for k, v in mapping.items()}
        
        states = self.states
        actual_node = [states[0]]

        mapping = {}
        for node in states:
            mapping[node] = f.get_adjacencies(G, node)

        Obs = f.iterat_observer(Obs.copy(),G, sigma_uo, mapping, actual_node)

        settings= f.generate_incmatrix_for_obs_automate(Obs)

        P = des(settings[0], settings[1], \
             'Obs(' + self.label +')', [])
        P.generate_figure(P.get_automate(), label='Obs(' + self.label +')',shape='box')

        return P
    
    def build_fail_rotulator(self, fail_events):
        events = ""
        for ev in fail_events:
            events += ev + ","
        events = events[:-1]
        return des([['0',events],['0',events]], ['N','Y'], 'Rotulator',[])

    def verifier(self, fail_events, uo_events):
        rot = self.build_fail_rotulator(fail_events)
        G = des(self.inc_matrix,self.states,self.label,self.marked)
        Gl = G // rot
        Gn = self.generate_non_fail_automate(Gl)
        Gf = self.generate_fail_automate(Gl)

        Gn_r = []
        for i in range(len(uo_events)):
            Gr = Gn
            inc_m = Gn.get_inc_matrix()[:]
            for ev in uo_events[i]:
                for x in inc_m:
                    for s in range(len(x)):
                        if x[s].find(ev)>-1:
                            x[s] = x[s].replace(ev, ev+'_r'+str(i))

                    
            Gn_r.append(des(inc_m, Gn.get_state_list(), "G_N"+str(i), []))

        Gn_p = Gn_r[0]
        for g in Gn_r[1:]:
            Gn_p = Gn_p // g
        
        Gv= Gn_p // Gf
        Gv= des(Gv.get_inc_matrix(), Gv.get_state_list(), self.label+'_V',[])
        Gv.generate_figure(Gv.get_automate(),shape='box')
        return Gv


    
    def generate_non_fail_automate(self, D):
        G = D.get_automate().copy()
        nodes = list(G.nodes())
        for n in nodes:
            if n.find('Y') > -1:
                G.remove_node(n)
        noAc = self.get_accessible_part(draw = False, rev = True)
        G.remove_nodes_from(noAc)        

        settings = f.generate_incmatrix_for_obs_automate(G)
        return des(settings[0], settings[1], self.label+'_N',[])
    
    def generate_fail_automate(self, D):
        G = D.get_automate().copy()
        nodes = list(G.nodes())

        marked = []        
        for n in nodes:
            if n.find('Y') > -1:
                marked.append(n)
        
        stt = D.get_state_list()
        label = D.get_label()+'_f'

        Gt = des(D.get_inc_matrix(), stt, label, marked[:])
        CoAc = Gt.get_coaccessible_part(draw = False)

        for n in nodes:
            if not n in CoAc:
                G.remove_node(n)
                

        settings = f.generate_incmatrix_for_obs_automate(G)
        return des(settings[0], settings[1], self.label+'f',[])




        
    
    





            
        
        
            



