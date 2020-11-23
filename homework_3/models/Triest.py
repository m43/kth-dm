import numpy as np
import random


class Triest:

    def __init__(self, fname, m):
        self.m = m
        self.fname = fname
        self.t = 0
        self.samples = set()
        self.global_counter = 0
        self.local_counters = dict()
        self.neighbourhoods = dict()

    def base(self):
        self.__reservoir_sampling(improved=False)

    def improved(self):
        self.__reservoir_sampling(improved=True)

    def __reservoir_sampling(self, improved):
        # open I/O stream
        with open(self.fname, 'r') as f:
            # go through stream and do reservoir sampling
            counter = 0
            for line in f:
                # ignore comments
                if line.startswith('#'):
                    continue

                # get edge vertices (sort to handle directed graphs and/or multiple addition of same edges)
                edge = tuple(sorted([int(x) for x in (line.strip('\n')).split()]))

                # increment time
                self.t += 1

                # use reservoir sampling
                if improved:
                    self.__update_counter('+', edge, improved)
                if self.__reservoir_sample(edge, improved):
                    self.__add_sample(edge)  # add edge to samples
                    if not improved:
                        self.__update_counter('+', edge)  # update counters according to edge addition

        # TODO: remove later
        # prints global triangle estimation
        epsilon = (self.t * (self.t - 1) * (self.t - 2)) / (self.m * (self.m - 1) * (self.m - 2))
        if epsilon < 1:
            epsilon = 1
        print(f'Global triangles estimate using m={self.m} is equal to {epsilon * self.global_counter}')

    def __reservoir_sample(self, edge, improved):
        # if reservoir not full we will add the edge, return true
        if self.t <= self.m:
            return True

        # if reservoir full, flip a coin to determine if we will replace a currently saved sample or not
        elif np.random.binomial(n=1, p=self.m / self.t, size=1)[0] == 1:
            removed_edge = self.__remove_random_sample()
            if not improved:
                self.__update_counter('-', removed_edge)  # update counters according to edge removal
            return True

        else:
            return False

    def __add_sample(self, edge):
        self.samples.add(edge)

        # manage neighbourhood hash table
        if edge[0] not in self.neighbourhoods:
            self.neighbourhoods[edge[0]] = set()
        if edge[1] not in self.neighbourhoods:
            self.neighbourhoods[edge[1]] = set()
        self.neighbourhoods[edge[0]].add(edge[1])
        self.neighbourhoods[edge[1]].add(edge[0])

    def __remove_random_sample(self):
        removed_edge = random.sample(self.samples, 1)[0]  # pick a random old sample and remember it
        self.samples.remove(removed_edge)  # remove the randomly picked old sample

        # manage neighbourhood hash table
        self.neighbourhoods[removed_edge[0]].remove(removed_edge[1])
        if len(self.neighbourhoods[removed_edge[0]]) == 0:
            del self.neighbourhoods[removed_edge[0]]
        self.neighbourhoods[removed_edge[1]].remove(removed_edge[0])
        if len(self.neighbourhoods[removed_edge[1]]) == 0:
            del self.neighbourhoods[removed_edge[1]]

        return removed_edge

    def __update_counter(self, action, edge, improved=False):
        # get vertices from edge
        u = edge[0]
        v = edge[1]

        # if one the vertices i no longer in the graph (they have no edges and thus no neighbours) just exit
        if not (u in self.neighbourhoods and v in self.neighbourhoods):
            return

        # get their shared neighbours
        shared_neighbourhood = self.neighbourhoods[u].intersection(self.neighbourhoods[v])

        # update counters according to the action
        for shared_neighbour in shared_neighbourhood:
            if action == '+':
                self.global_counter += 1
                self.__increase_count(shared_neighbour, improved)
                self.__increase_count(u, improved)
                self.__increase_count(v, improved)

            elif action == '-':
                self.global_counter -= 1
                self.__decrease_count(shared_neighbour)
                self.__decrease_count(u)
                self.__decrease_count(v)
            else:
                raise RuntimeError(f'Action {action} is not a defined action, must be \'-\' or \'+\'!')

    def __increase_count(self, vertex, weighted=False):
        eta = max(1, ((self.t - 1) * (self.t - 2)) / (self.m * (self.m - 1)))

        if vertex in self.local_counters:
            self.local_counters[vertex] += 1 if not weighted else eta
        else:
            self.local_counters[vertex] = 1 if not weighted else eta

    def __decrease_count(self, vertex):
        if vertex in self.local_counters:
            self.local_counters[vertex] -= 1
            if self.local_counters[vertex] == 0:
                del self.local_counters[vertex]
