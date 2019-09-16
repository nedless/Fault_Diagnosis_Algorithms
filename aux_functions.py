from des import *

def load_input():
        with open('input.txt', 'r') as myfile:
            input = myfile.read()
        return parse2des(input)

def parse2des(input):
    #Parsing incidence matrix
    gg = input.split("\n\n-\n\n")
    des_list = []

    for g in gg:        
        inc = []
        inc = g.split("\n")
        inc_matrix = []
        for line in inc:
            if line.find(':')>0:
                label = line[:-1]
                continue
            inc_matrix.append(line.strip().split(";"))
        G = des(inc_matrix, label)
        des_list.append(G)
    return des_list