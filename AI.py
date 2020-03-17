from kalaha import Kalaha, Board, Player
import math

class AI():
    def __init__(self, board):
        self.boards = []
        self.players = [Player(1), Player(2)]
        

    def alpha_beta_search(self, board):
        self.root.value = self.max_value(board, -10000, 10000)

    def max_value(self, board, alpha, beta):
        if board.game_over():
            return self.utility(board)
        v = -1000
        for action in board.possible_moves():
            v = max(v, min_value(self.players[1].result(board, action), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
            
    def min_value(self, board, alpha, beta):
        if board.game_over():
            return self.utility(board)
        v = 1000
        for action in board.possible_moves():
            v = min(v, max_value(self.players[1].result(board, action), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
            
    def utility(self, board):
        return board[13] - board[6]

"""
class Node:
    def __init__(self, board, parent):
        self.children = []
        self.previous_pick = None
        self.parent = parent
        self.value = None  # value in the state
        self.board = board # state of the board
        self.max = True    # is it max or min
"""     

kalaha = Kalaha()
kalaha.start_against_ai()   
