from kalaha import Board, Player
import math

class AI():
    def __init__(self):
        self.boards = []
        self.players = [Player(1), Player(2)]
    
    def find_best_move(self, board):
        moves = board.possible_moves(2)
        for move in moves:
            board_copy = Board()
            board_copy.board = board.board
            boards += [players[1].move(board_copy, move)]
        for board in boards:
            game_over = False
            while not game_over:
                for player in players:
                    if not board.game_over():
                        print("Turn of player", player.player_no)
                        pick = random
                        player.move(self.board, pick)
                        print('\n' * 2)
                    else:
                        self.announce_winner()
                        game_over = True
                        break
