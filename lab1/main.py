from dimacs import *
from time import time
from os import listdir
from os.path import isfile, join
from math import inf
from enum import Enum
from queue import PriorityQueue


class GType(Enum):
    NONE_TYPE = 0
    CNFFORMULA = 1
    UNDIR_GRAPH = 2
    DIR_GRAPH = 3


class InputError(Exception): pass


def prog(V, E):
    s = 1
    t = 2
    n = V + 1

    q = PriorityQueue()
    neighbours = [[] for _ in range(n)]
    d = [-float("inf") for _ in range(n)]
    visited = [False for _ in range(n)]

    for i in E:
        neighbours[i[0]].append([i[1], i[2]])
        neighbours[i[1]].append([i[0], i[2]])

    q.put([-float("inf"), s])

    while not q.empty():
        u = q.get()
        u[0] *= -1
        visited[u[1]] = True
        for v, w in neighbours[u[1]]:
            if not visited[v] and d[v] < min(u[0], w):
                d[v] = min(u[0], w)
                q.put([-d[v], v])

    return d[t]


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
    path = "C:\\school\\algorytmy grafowe\\lab1\\graphs"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    print(files)

    name_width = -inf
    for file in files:
        name_width = max(name_width, len(file))
    name_width += 15

    output = []
    print("File:".ljust(name_width) + " Result:".ljust(name_width) + "  Time:".ljust(15))
    for file in files:
        file = 'C:\\school\\algorytmy grafowe\\lab1\\graphs\\' + file
        solution = int(readSolution(file))

        time_s = time()
        V, E = None, None
        try:
            V, E = getData(file, GType.UNDIR_GRAPH)
        except:
            print("Wrong data type!")
        program = prog(V, E)
        time_e = time()

        name = file + ':'
        if solution != program:
            print("zle\toczekiwano: " + str(solution) + ", a otrzymano: " + str(program))
        else:
            print(f'{name.ljust(name_width)} {str(solution == program).ljust(name_width)} {str(round(time_e - time_s, 3)).ljust(5, "0")}s')
