from agent import Agent
from environment import *


class GeneralNode:
    def __init__(self, heuristic=0, node_lis=None, alpha=-float('inf'), beta=float('inf'), parent=None,move=None,state=None):
        self.alpha = alpha
        self.beta = beta
        self.parent = parent
        self.move = move
        self.best = None
        self.heuristic = heuristic
        self.state = state
        self.children = []

def minimax_ab(node, depth):
    if depth == 0 or node is None:
        return node.heuristic

    maximizing_player = depth % 2 == 0
    if maximizing_player:
        best_value = -float('inf')
        children = env.get_legal_moves(node.state)
        for child in children:
            value = minimax_ab(child, depth-1, False)
            best_value = max(best_value, value)
            node.alpha = max(node.alpha, best_value)
            if node.beta <= node.alpha:
                break
        return best_value

    else:
        best_value = float('inf')
        children = env.get_legal_moves(node.state)
        for child in children:
            value = minimax_ab(child, depth-1, True)
            best_value = min(best_value, value)
            node.beta = min(node.beta, best_value)
            if node.beta <= node.alpha:
                break
        return best_value

class GeneralTree:
    def __init__(self, limit = 5, depth = 0, state = None):
        self.root = None
        self.limit = limit
        self.depth = depth
        self.state = state
        if state == None:
            raise EnvironmentError
    def populate_tree(self):
        self.root = self.populate_tree_recur()

    def populate_tree_recur(self):
        data = input("input value : ")
        if data == "":
            return ""
        node = GeneralNode(data)
        for move in env.
            child = self.populate_tree_recur()
            if child == "":
                break
            node.node_lis.append(child)
        return node

    def alpha_beta(self):
        if self.depth == self.limit:
            return None

    def alphabeta_root(self):
        under_root = []
        for x in env.get_legal_moves(self.state):
            under_root.append()

        return self.alpha_beta()

class MyAgent(Agent):
    def __init__(self):
        self.role = None
        self.play_clock = None
        self.my_turn = False
        self.width = 0
        self.height = 0
        self.env = None

    def get_best_move(self,limit=5):
        tree = GeneralTree(state=self.env.current_state,limit=limit)
        tree.alphabeta_root()
        return tree.root.best


    # start() is called once before you have to select the first action. Use it to initialize the agent.
    # role is either "white" or "black" and play_clock is the number of seconds after which nextAction must return.
    def start(self, role, width, height, play_clock):
        self.play_clock = play_clock
        self.role = role
        self.my_turn = role != 'white'
        # we will flip my_turn on every call to next_action, so we need to start with False in case
        #  our action is the first
        self.width = width
        self.height = height
        # TODO: add your own initialization code here
        self.env = Environment(width, height)

    def next_action(self, last_action):
        if last_action:
            if self.my_turn and self.role == 'white' or not self.my_turn and self.role != 'white':
                last_player = 'white'
            else:
                last_player = 'black'
            print("%s moved from %s to %s" % (last_player, str(last_action[0:2]), str(last_action[2:4])))
            self.env.move(self.env.current_state, last_action)
        else:
            print("first move!")

        # update turn (above that line it myTurn is still for the previous state)
        self.my_turn = not self.my_turn
        if self.my_turn:
            x1, y1, x2, y2 = self.get_best_move()
            return "(move " + " ".join(map(str, [x1, y1, x2, y2])) + ")"
            # send the move first, then update your own world
            # if the move is not legal the game player will give you a random move
        else:
            return "noop"

    # this method is called when the environment has reached a terminal state
    # override it to reset the agent
    def cleanup(self, last_move):
        print("cleanup called")
        return