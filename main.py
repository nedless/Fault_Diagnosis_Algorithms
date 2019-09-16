import aux_functions as f


aut_list = f.load_input()
G = aut_list[0]
#G.deepth_first_search()
G_ts = G.top_sort();
    