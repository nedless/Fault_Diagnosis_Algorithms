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
    mm = get_marked(marked)
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
        G = des(inc_matrix, label, mm[label])
        des_list.append(G)
    return des_list

def get_marked(marked):
    mm = marked.split("\n")
    m_dict = {}
    for m in mm:
        label = m[:m.find(":")]
        mar = [s for s in m[m.find(":")+1:].split(",")]
        m_dict[label] = mar
    return m_dict
