# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

"""Main module."""

def input_matrix(v = 1):
    matrix_array = []
    print("Insert the |V| × |V| matrix, separated by (,) and RETURN")
    for i in range(v):
        row = input()
        matrix_array.append(list(map(int, row.split(','))))
        i += 1
    return matrix_array

def matrix_construct():
    v = int(input("Insert # of Vertices:\n"))
    return v

def get_matrix():
    v = matrix_construct()
    return input_matrix(v)

get_label_map = lambda: {v: k for v, k in enumerate(list(map(str, input("Insert labels, separated by (,)\n").split(','))))}
get_vertex_rank = lambda: {v: k for v, k in enumerate(list(map(str, input("Insert vertex rank, separated by (,)\n").split(','))))}

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

    # Setting up the rank
    rank_map = get_vertex_rank()
    nx.set_node_attributes(G, rank_map, 'rank')

    # Setting up the labels
    labels_map = get_label_map()
    labels_map = get_label_with_attribute(labels_map, rank_map)
    G = nx.relabel_nodes(G, labels_map)

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
    plt.show()


