# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import string

class Node(object):
    def __init__(self, index, name, degree, rank):
        self.index = index
        self.name = name
        self.degree = degree
        self.rank = rank


def input_matrix_from_file(fd):
    shadow_list = []
    with open(fd, 'r') as f:
        h_list = [line.rstrip('\n') for line in f]
        for idx, r in enumerate(h_list):
            shadow_list.insert(idx, [int(i) for i in r.split(',')])
    return shadow_list



def get_label_with_attribute(G, rank_list=[]):
    labels_map = {}
    labels_list = list(string.ascii_lowercase)[0:len(G)]
    if not rank_list:
        for idx, i in enumerate(labels_list):
            labels_map[idx] = labels_list[idx]
    else:
        for idx, i in enumerate(rank_list):
            labels_map[idx] = labels_list[idx] + ':' + str(i)
    return labels_map

def get_fixed_positions(rank_list, labels_map):
    fixed_positions = {}
    highest_rank = max(rank_list)
    highest_rank_idx = rank_list.index(max(rank_list))

    r = 1
    while (r<=highest_rank):
        indices = [i for i, x in enumerate(rank_list) if x == r]
        for q in indices:
            fixed_positions[labels_map[q]]= (q+1,r)
        r += 1
    return fixed_positions        

        

def draw_graph(matrix_array):
    """draws the graph based on adjacency matrix"""

    # Initialize the Graph
    G = nx.Graph()
    adjacency_matrix = np.array(matrix_array)
    G = nx.from_numpy_matrix(adjacency_matrix)
    G = set_ranks(G)
    rank_list = get_rank_list(G)
    print_ranks(G)
    node_list = node_details(G)

    labels_map = get_label_with_attribute(G, rank_list)
    G = nx.relabel_nodes(G, labels_map, copy=False)

    # Draw Graph
    fixed_positions = get_fixed_positions(rank_list, labels_map)
    fixed_nodes = fixed_positions.keys()
    plt.figure()
    g_nodes = nx.spring_layout(G, pos=fixed_positions, fixed = fixed_nodes)
    nx.draw(G, g_nodes, with_labels=True, node_size=900)
    nx.draw_networkx_labels(G, g_nodes, bbox=dict(facecolor='yellow'))
    plt.savefig('/tmp/testplot.png')


def draw_graph_native(matrix_array):
    """draws the graph based on adjacency matrix"""

    # Initialize the Graph
    G = nx.Graph()
    adjacency_matrix = np.array(matrix_array)
    G = nx.from_numpy_matrix(adjacency_matrix)
#    G = set_ranks(G)
#    rank_list = get_rank_list(G)
#    print_ranks(G)
#    node_list = node_details(G)

    labels_map = get_label_with_attribute(G)
    G = nx.relabel_nodes(G, labels_map, copy=False)

    # Draw Graph
    plt.figure()
    g_nodes = nx.spring_layout(G)
    nx.draw(G, g_nodes, with_labels=True, node_size=900)
    nx.draw_networkx_labels(G, g_nodes, bbox=dict(facecolor='yellow'))
    plt.savefig('/tmp/testplot_native.png')


def node_details(G):
    node_list = []
    for i in range(len(G)):
        node_list.append(Node(i, 'A', G.degree(i), 1))

    return node_list

def get_degree_list(G):
    degree_list = []
    for i in range(len(G)):
        degree_list.append(G.degree(i))
    return list(dict.fromkeys(degree_list))


def set_ranks(G):
    # set all ranks to 0
    nx.set_node_attributes(G, '0', 'rank')
    degree = get_degree_list(G)
    exclude_nodes = []
    # rank leaves to 1 and everything else to 2
    exclude_nodes = rank_leaves(G, exclude_nodes)
    exclude_nodes = rank_nodes_level_one(G, exclude_nodes)
    return G

def get_rank_list(G):
    rank_list = []
    for i in range(len(G)):
        rank_list.append(int(G.nodes[i]['rank']))
    return rank_list

def get_keys_from_value(dlist, value):
    keys_list = []
    for d in dlist:
        if value == d['rank']:
            keys_list.append(d['idx'])
    print(keys_list)
    return keys_list

def rank_nodes_level_one(G, exclude_nodes):
    '''raise the rank of nodes, which has similar plural neighbors'''
    node_list = []
    for i in range(len(G)):
        if i not in exclude_nodes:
            nb_dict = []
            self_idx = i
            self_rank = int(G.nodes[i]['rank'])
            for n_node in list(G.neighbors(i)):
                nb_dict.append({'idx':n_node, 'rank':int(G.nodes[n_node]['rank'])})

            list_of_nb_ranks = [d['rank'] for d in nb_dict]

            if max(list_of_nb_ranks) < self_rank:
                continue
            elif max(list_of_nb_ranks) == self_rank and min(list_of_nb_ranks) == self_rank:
                G.nodes[self_idx]['rank'] = str(self_rank+1)
            elif max(list_of_nb_ranks) == self_rank and min(list_of_nb_ranks) < self_rank:
                for i in get_keys_from_value(nb_dict, self_rank):
                    G.nodes[i]['rank'] = str(self_rank+1)
            elif max(list_of_nb_ranks) > self_rank and self_rank in list_of_nb_ranks:
                G.nodes[self_idx]['rank'] = str(max(list_of_nb_ranks)+1)
            node_list.append(i)
                
    return exclude_nodes+node_list
                
def rank_leaves(G, exclude_nodes):
    '''rank leaves to 1 and everything else to 2'''
    leaves_list = []
    for i in range(len(G)):
        if i not in exclude_nodes:
            if G.degree(i)==1:
                leaves_list.append(i)
                G.nodes[i]['rank'] = 1
            else:
                G.nodes[i]['rank'] = 2

    return exclude_nodes + leaves_list
            

def print_ranks(G):
    for i in range(len(G)):
        print('-----------------------------------')
        print('node => '+str(i))
#        print('neighbors => '+str(list(G.neighbors(i))))
#        print('degree => '+str(G.degree(i)))
        print('rank => '+str(G.nodes[i]['rank']))
        
