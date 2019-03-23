# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

"""Main module."""

def input_matrix(x = 1, y = 1):
    matrix_array = []
    print("Insert the matrix, separated by (,)")
    for i in range(y):
        row = input()
        matrix_array.append(list(map(int, row.split(','))))
        i += 1
    return matrix_array

def matrix_construct():
    x = int(input("Insert x:"))
    y = int(input("Insert y:"))
    return (x, y)

def get_matrix():
    (x, y) = matrix_construct()
    return input_matrix(x, y)

def draw_graph(matrix_array):
    """draws the graph based on adjacency matrix"""
    G = nx.Graph()
    adjacency_matrix = np.array(matrix_array)
    G = nx.from_numpy_matrix(adjacency_matrix)
    nx.draw(G, cmap = plt.get_cmap('jet'), with_labels=True)
    plt.show()

if __name__=='__main__':
    """main method"""
    matrix_array = get_matrix()
    draw_graph(matrix_array)
