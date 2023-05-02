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

# algorytm Stoera - Wagnera
# grid 100x100 przechodzi w 400s a tak to reszta szybko
def prog(V, E):
    class Node:
        def __init__(self):
            self.edges = {}  # słownik  mapujący wierzchołki do których są krawędzie na ich wagi

        def addEdge(self, to, weight):
            self.edges[to] = self.edges.get(to, 0) + weight
            # dodaj krawędź do zadanego wierzchołka
            # o zadanej wadze; a jeśli taka krawędź
            # istnieje, to dodaj do niej wagę

        def delEdge(self, to):
            if self.edges.get(to, 0) != 0:
                del self.edges[to]  # usuń krawędź do zadanego wierzchołka

    G = [Node() for _ in range(V+1)]
    for (u, v, w) in E:
        G[u].addEdge(v, w)
        G[v].addEdge(u, w)

    result = float("inf")
    for i in range(1,V+1):
        result = min(result, len(G[i].edges))
    if result == 0:
        return result

    q = PriorityQueue()

    for _ in range(V-1):
        used = [False for _ in range(V+1)]
        weights = [0 for _ in range(V+1)]
        S = []
        q.put([0, 1])

        while not q.empty():
            w, x = q.get()
            w *= -1

            if used[x]:
                continue

            for i in G[x].edges:
                if not used[i]:
                    weights[i] += G[x].edges[i]
                    q.put([-weights[i], i])

            S.append(x)
            used[x] = True

        result = min(result, weights[S[-1]])
        if result == 0:
            return 0

        copy = G[S[-1]].edges.copy()
        for i in copy:
            if i != S[-2]:
                G[S[-2]].addEdge(i, G[S[-1]].edges[i])
                G[i].addEdge(S[-2], G[S[-1]].edges[i])
            G[S[-1]].delEdge(i)
            G[i].delEdge(S[-1])

    return result


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
    path = "C:\\school\\algorytmy grafowe\\lab3\\graphs_lab3"
    files = [f for f in listdir(path) if isfile(join(path, f))]

    name_width = -inf
    for file in files:
        name_width = max(name_width, len(file))
    name_width += 15

    output = []
    print("File:".ljust(name_width) + " Result:".ljust(name_width) + "  Time:".ljust(15))
    for file in files:
        file = 'C:\\school\\algorytmy grafowe\\lab3\\graphs_lab3\\' + file
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
