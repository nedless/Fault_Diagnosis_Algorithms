import aux_functions as f


aut_list = f.load_input()
Gl = aut_list[0]
Gl.verifier(['f'], [['c'],['b']])

Gd = aut_list[1]
Gd.Observer(['a','b','c'])
# G.get_accessible_part()
# G.get_coaccessible_part()
# G.strongly_connected()
# G.deepth_first_search()
# G_ts = G.top_sort();
F1 = aut_list[0]
F2 = aut_list[1]
P = F1//F2

print("testing changes for using git repository...")    