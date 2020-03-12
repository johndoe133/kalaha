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

    def start(self):
        '''
        Starts the kalaha game. Ends when one player wins.
        '''
        game_over = False
        while not game_over:
            for player in self.players:
                if not self.board.game_over():
                    print("Turn of player", player.player_no)
                    pick = self.player_input(player.player_no)
                    player.move(self.board, pick)
                    print('\n' * 2)
                else:
                    winner, score = self.board.check_winner()
                    print("GAME OVER!")
                    if winner == 3:
                        print("The game was a draw")
                        self.board.print_board(0)
                    else:
                        print("The winner is Player", winner, " with score", score)
                        self.board.print_board(winner)
                    game_over = True
                    break
        

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
            except:
                print("Input a number you donut")
        return pick

if __name__ == '__main__':
    kalaha = Kalaha()
    kalaha.start()

