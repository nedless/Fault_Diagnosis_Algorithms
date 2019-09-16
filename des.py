import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
from networkx.drawing.nx_agraph import to_agraph 
from random import shuffle


class des:
    def __init__(self, inc_matrix, label):        
        self.inc_matrix = inc_matrix
        self.label = label
        self.automate = self.define_des()
        self.generate_figure(self.automate)

        #deepth-first search
        self.time = []
        self.color = []

    def __repr__(self):        
        return self.label + '\n'  + str(self.inc_matrix)

    def generate_figure(self, G,sufix='', layout='dot'):                
        A = to_agraph(G) 
        A.layout(layout)                                                                 
        A.draw(self.label + sufix + '.png')

    def define_des(self):                        
        G = nx.DiGraph()
        for j in range(len(self.inc_matrix)):
            for k in range(len(self.inc_matrix[j])):
                if self.inc_matrix[j][k] != '0':
                    G.add_edge(str(j+1), str(k+1), label = self.inc_matrix[j][k])
        return G
    
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
        
        G_dfs = nx.relabel_nodes(self.automate, mapping)
        self.generate_figure(G=G_dfs, sufix='_dfs')

        r = (G_dfs, n_time)
        return r

    def top_sort(self):
        r = self.deepth_first_search()
        
        top = []
        for n in r[1]:
            top.append(n[n.index('/')+1:])
        
        sort = top[:]
        sort.sort(reverse=True)

        corresp = {}
        for i in range(len(sort)):
            k = top.index(sort[i])
            corresp[str(i+1)] = str(k+1)
        
        keys = [k for k in corresp.keys()]
        
        keys.sort()

        new_inc_matrix = []
        for k in keys:
            new_row = []
            for j in range(len(keys)):
                new_row.append(self.inc_matrix[int(corresp[k])-1][int(corresp[str(j+1)])-1])
            
            new_inc_matrix.append(new_row)#self.inc_matrix[int(corresp[k])-1][:])
        
        G_topsorted = des(new_inc_matrix, 'G_topsorted')
        return G_topsorted
            
        
        
            



