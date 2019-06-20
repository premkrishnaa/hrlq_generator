from graph_class import Graph
from members import *
from maxcard_lp import *
from stable_matching import *
import collections
import random
import numpy as np
import cplex
import os

def random_model(n1, n2, k, cap):
    """
    create a graph with the partition A of size n1
    and partition B of size n2 using the random model
    :param n1: size of partition A
    :param n2: size of partition B
    :param k: length of preference list for vertices in A
    :param cap: capacity of a vertex in partition B
    :return: bipartite graph with above properties
    """
    def order_by_master_list(l, master_list):
        return sorted(l, key=master_list.index)

    g = Graph()

    # create the sets R and H, r_1 ... r_n1, h_1 .. h_n2
    R = set('r{}'.format(i) for i in range(1, n1+1))
    H = set('h{}'.format(i) for i in range(1, n2+1))

    for res in R:
        g.residents.append(Resident(res))

    for hosp in H:
        g.hospitals.append(Hospital(hosp, 0, cap))

    # prepare a master list
    # master_list = list(h for h in H)
    # random.shuffle(master_list)

    pref_lists_H, pref_lists_R = collections.defaultdict(list), {}
    for resident in R:
        r_ind = resident[1:]
        pref_list = random.sample(H, min(len(H), k))  # random.randint(1, len(H)))  # sample houses
        pref_lists_R[resident] = pref_list  # order_by_master_list(pref_list, master_list)
        # add these residents to the preference list for the corresponding hospital
        for hospital in pref_list:
            h_ind = hospital[1:]
            pref_lists_H[hospital].append(resident)
            g.edges.append(Edge(r_ind,h_ind))

        res = g.get_resident(resident)
        for hosp in pref_lists_R[resident]:
            res.pref.append(g.get_hospital(hosp))

    for hospital in H:
        random.shuffle(pref_lists_H[hospital])
        hosp = g.get_hospital(hospital)
        for res in pref_lists_H[hospital]:
            hosp.pref.append(g.get_resident(res))

    return g

def mahadian_model(n1, n2, k, cap):
    """
    create a graph with the partition R of size n1 and
    partition H of size n2 using the model as described in
    Marriage, Honesty, and Stability
    Immorlica, Nicole and Mahdian, Mohammad
    Sixteenth Annual ACM-SIAM Symposium on Discrete Algorithms
    :param n1: size of partition R
    :param n2: size of partition H
    :param k: length of preference list for the residents
    :param cap: capacity of the hospitals
    :return: bipartite graph with above properties
    """
    def order_by_master_list(l, master_list):
        return sorted(l, key=master_list.index)

    g = Graph()

    # create the sets R and H, r_1 ... r_n1, h_1 .. h_n2
    R = list('r{}'.format(i) for i in range(1, n1+1))
    H = list('h{}'.format(i) for i in range(1, n2+1))

    # prepare a master list
    master_list = list(r for r in R)
    random.shuffle(master_list)

    for res in R:
        g.residents.append(Resident(res))

    for hosp in H:
        g.hospitals.append(Hospital(hosp, 0, cap))

    # setup a probability distribution over the hospitals
    p = np.random.geometric(p=0.10, size=len(H))

    # normalize the distribution
    p = p / np.sum(p)  # p is a ndarray, so this operation is correct

    prob_dict = dict(zip(H, p))
    master_list_h = sorted(H, key=lambda h: prob_dict[h], reverse=True)
    # print(prob_dict, master_list_h, sep='\n')

    pref_H, pref_R = collections.defaultdict(list), {}
    for r in R:
        # sample women according to the probability distribution and without replacement
        pref_R[r] = list(np.random.choice(H, size=min(len(H), k), replace=False, p=p))
        # add these man to the preference list for the corresponding women
        r_ind = r[1:]
        for h in pref_R[r]:
            h_ind = h[1:]
            pref_H[h].append(r)
            g.edges.append(Edge(r_ind, h_ind))

    for r in R:
        pref_R[r] = order_by_master_list(pref_R[r], master_list_h)
        res = g.get_resident(r)
        for hosp in pref_R[r]:
            res.pref.append(g.get_hospital(hosp))


    for h in H:
        pref_H[h] = order_by_master_list(pref_H[h], master_list)
        #random.shuffle(pref_H[h])
        hosp = g.get_hospital(h)
        for res in pref_H[h]:
            hosp.pref.append(g.get_resident(res))

    return g

def set_lower_quotas(g):
    m = get_stable_matching(g)
    generate_max_card_lp(g, 'temp.txt')
    model = cplex.Cplex('temp.txt')
    model.solve()
    var = model.variables.get_names()
    for v in var:
        v_split = v.split('_')
        h_name = 'h' + v_split[2]
        if(model.solution.get_values(v) > 0.5):
            h = g.get_hospital(h_name)
            if(len(h.pref) > 0 and len(h.matched) == 0):
                h.lq = 1

    os.system('rm temp.txt')

def random_model_generator(n1, n2, k, cap):
    g = random_model(n1, n2, k, cap)
    set_lower_quotas(g)
    return g

def mahadian_model_generator(n1, n2, k, cap):
    g = mahadian_model(n1, n2, k, cap)
    set_lower_quotas(g)
    return g

def main():
    import sys
    if len(sys.argv) < 6:
        print("usage: {} <n1> <n2> <k> <capacity> <output_path>".format(sys.argv[0]), file=sys.stderr)
    else:
        n1, n2, k, max_capacity = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        output_path = sys.argv[5]
        G = mahadian_model_generator(n1, n2, k, max_capacity)
        # G = random_model_generator(n1, n2, k, max_capacity)
        G.print_to_file(output_path)

if __name__ == '__main__':
    main()
