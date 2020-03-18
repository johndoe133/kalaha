class Board:
    def __init__(self):
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.opposite_pit = dict()
        for i in range(6):
            self.opposite_pit[i] = 12-i
        for i in range(7, 13):
            self.opposite_pit[i] = 12-i

    def game_over(self):
        '''
        Checks if the game is over
        '''
        if (sum(self.board[0:6]) == 0 or (sum(self.board[7:13]) == 0)):
            return True
        else:
            return False

    def print_board(self, player):
        '''
        Prints the board. 

        Parameters
        ----------
        player : int
            
        Indicate which player it is. If you wish to display game state, set `player=0`
        '''
        p1 = '     '
        p2 = '     '
        if player == 1:
            p1 = ' --> '
        elif player == 2:
            p2 = ' --> '
        elif player != 0:
            raise Exception('Invalid player number')
        print(p2, end='')
        for i in range(6, 0, -1):
            print(f'{i:^5}', end='')
        print('')
        print("-"*40)
        for i in range(1, 8):
            print(f'{self.board[-i]:^5}', end='')
        print('\n\n     ', end='')
        for i in range(0, 7):
            print(f'{self.board[i]:^5}', end='')
        print('')
        print("-"*40)
        print(p1, end='')
        for i in range(1, 7):
            print(f'{i:^5}', end='')
        print("")

    def check_winner(self):
        '''
        Checks who the winner is

        Returns
        -------
        winner : int, score : int

        `winner` is the player number, `score` is the score of the winner. 
        If `winner==3` then it was a draw

        '''
        player_1_score = sum(self.board[0:7])
        player_2_score = sum(self.board[7:14])
        score = player_1_score
        if player_1_score > player_2_score:
            winner = 1
        elif player_2_score > player_1_score:
            winner = 2
            score = player_2_score
        else:
            winner = 3  # draw
        return winner, score

    def possible_moves(self, player1):
        """
        Finds the possible picks for player_no
        """
        moves = []
        #if player_no == 2
        a=7
        b=13
        if (player1):
            a = 0
            b=6
        
        for i in range(a,b):
            if (self.board[i] != 0):
                moves += [i]
        return moves

class Player:
    def __init__(self, player_no):
        self.player_no = player_no
        self.score = 0

    def move(self, board, pick):
        """
        Moves the pieces according to player selection

        Parameters
        ----------
        board : Board 

        The board the player is currently playing on

        pick : int
        
        The pit the player has picked
        """
        if self.player_no == 1:
            # Pick up the beans
            beans = board.board[pick]
            board.board[pick] = 0
            pit_no = pick
            # Distribute them
            while beans > 0:
                pit_no = (pit_no + 1) % 13
                # doesnt get into player 2s kalaha
                board.board[pit_no] += 1
                beans -= 1
            # if you land in your own empty 'thing' you get that into the kalaha
            # plus the pieces directly opposite
            if self.can_capture(board, pit_no):
                self.capture(board, pit_no)
        else:
            pick = pick + 7
            beans = board.board[pick]
            board.board[pick] = 0
            pit_no = pick
            while beans > 0:
                pit_no = (pit_no + 1) % 14
                if pit_no == 6:
                    pit_no += 1  # skip player 1s kalaha
                board.board[pit_no] += 1
                beans -= 1
            if self.can_capture(board, pit_no):
                self.capture(board, pit_no)
        print("\n")
        board.print_board(0)
        print("\n")
        return board

        

        # if it ends in kalaha
        if (not board.game_over()):
            if self.player_no == 1:
                if pit_no == 6:
                    pick = kalaha.player_input(1)
                    self.move(board, pick)
            else:
                if pit_no == 13:
                    pick = kalaha.player_input(2)
                    self.move(board, pick)

    
    def can_capture(self, board, last_pit):
        """Checks if the player can capture the beans on the opposite side

        This assumes that you have just placed your last bean in the pit you
        wish to check for

        Parameters
        ----------
        board : Board

            The current board being played on

        last_pit : int
            the last pit a bean is being placed in
        """
        if (board.board[last_pit] == 1 and (last_pit not in [6, 13])):
            if self.player_no == 1 and last_pit in range(0, 6) or (self.player_no == 2 and last_pit in range(7, 13)):
                return True
        else:
            return False

    def capture(self, board, pit_no):
        """
        Captures the player's last piece placed, as well as the pieces opposite

        This assumes that capturing can be done

        Parameters
        ----------
        board : Board

        The board the player is currently using

        pit_no : int

        The pit the player is placing their last bean in
        """
        if self.player_no == 1:
            board.board[pit_no] = 0
            board.board[6] += 1
            opposite_pitIndex = board.opposite_pit[pit_no]
            opposite_pit = board.board[opposite_pitIndex]
            board.board[opposite_pitIndex] = 0
            board.board[6] += opposite_pit

        elif self.player_no == 2:
            board.board[pit_no] = 0
            board.board[13] += 1
            opposite_pitIndex = board.opposite_pit[pit_no]
            opposite_pit = board.board[opposite_pitIndex]
            board.board[opposite_pitIndex] = 0
            board.board[13] += opposite_pit

class Kalaha():
    def __init__(self):
        self.board = Board()
        self.players = [Player(1),Player(2)]
        self.player_1 = Player(1)
        self.player_2 = Player(2)

    def announce_winner(self):
        winner, score = self.board.check_winner()
        print("GAME OVER!")
        if winner == 3:
            print("The game was a draw")
            self.board.print_board(0)
        else:
            print("The winner is Player", winner, " with score", score)
            self.board.print_board(winner)


    def start(self):
        '''
        Starts the kalaha game. Ends when one player wins.
        '''
        game_over = False
        while not game_over:
            for player in self.players:
<<<<<<< Updated upstream
                if not self.board.game_over():
                    print("Turn of player", player.player_no)
                    pick = self.player_input(player.player_no)
                    player.move(self.board, pick)
                    print('\n' * 2)
=======
                if not self.board.game_over(self.board.state):
                    switch_turns = False
                    while not switch_turns:
                        print("Turn of player", player.player_no)
                        if (player.player_no == 2):
                            ai = AI(self.players, self.board.state)
                            state_copy = self.board.state[:]
                            print("Best v:", ai.alpha_beta_search(state_copy))
                            print("")
                        pick = self.player_input(player.player_no)
                        s, switch_turns = player.move(self.board, pick)
                        print('\n' * 2)
>>>>>>> Stashed changes
                else:
                    self.announce_winner()
                    game_over = True
                    break

    def start_against_ai(self):
        '''
        Starts the kalaha game. Ends when one player wins.
        '''
        ai = ai()
        game_over = False
        while not game_over:
            ### player 1 turn
            for player in self.players[0:1]:
                if not self.board.game_over():
                    print("Turn of player", player.player_no)
                    pick = self.player_input(player.player_no)
                    player.move(self.board, pick)
                    print('\n' * 2)
                else:
                    self.announce_winner()
                    break

            ### player AI turn
            pick = AI.find_best_move(self.board)
            player[1].move(self.board, pick)

        

    def player_input(self, player):
        '''
        Gets a 'pit' picked by a player. 
        Parameters
        ----------
        player : int
                 Player number. Must be 1 or 2.
        
        Returns
        -------
        The 'hole' number picked by the player.
        '''
        self.board.print_board(player)

        while True:
            try:
                pick = int(input("Pick a slot: "))
                pick = pick - 1
                if pick in [0, 1, 2, 3, 4, 5]:
                    if player == 1:
                        if self.board.board[pick] != 0:
                            break
                    elif player == 2:
                        if self.board.board[pick + 7] != 0:
                            break
                print("Pick a proper slot")
            except ValueError:
                print("Input a number you donut")
        return pick

<<<<<<< Updated upstream
=======
    def start_against_ai(self):
        '''
        Starts the kalaha game. Ends when one player wins.
        '''
        ai = AI()
        game_over = False
        while not game_over:
            ### player 1 turn
            
            if not self.board.game_over():
                print("Turn of player", self.players[0].player_no)
                pick = self.player_input(self.players[0].player_no)
                self.players[0].move(self.board, pick)
                print('\n' * 2)
            else:
                self.announce_winner()
                break

            ### player AI turn
            pick = ai.find_best_move(self.board)
            self.players[1].move(self.board, pick)



class AI():
    def __init__(self, players,state):
        self.players = players
        self.best_action = None
        self.tree = Node(state[:], True)

    
    def alpha_beta_search(self, state): # the AI is maximizing
        print("State",state)
        v = self.max_value(state, -100, 100, 1)
        return v

    def max_value(self, state, alpha, beta, depth):
        if (Board.game_over(state) or depth == 0):
            return self.utility(state)
        v = -100
        print("possible actions max",Board.possible_actions(state, False))
        
        for action in Board.possible_actions(state, False)[:]:
            print("action", action)
            s, switch_turns = Board.result(state, action, self.players[1])
            print("switch_turns:",switch_turns)
            result_state = s[:]
            if (switch_turns):
                v = max(v, self.min_value(result_state, alpha, beta, depth-1))
                if v >= beta:
                    print("vbeta1:",v,"\n")
                    return v
                alpha = max(alpha, v)
            else:
                v = max(v, self.max_value(result_state, alpha, 100, depth))
                if v <= alpha:
                    print("vbeta2:",v,"\n")
                    return v
                beta = min(beta, v)
        print("v:",v,"\n")
        return v

    def min_value(self, state, alpha, beta, depth):
        if (Board.game_over(state) or depth==0):
            return self.utility(state)
        v = 100
        for action in Board.possible_actions(state, True)[:]:
            s, switch_turns = Board.result(state, action, self.players[0])
            result_state = s[:]
            if (switch_turns):
                v = min(v, self.max_value(result_state, alpha, beta, depth-1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            else:
                v = min(v, self.min_value(result_state, -100, beta, depth))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        return v



    def utility(self, state):
        return state[13]-state[6]

class Node():
    def __init__(self, state, maximizing_player):
        self.children = []
        self.action = None # How you got here
        self.state = state
        self.value = None
        self.player = maximizing_player # player class
        self.alpha = None
        self.beta = None

    # def expand(self):
    #     for action in Board.possible_actions(state, player.player_no==1):


>>>>>>> Stashed changes
if __name__ == '__main__':
    kalaha = Kalaha()
    kalaha.start()

