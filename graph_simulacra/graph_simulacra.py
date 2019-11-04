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
    critical_rank(G)
    return G

def critical_rank(G):
    '''Iterate through vertecies'''

def pick_arbitary_node(G, biase=0):
    '''picks arbitary node'''

def root_rank(G):
    '''Set root rank'''


def get_rank_list(G):
    rank_list = []
    for i in range(len(G)):
        rank_list.append(int(G.nodes[i]['rank']))
    return rank_list                    

def print_ranks(G):
    for i in range(len(G)):
        print('-----------------------------------')
        print('node => '+str(i))
        print('rank => '+str(G.nodes[i]['rank']))
        
