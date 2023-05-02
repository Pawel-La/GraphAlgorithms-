from dimacs import *
from time import time
from os import listdir
from os.path import isfile, join
from math import inf
from enum import Enum
import networkx as nx
from networkx.algorithms.planarity import check_planarity
from networkx.algorithms.flow import maximum_flow
from networkx.algorithms.components import strongly_connected_components


class GType(Enum):
    NONE_TYPE = 0
    CNFFORMULA = 1
    UNDIR_GRAPH = 2
    DIR_GRAPH = 3

class InputError(Exception): pass


def planar(V, E):
    G = nx.Graph()
    for node in range(1, V + 1):
        G.add_node(node)
    for edge in E:
        G.add_edge(edge[0], edge[1])

    return check_planarity(G)[0]


def maximal_flow(V, E):
    start = 1
    end = V
    G = nx.DiGraph()
    for node in range(1, V+1):
        G.add_node(node)
    for edge in E:
        G.add_edge(edge[0], edge[1])
        G[edge[0]][edge[1]]['capacity'] = edge[2]

    return maximum_flow(G, start, end)[0]


def sat_2CNF(V, L):
    G = nx.DiGraph()
    for node in range(-V, 0):
        G.add_node(node)
    for node in range(1, V + 1):
        G.add_node(node)
    for x, y in L:
        G.add_edge(-x, y)
        G.add_edge(-y, x)
    SCC = strongly_connected_components(G)

    flag = 1
    for S in SCC:
        for v in S:
            if -v in S:
                flag = 0
                break
        if not flag:
            break
    return flag


def getData(name, type):
    if type == GType.CNFFORMULA:
        return loadCNFFormula(name)
    elif type == GType.DIR_GRAPH:
        return loadDirectedWeightedGraph(name)
    elif type == GType.UNDIR_GRAPH:
        return loadWeightedGraph(name)
    else:
        raise InputError


if __name__ == "__main__":
    path = "C:\\school\\algorytmy grafowe\\lab7\\sat"
    files = [f for f in listdir(path) if isfile(join(path, f))]

    name_width = -inf
    for file in files:
        name_width = max(name_width, len(file))
    name_width += 15

    output = []
    print("File:".ljust(name_width) + " Result:".ljust(name_width) + "  Time:".ljust(15))
    for file in files:
        file = 'C:\\school\\algorytmy grafowe\\lab7\\sat\\' + file
        solution = int(readSolutionCNF(file))

        time_s = time()
        V, E = None, None
        try:
            V, E = getData(file, GType.CNFFORMULA)
        except:
            print("Wrong data type!")
        program = sat_2CNF(V, E)
        time_e = time()

        name = file + ':'
        if solution != program:
            print("zle\toczekiwano: " + str(solution) + ", a otrzymano: " + str(program))
        else:
            print(f'{name.ljust(name_width)} {str(solution == program).ljust(name_width)} {str(round(time_e - time_s, 3)).ljust(5, "0")}s')
