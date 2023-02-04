import collections
import heapq
import math
Node = collections.namedtuple('Node', ['value', 'parent', 'state', 'action','g_score'])


class Heuristics:
    env = None

    # inform the heuristics about the environment, needs to be called before the first call to eval()
    def init(self, env):
        self.env = env

    # return an estimate of the remaining cost of reaching a goal state from state s
    def eval(self, s):
        pass


class SimpleHeuristics(Heuristics):

    def eval(self, s):
        h = 0
        # if there is dirt: max of { manhattan distance to dirt + manhattan distance from dirt to home }
        # else manhattan distance to home
        if len(s.dirts) == 0:
            h = self.nb_steps(s.position, self.env.home)
        else:
            for d in s.dirts:
                steps = self.nb_steps(s.position, d) + self.nb_steps(d, self.env.home)
                if (steps > h):
                    h = steps
            h += len(s.dirts)  # sucking up all the dirt
        if s.turned_on:
            h += 1  # to turn off
        return h

    # estimates the number of steps between locations a and b by Manhattan distance
    def nb_steps(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

class CustomHeuristics(Heuristics):
    def eval(self, s):
        h = 0
        multiply = 0
        # if there is dirt: max of { manhattan distance to dirt + manhattan distance from dirt to home }
        # else manhattan distance to home
        if len(s.dirts) == 0:
            h = self.nb_steps(s.position, self.env.home)
        else:
            for d in s.dirts:
                todirt = self.nb_steps(s.position, d)
                steps = todirt + self.nb_steps(d, self.env.home)
                if (steps > h):
                    h = steps
                for dirts in s.dirts:
                    dirtsteps = self.nb_steps(dirts, d)
                    # this does not run, but I tried to make a heuristic incorperating dirt grouping. So it will
                    if self.env.width < 10 and self.env.height < 10 or dirtsteps > 10:
                        if dirtsteps <= 10:
                            h += 1
                        if dirtsteps <= 5:
                            h += 1
                    else:
                        if dirtsteps <= 2:
                            h += 1
                        if dirtsteps <= 1:
                            h += 1
            h += len(s.dirts)  # sucking up all the dirt
        if s.turned_on:
            h += 1  # to turn off
        return h

    # estimates the number of steps between locations a and b by Manhattan distance
    def nb_steps(self, a, b):
        return math.sqrt(math.pow(a[0] - b[0],2) + math.pow(a[1] - b[1],2))


######################

class SearchAlgorithm:
    heuristics = None

    def __init__(self, heuristics):
        self.heuristics = heuristics

    # searches for a goal state in the given environment, starting in the current state of the environment,
    # stores the resulting plan and keeps track of nb. of node expansions, max. size of the frontier and cost of best solution found 
    def do_search(self, env):
        pass

    # returns the plan found, the last time do_search() was executed
    def get_plan(self):
        pass

    # returns the number of node expansions of the last search that was executed
    def get_nb_node_expansions(self):
        pass

    # returns the maximal size of the frontier of the last search that was executed
    def get_max_frontier_size(self):
        pass

    # returns the cost of the plan that was found
    def get_plan_cost(self):
        pass


class AStarSearch(SearchAlgorithm):
    nb_node_expansions = 0
    max_frontier_size = 0
    visitedspaces = 0
    goal_node = None

    def __init__(self, heuristic):
        super().__init__(heuristic)

    def do_search(self, env):
        self.heuristics.init(env)
        self.nb_node_expansions = 0
        self.max_frontier_size = 0
        self.goal_node = None
        # Node = collections.namedtuple('Node', ['value', 'parent', 'state', 'action', 'g_score'])
        rootState = env.current_state
        rootHeuristic = self.heuristics.eval(rootState)
        root_node = Node(rootHeuristic, None, rootState, None, 0)

        open_heap = []
        heapq.heapify(open_heap)

        open_map = {root_node.state: root_node}
        closed_map = {}

        heapq.heappush(open_heap, root_node)

        while len(open_heap) > 0:
            # start by picking the best state available from the heapqueue
            currentNode = heapq.heappop(open_heap)
            open_map.pop(currentNode.state)
            closed_map[currentNode.state] = currentNode

            if env.is_goal_state(currentNode.state):
                self.goal_node = currentNode
                break

            legal_actions = env.get_legal_actions(currentNode.state)

            for actionnow in legal_actions:
                statenow = env.get_next_state(currentNode.state, actionnow)
                if statenow in closed_map:
                    continue

                parentnow = currentNode
                g = parentnow.g_score + env.get_cost(statenow, actionnow)
                valuenow = self.heuristics.eval(statenow) + g

                in_open_map = statenow in open_map

                turn_off_and_on_for_question_8 = False

                if in_open_map and turn_off_and_on_for_question_8:
                    if_its_less = g < open_map[statenow].g_score
                    if if_its_less:
                        newNode = Node(valuenow, parentnow, statenow, actionnow, g)
                        # replaces old state with a new node
                        open_map[statenow] = newNode

                        # update the heap, so it will agree with the open_map
                        open_heap.remove(statenow)
                        heapq.heapify(open_heap)
                        heapq.heappush(open_heap, newNode)
                        self.nb_node_expansions += 1
                else:
                    newNode = Node(valuenow, parentnow, statenow, actionnow, g)

                    # add the node to the heap and map
                    open_map[statenow] = newNode
                    heapq.heappush(open_heap, newNode)
                    self.nb_node_expansions += 1

                # end of for
                self.max_frontier_size = max(len(open_map), self.get_max_frontier_size())
            # end of while
            if len(open_heap) == 0:
                return False

    def get_plan(self):
        if not self.goal_node:
            return None

        plan = ["TURN_ON"]
        n = self.goal_node
        while n.parent:
            plan.append(n.action)
            n = n.parent
        return plan[::-1]

    def get_nb_node_expansions(self):
        return self.nb_node_expansions

    def get_max_frontier_size(self):
        return self.max_frontier_size

    def get_plan_cost(self):
        if self.goal_node:
            return self.goal_node.value
        else:
            return 0