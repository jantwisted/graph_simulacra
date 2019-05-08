# -*- coding: utf-8 -*-


"""Console script for graph_simulacra."""
import sys
import click
from graph_simulacra import graph_simulacra
from graph_simulacra.ui_wrapper import MainWindow
from PyQt5.QtWidgets import *


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--xwindow', '-X', is_flag=True, help="gui")
@click.option('--native', is_flag=True, help="native mode")
def main(verbose, xwindow, native):
    """Console script for graph_simulacra."""
    if verbose:
        print("verbose message")
    elif xwindow:
        print("X window")
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())
    elif native:
        print("X(native) window")
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

