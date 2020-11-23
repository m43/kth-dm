import random


class Triest:

    def __init__(self, fname, m):
        self.m = m
        self.fname = fname

    def base(self):
        return self.__reservoir_sampling(improved=False)

    def improved(self):
        return self.__reservoir_sampling(improved=True)

    def __reservoir_sampling(self, improved):
        self.t = 0
        self.global_counter = 0
        self.samples = []
        self.local_counters = dict()
        self.neighbourhoods = dict()

        with open(self.fname, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue

                edge = tuple(sorted([int(x) for x in (line.strip('\n')).split()]))
                self.t += 1

                # use reservoir sampling
                if improved:
                    self.__update_counter('+', edge, improved)
                if self.__reservoir_sample(edge, improved):
                    self.__add_sample(edge)  # add edge to samples
                    if not improved:
                        self.__update_counter('+', edge)  # update counters according to edge addition

        if improved:
            epsilon = 1
        else:
            epsilon = (self.t * (self.t - 1) * (self.t - 2)) / (self.m * (self.m - 1) * (self.m - 2))
            epsilon = max(1, epsilon)

        return {
            "m": self.m,
            "epsilon": epsilon,
            "global_counter": self.global_counter,
            "global_triangles": epsilon * self.global_counter
        }

    def __reservoir_sample(self, _, improved):
        # if reservoir not full we will add the edge, return true
        if self.t <= self.m:
            return True

        # if reservoir full, flip a coin to determine if we will replace a currently saved sample or not
        elif random.random() < self.m / self.t:
            removed_edge = self.__remove_random_sample()
            if not improved:
                self.__update_counter('-', removed_edge)  # update counters according to edge removal
            return True

        else:
            return False

    def __add_sample(self, edge):
        self.samples.append(edge)

        # manage neighbourhood hash table
        if edge[0] not in self.neighbourhoods:
            self.neighbourhoods[edge[0]] = set()
        if edge[1] not in self.neighbourhoods:
            self.neighbourhoods[edge[1]] = set()
        self.neighbourhoods[edge[0]].add(edge[1])
        self.neighbourhoods[edge[1]].add(edge[0])

    def __remove_random_sample(self):
        remove_id = random.randint(0, self.m - 1)
        removed_edge = self.samples[remove_id]
        self.samples[remove_id] = self.samples[-1]
        del self.samples[-1]

        self.neighbourhoods[removed_edge[0]].remove(removed_edge[1])
        if len(self.neighbourhoods[removed_edge[0]]) == 0:
            del self.neighbourhoods[removed_edge[0]]

        self.neighbourhoods[removed_edge[1]].remove(removed_edge[0])
        if len(self.neighbourhoods[removed_edge[1]]) == 0:
            del self.neighbourhoods[removed_edge[1]]

        return removed_edge

    def __update_counter(self, action, edge, improved=False):
        u = edge[0]
        v = edge[1]

        # if one of the vertices is no longer in the sample (they have no edges and thus no neighbours) just exit
        if not (u in self.neighbourhoods and v in self.neighbourhoods):
            return

        shared_neighbourhood = self.neighbourhoods[u].intersection(self.neighbourhoods[v])

        for shared_neighbour in shared_neighbourhood:
            if action == '+':
                if improved:
                    value = max(1, ((self.t - 1) * (self.t - 2)) / (self.m * (self.m - 1)))
                else:
                    value = 1
                self.global_counter += value
                self.__increase_count(shared_neighbour, value)
                self.__increase_count(u, value)
                self.__increase_count(v, value)
            elif action == '-':
                self.global_counter -= 1
                self.__decrease_count(shared_neighbour)
                self.__decrease_count(u)
                self.__decrease_count(v)
            else:
                raise RuntimeError(f'Action {action} is not a defined action, must be \'-\' or \'+\'!')

    def __increase_count(self, vertex, value):
        if vertex not in self.local_counters:
            self.local_counters[vertex] = 0
        self.local_counters[vertex] += value

    def __decrease_count(self, vertex):
        self.local_counters[vertex] -= 1
        if self.local_counters[vertex] == 0:
            del self.local_counters[vertex]
