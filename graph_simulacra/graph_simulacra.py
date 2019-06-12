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
    rapid_rank(G)
    return G

def rapid_rank(G):
    '''Rapidly ranking the graph'''

    #copy of G is H
    H = G.copy()
    mem = 1
    
    while len(H) > 2:
        print(list(H))
        min_degree_dict = get_minimum_degree_dict(H)
        set_zero_rank_to_one(G, H, list(min_degree_dict.keys()))
        rank_leaf_neighbors(G, H, min_degree_dict)
        rank_leaf_neighbors_if_equal(G, H, min_degree_dict)
        mem = remove_leaves(H, min_degree_dict)

    if len(H) == 2:
        rank_last_two(G, H, mem)


                
def rank_last_two(G, H, mem):
    '''Rank last two remianing vertices'''
    if len(list(H.edges)) > 0:
        a = list(H.edges)[0][0]
        b = list(H.edges)[0][1]
        a_rank = H.nodes[a]['rank']
        b_rank = H.nodes[b]['rank']
        if a_rank == b_rank:
            if (a_rank - mem) < mem:
                H.nodes[a]['rank'] = a_rank - mem
                G.nodes[a]['rank'] = a_rank - mem
            else:
                H.nodes[a]['rank'] = a_rank + 1
                G.nodes[a]['rank'] = a_rank + 1
            
                
def remove_leaves(H, min_degree_dict):
    '''Remove all leaves in the copy of graph'''
    mem = 0
    for idx, d in min_degree_dict.items():
        mem = H.nodes[idx]['rank']
        H.remove_node(idx)
    return mem


def rank_leaf_neighbors_if_equal(G, H, min_degree_dict):
    '''Increases rank of the neighbors if they are equal'''
    for midx, mrank in min_degree_dict.items():
        neighbors_ranks_dict = get_neighbors_ranks_dict(H, midx)
        flipped_ranks_dict = get_dup_flipped_dict(neighbors_ranks_dict)
        for nrank, nodes_list in flipped_ranks_dict.items():
            if len(nodes_list) >= 2:
                H.nodes[nodes_list[0]]['rank'] = int(G.nodes[nodes_list[0]]['rank']) + 1
                G.nodes[nodes_list[0]]['rank'] = int(G.nodes[nodes_list[0]]['rank']) + 1


def get_dup_flipped_dict(d):
    flipped = {}
    for key, value in d.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)
    return flipped
    

def rank_leaf_neighbors(G, H, min_degree_dict):
    '''Increases rank of the neighbors'''
    for midx, d in min_degree_dict.items():
        mrank = H.nodes[midx]['rank']
        neighbors_ranks_dict = get_neighbors_ranks_dict(H, midx)
        for nidx, nrank in neighbors_ranks_dict.items():
            if nrank == 0 or nrank == mrank:
                H.nodes[nidx]['rank'] = mrank + 1
                G.nodes[nidx]['rank'] = mrank + 1

                
def set_zero_rank_to_one(G, H, list_of_nodes):
    '''set 1, if the rank is 0'''
    for i in list_of_nodes:
        if int(H.nodes[i]['rank']) == 0:
            H.nodes[i]['rank'] = 1
            G.nodes[i]['rank'] = 1

            
def get_neighbors_ranks_dict(H, node):
    '''returns a dictionary with neighbors rank'''
    neighbors_ranks_dict = {}
    for i in list(H.neighbors(node)):
        neighbors_ranks_dict[i] = int(H.nodes[i]['rank'])
    return neighbors_ranks_dict


def get_minimum_degree_dict(H):
    '''returns a dictionary with min degrees'''
    min_degree_dict = {}
    degree_dict = get_degree_dict(H)
    min_degree = degree_dict[min(degree_dict, key=degree_dict.get)]
    for i in list(H):
        if int(H.degree(i)) == min_degree:
            min_degree_dict[i] = min_degree
    accepted_list = check_node_adjacency(H, list(min_degree_dict.keys()))
    min_degree_nodes = list(min_degree_dict.keys())
    for i in min_degree_nodes:
        if i not in accepted_list:
            del min_degree_dict[i]
    return min_degree_dict

def check_node_adjacency(H, list_of_nodes):
    '''iterate each node to check adjacency'''
    accepted_list = []
    if len(list_of_nodes) < 2:
        return list_of_nodes
    else:
        for idx, node in enumerate(list_of_nodes):
            for midx, mnode in enumerate(list_of_nodes[idx:]):
                if not H.has_edge(node, mnode):
                    accepted_list.append(node)
        return accepted_list
        

def get_degree_dict(H):
    '''returns a dictionary with degrees'''
    degree_dict = {}
    for i in list(H):
        degree_dict[i] = int(H.degree(i))
    return degree_dict


def get_rank_dict(G):
    '''returns a dictionary with ranks'''
    ranks_dict = {}
    for i in range(len(G)):
        ranks_dict[i] = int(G.nodes[i]['rank'])
    return ranks_dict


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



def print_ranks(G):
    for i in range(len(G)):
        print('-----------------------------------')
        print('node => '+str(i))
        print('rank => '+str(G.nodes[i]['rank']))
