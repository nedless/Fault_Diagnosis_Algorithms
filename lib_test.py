import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as img
import pygraphviz
import des
from networkx.drawing.nx_agraph import to_agraph 


g_input = "G:\n0;b;a\n0;c;0\n0;0;c\n\n-\n\nH:\n0;b;a\n0;c;0\n0;0;c" 

with open('input.txt', 'r') as myfile:
  g_input = myfile.read()
#Parsing incidence matrix
gg = g_input.split("\n\n-\n\n")
inc_matrixes = []
des_list = []
for g in gg:
    if g.find(':')>0:
        label = g[:-1]
        break

    inc = []
    inc = g.split("\n")

    inc_matrix = []
    for line in inc:
        inc_matrix.append(line.strip().split(";"))
    
    des_list.append(des(inc_matrix, label))
    

G_list = []
for i in range(len(inc_matrixes)):
    G = nx.DiGraph()
    for j in range(len(inc_matrixes[i])):
        for k in range(len(inc_matrixes[i][j])):
            if inc_matrixes[i][j][k] != '0':
                G.add_edge(str(j+1)+'m', str(k+1)+'m', label = inc_matrixes[i][j][k])
    G_list.append(G)
    G = 0
    
for g in G_list:
    A = to_agraph(g) 
    A.layout('dot')                                                                 
    A.draw('multi.png')
    
    #pos = nx.spring_layout(g)
    #nx.draw(g, pos,)
    #nx.draw_networkx_edge_labels(g, pos, font_color='red')
    #plt.axis('off')
    #plt.show()
