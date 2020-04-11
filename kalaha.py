import operator
import time
from heapq import nlargest
import random

class Board:
    opposite_pit = dict()
    for i in range(6):
        opposite_pit[i] = 12-i
    for i in range(7, 13):
        opposite_pit[i] = 12-i
    def __init__(self):
        self.state = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0] # state of the initial board
        

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
        l = "|"
        if player == 1:
            p1 = ' --> '
        elif player == 2:
            p2 = ' --> '
        elif player != 0:
            raise Exception('Invalid player number')
        print(p2, end='')
        for i in range(6, 0, -1):
            print(" " + str(i) + "  " , end='')
        print('')
        print("+" + "---+"*8)
        print(l+" "*3+l,end="")
        for i in range(2, 8):
            print(f'{self.state[-i]:>2} {l:<1}', end='')
        print('   |')
        print(f"|{self.state[13]:^3}|" + "---+"*5 + f'---|{self.state[6]:^3}|')
        print('|   |', end='')
        for i in range(0, 6):
            print(f'{self.state[i]:>2} {l:<1}', end='')
        print('   |')
        print("+" + "---+"*8)
        print(p1, end='')
        for i in range(1, 7):
            print(f'{i:^4}', end='')
        print("")

    @staticmethod
    def result(state, action, player):
        '''
        Static method. Returns the resulting board/state of making a move/action

        Parameters
        ----------
        state: list
        
        a list representing a board state

        action: int
        
        the number of the pit the player has chosen

        player: Player

        Returns
        ----------
        state: list
        
        the resulting state of the action

        switch_turns: bool
        
        true if it is still the same players turn
        '''
        state = state[:]
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

    @staticmethod
    def possible_actions(state, player1):
        """
        Finds the possible picks/actions for player.
        """
        moves = []
        start_index=7
        end_index=13
        if (player1):
            start_index = 0
            end_index=6
        
        for i in range(start_index,end_index):
            if (state[i] != 0):
                moves += [i - start_index]
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
        board.state = state
        
        if __name__ == '__main__': # so it doesnt print in simulations
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

    def reset_board(self):
        self.board.state = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    def announce_winner(self):
        winner, score = self.board.check_winner(self.board.state)
        print("GAME OVER!")
        if winner == 3:
            print("The game was a draw")
            self.board.print_board(0)
        else:
            print("The winner is Player", winner, " with score", score)
            self.board.print_board(winner)
        

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
            except ValueError:
                print("Input a number you donut")
        return pick



    def play_against_human(self):
        '''
        Starts the kalaha game 1v1. Ends when one player wins.
        '''
        game_over = False
        while not game_over:
            for player in self.players:
                if not self.board.game_over(self.board.state):
                    switch_turns = False
                    while not switch_turns:
                        print("Turn of player", player.player_no,"\n")
                        # if (player.player_no == 2):
                        #     ai = AI(self.players)
                        #     state_copy = self.board.state[:]
                        #     print("Best action:", ai.alpha_beta_search(state_copy))
                        #     print("")
                        pick = self.player_input(player.player_no)
                        s, switch_turns = player.move(self.board, pick)
                        print('\n' * 2)
                else:
                    self.announce_winner()
                    game_over = True
                    break

    def play_against_ai(self, d, AI_player = 2):
        '''
        Starts the kalaha game vs AI. Ends when one player wins.
        '''
        ai = AI(self.players)
        
        game_over = False
        while not game_over:
            for player in self.players:
                if not self.board.game_over(self.board.state):
                    switch_turns = False
                    while not switch_turns:
                        # AIs turn
                        if (player.player_no == AI_player):
                            print("AI's turn")
                            state_copy = self.board.state[:]   
                            print("AI thinking...")       
                            best_move = ai.alpha_beta_search(state_copy, depth = d, maximizing_player = 1 if AI_player == 2 else 0)
                            print("AI picks",best_move)
                            s, switch_turns = player.move(self.board, best_move-1)
                        else:
                            print("Turn of player", player.player_no,"\n")
                            pick = self.player_input(player.player_no)
                            s, switch_turns = player.move(self.board, pick)
                        print('\n' * 2)
                else:
                    self.announce_winner()
                    game_over = True
                    break

    def ai_against_ai(self, depth_p1, depth_p2):
        
        ai = AI(self.players)

        game_over = False
        while not game_over:
            for player in self.players:
                if not self.board.game_over(self.board.state):
                    switch_turns = False
                    while not switch_turns:
                        if player.player_no == 1:
                            #print("AI 1's turn")
                            state_copy = self.board.state[:]   
                            #print("AI thinking...")                         
                            best_move = ai.alpha_beta_search(state_copy, maximizing_player = 0, depth=depth_p1)
                            #print("AI picks",best_move)
                            s, switch_turns = player.move(self.board, best_move-1)
                        else:
                            #print("AI 2's turn")
                            state_copy = self.board.state[:]
                            #print("AI thinking...")
                            best_move = ai.alpha_beta_search(state_copy, maximizing_player = 1, depth = depth_p2)
                            #print("AI picks",best_move)
                            s, switch_turns = player.move(self.board, best_move-1)
                else:
                    if __name__ == '__main__': # so it does not show in simulations
                        self.announce_winner()
                    game_over = True
                    return self.board.check_winner(self.board.state)
                    break


    def display_menu(self):
        options = ["Play against AI", "Play against another player", "Exit"]
        for i in range(len(options)):
            print(f"{i+1}. {options[i]}")
        choice = 0
        while (choice not in [1,2,3]):
            while True:
                try:
                    choice = float(input("Enter a menu number: "))
                    break
                except ValueError:
                    print("Please enter a valid number: ")
        return choice

    def ai_menu(self):
        options = ["Easy", "Medium", "Hard"]
        print("Choose a level of difficulty")
        for i in range(len(options)):
            print(f"{i+1}. {options[i]}")
        choice = 0
        while (choice not in [1,2,3]):
            while True:
                try:
                    choice = float(input("Enter a menu number: "))
                    break
                except ValueError:
                    print("Please enter a valid number: ")
        return choice
    
    def AI_plays_as(self):
        options = ["Play as player 1", "Play as player 2"]
        print("\nChoose to play as player 1 or 2")
        for i in range(len(options)):
            print(f"{i+1}. {options[i]}")
        choice = 0
        while (choice not in [1,2]):
            while True:
                try:
                    choice = float(input("Enter a menu number: "))
                    break
                except ValueError:
                    print("Please enter a valid number: ")
        return 1 if choice == 2 else 2

class AI():
    def __init__(self, players):
        self.players = players
        self.action_score = dict()
        self.maximizing_player = None
        self.minimizing_player = None
   
    def alpha_beta_search(self, state, maximizing_player = 1, depth = 3): # the AI is maximizing
        '''
        The alpha beta pruning search algorithm for finding the best move

        Parameters
        ---------
        state: list

        '''
        self.action_score = dict() # dictionary of actions and corresponding score
        
        self.maximizing_player = maximizing_player
        self.minimizing_player = 0 if self.maximizing_player == 1 else 1
        actions = Board.possible_actions(state, True if self.maximizing_player == 0 else False)
        if len(actions) == 1:
            return actions[0] + 1 # if only one action is available AI picks it
        for action in actions:
            s, switch_turns = Board.result(state, action, self.players[self.maximizing_player])
            result_state = s[:] # copy of resulting board state of making that action
            if switch_turns:
                v = self.min_value(result_state,-100,100,depth-1)
            else: # if it is still the AI's turn it will keep maximizing
                v = self.max_value(result_state,-100,100,depth)
            d = {action+1: v}
            self.action_score.update(d)
        return self.pick_best_move()

    def max_value(self, state, alpha, beta, depth):
        if (Board.game_over(state) or depth == 0):
            return self.utility(state)
        v = -100
        for action in Board.possible_actions(state, True if self.maximizing_player == 0 else False):
            s, switch_turns = Board.result(state, action, self.players[self.maximizing_player])
            result_state = s[:]
            if (switch_turns):
                v = max(v, self.min_value(result_state, alpha, beta, depth-1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            else:
                v = max(v, self.max_value(result_state, alpha, 100, depth))
                if v <= alpha:
                    return v
                beta = min(beta, v)
        return v

    def min_value(self, state, alpha, beta, depth):
        if (Board.game_over(state) or depth==0):
            return self.utility(state)
        v = 100
        for action in Board.possible_actions(state, False if self.maximizing_player == 0 else True):
            s, switch_turns = Board.result(state, action, self.players[self.minimizing_player])
            result_state = s[:]
            if (switch_turns):
                v = min(v, self.max_value(result_state, -100, beta, depth-1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            else:
                v = min(v, self.min_value(result_state, alpha, beta, depth))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        return v

    def utility(self, state):
        utility = 0
        if self.maximizing_player == 0: 
            utility = state[6] - state[13]
        elif self.maximizing_player == 1:
            utility = state[13] - state[6]
        if Board.game_over(state):
            utility += 1000
        return utility

    def pick_best_move(self):
        '''
        Picking the best move based on the alpha beta search. If there are several moves that are equally good
        the AI will randomly choose one of them. 
        '''
        max_score_index = max(self.action_score.items(), key = operator.itemgetter(1))[0] # gets key/action with highest value i.e. the best move
        max_score = self.action_score[max_score_index]
        no_of_max_scores = 0 
        for key in self.action_score.keys(): # as there might be more moves that result in the max_score we find those
            if self.action_score[key] == max_score:
                no_of_max_scores += 1
        choices = nlargest(no_of_max_scores, self.action_score, key = self.action_score.get)
        return random.choice(choices)

if __name__ == '__main__':
    kalaha = Kalaha()
    print('\n' * 100)
    choice = kalaha.display_menu()
    if choice == 1:
        choice = kalaha.ai_menu()
        AI_player_no = kalaha.AI_plays_as()
        kalaha.play_against_ai(choice, AI_player=AI_player_no)
    elif choice == 2:
        print('\n' * 100)
        kalaha.play_against_human()
    elif choice == 3:
        print("Goodbye")