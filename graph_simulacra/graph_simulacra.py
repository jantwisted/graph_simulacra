# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Node(object):
    def __init__(self, index, name, degree, rank):
        self.index = index
        self.name = name
        self.degree = degree
        self.rank = rank

def input_matrix(v = 1):
    matrix_array = []
    print("Insert the |V| × |V| matrix, separated by (,) and RETURN")
    for i in range(v):
        row = input()
        matrix_array.append(list(map(int, row.split(','))))
        i += 1
    return matrix_array


def input_matrix_from_file(fd):
    shadow_list = []
    with open(fd, 'r') as f:
        h_list = [line.rstrip('\n') for line in f]
        for idx, r in enumerate(h_list):
            shadow_list.insert(idx, [int(i) for i in r.split(',')])
    return shadow_list



def get_label_with_attribute(labels_map, rank_map):
    for rank_key, rank_value in rank_map.items():
        labels_map[rank_key] += ' : ' + rank_value
    return labels_map


def draw_graph(matrix_array):
    """draws the graph based on adjacency matrix"""

    # Initialize the Graph
    G = nx.Graph()
    adjacency_matrix = np.array(matrix_array)
    G = nx.from_numpy_matrix(adjacency_matrix)
    G = set_ranks(G)
    print_ranks(G)
    node_list = node_details(G)
    # Setting up the rank
    #rank_map = get_vertex_rank()
   # nx.set_node_attributes(G, rank_map, 'rank')

    # Setting up the labels
   # labels_map = get_label_map()
  #  labels_map = get_label_with_attribute(labels_map, rank_map)
   # G = nx.relabel_nodes(G, labels_map)

    # Draw Graph
    g_nodes = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, g_nodes, cmap = plt.get_cmap('jet'), with_labels=True)
    # g_node_attributes = {}
    # for node, coordinates in g_nodes.items():
    #     g_node_attributes[node] = (coordinates[0], coordinates[1] - 0.2)
    # node_attributes = nx.get_node_attributes(G, 'rank')
    # customer_node_attributes = {}
    # for node, attr in node_attributes.items():
    #     customer_node_attributes[node] = "r:" + attr
    # nx.draw_networkx_labels(G, g_node_attributes, labels=customer_node_attributes)
    nx.draw_networkx_labels(G, g_nodes, )
    plt.savefig('/tmp/testplot.png')

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

def rank_nodes_level_one(G, exclude_nodes):
    '''raise the rank of nodes, which has similar plural neighbors'''
    node_list = []
    equal_rank_list = []
    minor_rank_list = []
    for i in range(len(G)):
        if i not in exclude_nodes:
            minor_rank_list = []
            equal_rank_list = []
            for n_node in list(G.neighbors(i)):
                # check minor and equal nodes
                
                if int(G.nodes[i]['rank']) == int(G.nodes[n_node]['rank']):
                    equal_rank_list.append(n_node)
                elif int(G.nodes[i]['rank']) > int(G.nodes[n_node]['rank']):
                    minor_rank_list.append(n_node)

            # if both minor and equal present
            if minor_rank_list and equal_rank_list:
                for equal_node in equal_rank_list:
                    G.nodes[equal_node]['rank'] = str(int(G.nodes[equal_node]['rank'])+1)
                    node_list.append(i)
            # if only equal present
            elif not minor_rank_list and equal_rank_list:
                for equal_node in equal_rank_list:
                    G.nodes[i]['rank'] = str(int(G.nodes[i]['rank'])+1)
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
        
