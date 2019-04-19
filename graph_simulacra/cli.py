# -*- coding: utf-8 -*-

"""Console script for graph_simulacra."""
import sys
import click
from graph_simulacra import graph_simulacra


@click.command()
def main(args=None):
    """Console script for graph_simulacra."""
    matrix_array = graph_simulacra.get_matrix()
    graph_simulacra.draw_graph(matrix_array)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

