from Kalaha import Kalaha

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
