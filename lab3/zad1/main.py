from dimacs import *
from time import time
from os import listdir
from os.path import isfile, join
from math import inf
from enum import Enum

class GType(Enum):
    NONE_TYPE = 0
    CNFFORMULA = 1
    UNDIR_GRAPH = 2
    DIR_GRAPH = 3

class InputError(Exception): pass


# clique100 -> 20 sekund
# clique200 -> 600 sekund
# grid100x100 -> 140 sekund
def prog(V, E):

    n = V+1
    flow = [[0 for _ in range(n)] for _ in range(n)]
    parent = [None for _ in range(n)]
    visited = [False for _ in range(n)]
    neighbours = [[] for _ in range(n)]

    # dla listy krawedzi
    for u, v, w in E:
        neighbours[u].append(v)
        neighbours[v].append(u)

    result = float("inf")
    for i in range(1, n):
        result = min(result, len(neighbours[i]))

    start = 1


    # for start in range(1, n):
    for end in range(start + 1, n):
        for u, v, w in E:
            flow[u][v] = 0
            flow[v][u] = 0

        count = 0
        while count < result:
            for i in range(n):
                parent[i] = None
                visited[i] = False

            stack = []
            stack.append(start)
            while len(stack) > 0 and not visited[end]:
                x = stack.pop()
                if not visited[x]:
                    visited[x] = True
                for i in neighbours[x]:
                    if not visited[i] and flow[x][i] < 1:
                        parent[i] = x
                        stack.append(i)

            if not visited[end]:
                break

            i = end
            while i != start:
                flow[parent[i]][i] += 1
                flow[i][parent[i]] -= 1
                i = parent[i]
            count += 1

        result = min(result, sum(flow[start]))

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
