from queue import Queue
from functools import cmp_to_key

from distribution import Distribution
from constant import MAX_GROUP_SIZE


class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

class Node:
    def __init__(self, id, distribution):
        self.id = id
        self.distribution = distribution

class Solver:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def calc(self, best_mu, res, group_id, partition):
        dis_res = []
        for group in partition:
            group.sort(key=cmp_to_key(lambda x, y: self.nodes[x].mu - self.nodes[y].mu))
            now = None
            for u in group:
                foo = self.nodes[u].deepcopy()
                for edge in edges:
                    if edge.v == u and group_id[edge.u] >= group_id[u]:
                        foo = foo.add(Distribution.from_mu_sigma(edge.w, 0, edge.w * 2))

                foo = foo.div(NUM_TEAM
                if not now:
                    now = foo
                else:
                    now = now.max(foo)
            
            if len(dis_res) > 0:
                now = now.add(dis_res[-1])
            
            dis_res.append(now)
        
        if (dis_res[-1].mu > best_mu):
            best_mu = dis_res[-1].mu
            res = dis_res


    def dfs(self, best_mu, res, group_id, partition):
        if all(x > 0 for x in group_id):
            self.calc(best_mu, res, group_id, partition)
            return

        first = -1
        for i in range(len(self.nodes)):
            if group_id[i] > 0:
                continue
            if first == -1:
                first = i

            # create a new group
            if first == i:
                group_id[i] = len(partition)
                partition.append([])
                partition[-1].append(i)
                self.dfs(best_mu, res, group_id, partition)
                partition.pop()
                group_id[i] = 0

            # add to the last group
            if len(partition) > 0 and len(partition[-1]) < MAX_GROUP_SIZE and partition[-1][-1] < i:
                group_id[i] = len(partition) - 1 
                partition[-1].append(i)
                self.dfs(best_mu, res, group_id, partition)
                partition[-1].pop()
                group_id[i] = False

    # @return (partition, distribution)
    def solve():
        best_mu = -1e9
        res = None
        partition = []
        group_id = np.zeros(len(self.nodes), dtype=int)
        self.dfs(best_mu, res, group_id, partition)
        return res
