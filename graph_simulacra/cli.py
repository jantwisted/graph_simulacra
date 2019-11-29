# -*- coding: utf-8 -*-


"""Console script for graph_simulacra."""
import sys
import click
from graph_simulacra import graph_simulacra
from graph_simulacra.ui_wrapper import MainWindow
from PyQt5.QtWidgets import *


@click.command()
def main():
    """Console script for graph_simulacra."""
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

