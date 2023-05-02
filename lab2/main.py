from dimacs import *
from time import time
from os import listdir
from os.path import isfile, join
from math import inf
from enum import Enum
from collections import deque


class GType(Enum):
    NONE_TYPE = 0
    CNFFORMULA = 1
    UNDIR_GRAPH = 2
    DIR_GRAPH = 3


class InputError(Exception): pass


def prog1(V, E):
    def dfs(x):
        visited[x] = True
        for i in range(n-1, -1, -1):
            if visited[end]:
                return
            if not visited[i] and capacity[x][i] - flow[x][i] > 0:
                parent[i] = x
                dfs(i)

    n = V+1
    capacity = [[0 for _ in range(n)] for _ in range(n)]
    flow = [[0 for _ in range(n)] for _ in range(n)]
    parent = [None for _ in range(n)]
    visited = [False for _ in range(n)]
    start = 1
    end = V

    # dla listy krawedzi
    for u, v, w in E:
        capacity[u][v] = w

    while True:
        for i in range(n):
            parent[i] = None
            visited[i] = False

        dfs(start)

        if not visited[end]:
            break

        i = end
        f = float('inf')
        while i != start:
            f = min(f, capacity[parent[i]][i] - flow[parent[i]][i])
            i = parent[i]

        i = end
        while i != start:
            flow[parent[i]][i] += f
            flow[i][parent[i]] -= f
            i = parent[i]

    return sum(flow[start])


def prog2(V, E):
    def bfs():
        q = deque()
        q.append(start)
        while q and not visited[end]:
            u = q.pop()
            for v in neighbours[u]:
                if not visited[v] and capacity[u][v] - flow[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    q.append(v)

    n = V+1
    capacity = [[0 for _ in range(n)] for _ in range(n)]
    flow = [[0 for _ in range(n)] for _ in range(n)]
    parent = [None for _ in range(n)]
    visited = [False for _ in range(n)]
    neighbours = [[] for _ in range(n)]
    start = 1
    end = V

    # dla listy krawedzi
    for u, v, w in E:
        capacity[u][v] = w
        neighbours[u].append(v)
        neighbours[v].append(u)

    while True:
        for i in range(n):
            parent[i] = None
            visited[i] = False

        # szukanie sciezki powiekszajacej
        bfs()

        if not visited[end]:
            break

        # liczenie maksymalnego przeplywu przez sciezke powiekszajaca
        i = end
        f = float('inf')
        while i != start:
            f = min(f, capacity[parent[i]][i] - flow[parent[i]][i])
            i = parent[i]

        # aktualizowanie flowów na znalezionej sciezce powiekszajacej
        i = end
        while i != start:
            flow[parent[i]][i] += f
            flow[i][parent[i]] -= f
            i = parent[i]

    return sum(flow[start])


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
    path = "C:\\school\\algorytmy grafowe\\lab2\\flow"
    files = [f for f in listdir(path) if isfile(join(path, f))]

    name_width = -inf
    for file in files:
        name_width = max(name_width, len(file))
    name_width += 15

    output = []
    print("File:".ljust(name_width) + " Result:".ljust(name_width) + "  Time:".ljust(15))
    for file in files:
        file = 'C:\\school\\algorytmy grafowe\\lab2\\flow\\' + file
        solution = int(readSolution(file))

        time_s = time()
        V, E = None, None
        try:
            V, E = getData(file, GType.DIR_GRAPH)
        except:
            print("Wrong data type!")
        program = prog1(V, E)
        time_e = time()

        name = file + ':'
        if solution != program:
            print("zle\toczekiwano: " + str(solution) + ", a otrzymano: " + str(program))
        else:
            print(f'{name.ljust(name_width)} {str(solution == program).ljust(name_width)} {str(round(time_e - time_s, 3)).ljust(5, "0")}s')
