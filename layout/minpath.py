__author__ = 'Elvan'
__date__ = '2017/9/6 20:30'


inf = float("inf")


class PrioQueueError(ValueError):
    pass


class PrioQueue:
    def __init__(self, elist=[]):
        self._elems = list(elist)
        if elist:
            self.buildheap()

    def is_empty(self):
        return not self._elems

    def peek(self):
        if self.is_empty():
            raise PrioQueueError("in peek")
        return self._elems[0]

    def enqueue(self, e):
        self._elems.append(None)
        self.siftup(e, len(self._elems) - 1)

    def siftup(self, e, last):
        elems, i, j = self._elems, last, (last-1)//2
        while i > 0 and e < elems[j]:
            elems[i] = elems[j]
            i, j = j, (j-1)//2
        elems[i] = e

    def dequeue(self):
        if self.is_empty():
            raise PrioQueueError("in dequeue")
        elems = self._elems
        e0 = elems[0]
        e = elems.pop()
        if len(elems) > 0:
            self.siftdown(e, 0, len(elems))
        return e0

    def siftdown(self, e, begin, end):
        elems, i, j = self._elems, begin, begin*2+1
        while j < end:
            if j+1 < end and elems[j+1] < elems[j]:
                j += 1
            if e < elems[j]:
                break
            elems[i] = elems[j]
            i, j = j, 2*j+1
        elems[i] = e

    def buildheap(self):
        end = len(self._elems)
        for i in range(end//2, -1, -1):
            self.siftdown(self._elems[i], i, end)


class GraphError(ValueError):
    pass


class GraphAL:
    def __init__(self, mat=[], unconn=inf):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise GraphError("Argument for 'GraphAL'.")
        self._mat = [self._out_edges(mat[i], unconn) for i in range(vnum)]
        self._vnum = vnum
        self._unconn = unconn

    def vertex_num(self):
        return self._vnum

    def _invalid(self, v):
        return 0 > v or v >= self._vnum

    def add_vertex(self):
        self._mat.append([])
        self._vnum += 1
        return self._vnum - 1

    def add_edge(self, vi, vj, val=1):
        if self._vnum == 0:
            raise GraphError("Cannot add edge to empty graph.")
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + ' or ' + str(vj) + " is not valid vertex.")
        row = self._mat[vi]
        i = 0
        while i < len(row):
            if row[i][0] == vj:
                self._mat[vi][i] = (vj, val)
                return
            if row[i][0] > vj:
                break
            i += 1
        self._mat[vi].insert(i, (vj, val))

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + ' or ' + str(vj) + " is not valid vertex.")
        for i, val in self._mat[vi]:
            if i == vj:
                return val
        return self._unconn

    def out_edges(self, vi):
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex.")
        return self._mat[vi]

    @staticmethod
    def _out_edges(row, unconn):
        edges = []
        for i in range(len(row)):
            if row[i] != unconn:
                edges.append((i, row[i]))
        return edges

    def __str__(self):
        return "[\n" + ",\n".join(map(str, self._mat)) + "\n]" + "\nUnconnected: " + str(self._unconn)


def dijkstra_paths(graph, v0):
    vnum = graph.vertex_num()
    assert 0 <= v0 < vnum
    paths = [None] * vnum
    count = 0
    cands = PrioQueue([(0, v0, v0)])
    while count < vnum and not cands.is_empty():
        plen, u, vmin = cands.dequeue()
        if paths[vmin]:
            continue
        paths[vmin] = (u, plen)
        for v, w in graph.out_edges(vmin):
            if not paths[v]:
                cands.enqueue((plen + w, vmin, v))
        count += 1
    return paths


def floyd_paths(graph):
    vnum = graph.vertex_num()
    a = [[graph.get_edge(i, j) for j in range(vnum)]
         for i in range(vnum)]
    nvertex = [[-1 if a[i][j] == inf else j
                for j in range(vnum)]
               for i in range(vnum)]
    for k in range(vnum):
        for i in range(vnum):
            for j in range(vnum):
                if a[i][j] > a[i][k] + a[k][j]:
                    a[i][j] = a[i][k] + a[k][j]
                    nvertex[i][j] = nvertex[i][k]
    return a, nvertex


def show_paths(mat, begin, end):
    graph = GraphAL(mat)  # 实例化graph
    pathstack = floyd_paths(graph)  # 计算出所有顶点间距离和最短路径上第一个顶点
    path = [begin]  # 将起点装入path中
    temp = begin  # temp是临时起点, 以起点作为第一个临时起点
    while pathstack[1][temp][end] != end:
        temp = pathstack[1][temp][end]
        path.append(temp)
    path.append(end)
    path_length = pathstack[0][begin][end]
    return path, path_length


def cal_path():
    pass


mat = (
    (0, inf, 6, 3, inf, inf, inf),
    (11, 0, 4, inf, inf, 7, inf),
    (inf, 3, 0, inf, 5, inf, inf),
    (inf, inf, inf, 0, 5, inf, inf),
    (inf, inf, inf, inf, 0, inf, 9),
    (inf, inf, inf, inf, inf, 0, 10),
    (inf, inf, inf, inf, inf, inf, 0)
)
# path1 = dijkstra_paths(graph, 2)
# path2 = floyd_paths(GraphAL(mat))
# print(path1)
# print(path2)
for i in range(len(mat)):
    for j in range(len(mat)):
        print(show_paths(mat, i, j))
