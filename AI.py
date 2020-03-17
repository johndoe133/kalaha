from kalaha import Kalaha, Board, Player
import math

class AI():
    def __init__(self, board):
        self.boards = []
        self.players = [Player(1), Player(2)]
        self.node = Node(board)
    
    def find_best_move(self, board):
        moves = board.possible_moves(2)
        for move in moves:
            board_copy = Board()
            board_copy.board = board.board
            self.boards += [self.players[1].move(board_copy, move)]
        for board in self.boards:
            game_over = False
            while not game_over:
                for player in self.players:
                    if not board.game_over():
                        print("Turn of player", player.player_no)
                        pick = random
                        player.move(self.board, pick)
                        print('\n' * 2)
                    else:
                        self.announce_winner()
                        game_over = True
                        break

    def alpha_beta_search(self, board):
        self.node.value = self.max_value(board, -10000, 10000, self.node)
        
        # return pick corresponding to value

    def max_value(self, board, alpha, beta, node):
        if board.game_over():
            return self.utility(board)
        v = -100000
        for move in board.possible_moves(True):
            board_copy = Board()
            board_copy.board = board.board
            board_copy.board = self.players[2].move(board_copy,move) # make the move
            
            new_node = Node(board_copy)
            new.node.parent = node
            node.children.append(new_node)
            # child node now contain updated board
        for child_node in node.children:
            v = max(v, min_value(child_node.board, alpha, beta, child_node))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
            
    def min_value(self, board, alpha, beta, node):
        if board.game_over():
            return self.utility(board)
        v = 1000000
        for move in board.possible_moves(False):
            board_copy = Board()
            board_copy.board = board.board
            # make the move and make a new node with the result of that move
            board_copy.board = self.players[1].move(board_copy,move)
            new_node = Node(board_copy)
            new.node.parent = node
            node.children.append(new_node)
        for child_node in node.children:
            v = min(v, self.max_value(child_node.board. alpha, beta, child_node))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v 




    def utility(self, board):
        return board[6] - board[13]

class Node:
    def __init__(self, board):
        self.children = []
        self.parent = None
        self.value = None  # value in the state
        self.board = board # state of the board
        self.max = True    # is it max or min

kalaha = Kalaha()
kalaha.start_against_ai()   
