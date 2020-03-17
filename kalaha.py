class Board:
    opposite_pit = dict()
    for i in range(6):
        opposite_pit[i] = 12-i
    for i in range(7, 13):
        opposite_pit[i] = 12-i
    def __init__(self):
        self.state = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        

    @staticmethod
    def game_over(state):
        '''
        Checks if the game is over
        '''
        if (sum(state[0:6]) == 0 or (sum(state[7:13]) == 0)):
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
            print(f'{self.state[-i]:^5}', end='')
        print('\n\n     ', end='')
        for i in range(0, 7):
            print(f'{self.state[i]:^5}', end='')
        print('')
        print("-"*40)
        print(p1, end='')
        for i in range(1, 7):
            print(f'{i:^5}', end='')
        print("")

    def result(self, state, action, player):
        switch_turns = True
        if player.player_no == 1:
            # Pick up the beans
            beans = state[action]
            state[action] = 0
            pit_no = action
            # Distribute them
            while beans > 0:
                pit_no = (pit_no + 1) % 13
                # doesn't get into player 2s kalaha
                state[pit_no] += 1
                beans -= 1
            # if you land in your own empty 'thing' you get that into the kalaha
            # plus the pieces directly opposite
            if player.can_capture(state, pit_no):
                player.capture(state, pit_no)
        else:
            action = action + 7
            beans = state[action]
            state[action] = 0
            pit_no = action
            while beans > 0:
                pit_no = (pit_no + 1) % 14
                if pit_no == 6:
                    pit_no += 1  # skip player 1s kalaha
                state[pit_no] += 1
                beans -= 1
            if player.can_capture(state, pit_no):
                player.capture(state, pit_no)

        if (not Board.game_over(state)):
            if player.player_no == 1:
                if pit_no == 6:
                    switch_turns = False
            else:
                if pit_no == 13:
                    switch_turns = False
        return state, switch_turns

    def check_winner(self, state):
        '''
        Checks who the winner is

        Returns
        -------
        winner : int, score : int

        `winner` is the player number, `score` is the score of the winner. 
        If `winner==3` then it was a draw

        '''
        player_1_score = sum(state[0:7])
        player_2_score = sum(state[7:14])
        score = player_1_score
        if player_1_score > player_2_score:
            winner = 1
        elif player_2_score > player_1_score:
            winner = 2
            score = player_2_score
        else:
            winner = 3  # draw
        return winner, score

    def possible_actions(self, state, player1):
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
            if (state[i] != 0):
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
        state, switch_turns = board.result(board.state, pick, self)
        board.board = state
        print("\n")
        board.print_board(0)
        print("\n")
        return state, switch_turns

    
    def can_capture(self, state, last_pit):
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
        if (state[last_pit] == 1 and (last_pit not in [6, 13])):
            if self.player_no == 1 and last_pit in range(0, 6) or (self.player_no == 2 and last_pit in range(7, 13)):
                return True
        else:
            return False

    def capture(self, state, pit_no):
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
            state[pit_no] = 0
            state[6] += 1
            opposite_pitIndex = Board.opposite_pit[pit_no]
            opposite_pit = state[opposite_pitIndex]
            state[opposite_pitIndex] = 0
            state[6] += opposite_pit

        elif self.player_no == 2:
            state[pit_no] = 0
            state[13] += 1
            opposite_pitIndex = Board.opposite_pit[pit_no]
            opposite_pit = state[opposite_pitIndex]
            state[opposite_pitIndex] = 0
            state[13] += opposite_pit

class Kalaha():
    def __init__(self):
        self.board = Board()
        self.players = [Player(1),Player(2)]
        self.player_1 = Player(1)
        self.player_2 = Player(2)

    def announce_winner(self):
        winner, score = self.board.check_winner(self.board.state)
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
                if not self.board.game_over(self.board.state):
                    switch_turns = False
                    while not switch_turns:
                        print("Turn of player", player.player_no)
                        pick = self.player_input(player.player_no)
                        s, switch_turns = player.move(self.board, pick)
                        print('\n' * 2)
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
                        if self.board.state[pick] != 0:
                            break
                    elif player == 2:
                        if self.board.state[pick + 7] != 0:
                            break
                print("Pick a proper slot")
            except:
                print("Input a number you donut")
        return pick

if __name__ == '__main__':
    kalaha = Kalaha()
    kalaha.start()

