import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
from networkx.drawing.nx_agraph import to_agraph 
from random import shuffle,randint
import linecache


class des:
    def __init__(self, inc_matrix, label, marked):        
        self.inc_matrix = inc_matrix
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

    def generate_figure(self, G,sufix='', layout='dot'):                
        A = to_agraph(G)
        A.node_attr['shape']='circle'
        for mark in self.marked:
            m = A.get_node(mark)
            m.attr['shape'] = 'doublecircle'
        A.layout(layout)                                                                 
        A.draw(self.label + sufix + '.png')
    
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
                    G.add_edge(str(j+1), str(k+1), label = self.inc_matrix[j][k])
        return G
    
    def get_transpose(self):
        inc_matrix_t = [list(i) for i in zip(*self.inc_matrix)]

    def breadth_first_search(self, initial='1'):
        color = []
        for i in range(len(self.inc_matrix)):
            color.append('w')
                
        color[int(initial)-1] = 'g'
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
                
                result[str(pivot+1)] = str(deepth)                
                new_color[pivot] = 'b'

            deepth += 1
    def bfs_result(self, result, color):
        for i in range(len(color)):
            if color[i] == 'w':
                result[str(i+1)] = '*'
        
        mapping = {}
        for k in result.keys():
            mapping[k] = k + '(' + result[k] + ')'
        
        G_bfs = nx.relabel_nodes(self.automate, mapping)
        self.generate_figure(G=G_bfs, sufix='_bfs')

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
            mapping[str(i+1)] = str(i+1) + '('+ n_time[i] +')'
        
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
        s.sort()

        marked = self.marked

        corresp = {}
        for i in range(len(s)):
            k = top.index(s[i])
            corresp[str(i+1)] = str(k+1)

        rev_corresp = inv_map = {v: k for k, v in corresp.items()}
        for j in range(len(marked)):
            marked[j] = rev_corresp[marked[j]]

        keys = [k for k in corresp.keys()]
        
        keys.sort()

        new_inc_matrix = []
        for k in keys:
            new_row = []
            for j in range(len(keys)):
                new_row.append(self.inc_matrix[int(corresp[k])-1][int(corresp[str(j+1)])-1])
            
            new_inc_matrix.append(new_row)
        
        G_topsorted = des(new_inc_matrix, 'G_topsorted', marked)
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
                    r.append(str(v+1))
            
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

            
        
        
            



