class Kalaha():
    def __init__(self):
        self.board = [4,4,4,4,4,4,0,4,4,4,4,4,4,0]
        self.oppositeside = dict()
        self.oppositeside[0] = 12
        self.oppositeside[1] = 11
        self.oppositeside[2] = 10
        self.oppositeside[3] = 9
        self.oppositeside[4] = 8
        self.oppositeside[5] = 7
        self.oppositeside[7] = 5
        self.oppositeside[8] = 4
        self.oppositeside[9] = 3
        self.oppositeside[10] = 2
        self.oppositeside[11] = 1
        self.oppositeside[12] = 0
        
        
        

    def gameOver(self):
        '''
        Checks if the game is over
        '''
        if (sum(self.board[0:6]) == 0 or (sum(self.board[7:13]) == 0)):
            return True
        else:
            return False
            
    def printboard(self, player):
        '''
        Prints the board. 

        Parameters
        ----------
        player : int
                 Indicate which player it is. If you wish to display game state, set `player=0`
        '''
        p1 = ''
        p2 = ''
        if player == 1:
            p1 = ' --> '
            p2 = '     '
        elif player == 2:
            p2 = ' --> '
            p1 = '     '
        elif player == 0:
            p2 = '     '
            p1 = '     '
        else: 
            raise Exception('Invalid player number')

        print(p2,end='')
        for i in range(6,0,-1):
            print(f'{i:^5}', end='')
        print('')
        print("-"*40)
        for i in range(1,8):
            print(f'{self.board[-i]:^5}', end='')
        print('\n\n     ',end='')
        for i in range(0,7):
            print(f'{self.board[i]:^5}', end='')
        print('')
        print("-"*40)
        print(p1,end='')
        for i in range(1,7):
            print(f'{i:^5}', end='')
        print("")

    def player_move(self,player):
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
        self.printboard(player)
        while True:
            pick = int(input("Pick a slot: "))
            pick =  pick - 1
            if pick in [0,1,2,3,4,5]:
                if player == 1:
                    if self.board[pick] != 0:
                        break
                elif player == 2:
                    if self.board[pick + 7] != 0:
                        break
            print("Pick a proper slot")
                    
        return pick

    def move(self, player, pick):
        if player == 1:
            beans = self.board[pick]
            self.board[pick] = 0
            putinto = pick
            while beans > 0:
                putinto = (putinto + 1) % 13
                # doesnt get into player 2s kalaha
                self.board[putinto] += 1
                beans -= 1
        else:
            pick = pick + 7
            beans = self.board[pick]
            self.board[pick] = 0
            putinto = pick
            while beans > 0:
                putinto = (putinto + 1) % 14
                if putinto == 0:
                    putinto += 1 # skip player 1s kalaha
                self.board[putinto] += 1
                beans -= 1
        self.printboard(0)

# if you land in your own empty 'thing' you get that into the kalaha
# plus the pieces directly opposite
        if (self.board[putinto] == 1 and (putinto not in [6,13])):
            if player == 1:
                if putinto in range(0,6):
                    self.board[putinto] = 0
                    self.board[6] += 1
                    oppositeSideIndex = self.oppositeside[putinto]
                    oppositeSide = self.board[oppositeSideIndex]
                    self.board[oppositeSideIndex] = 0
                    self.board[6] += oppositeSide
            else:
                if putinto in range(7,13):
                    self.board[putinto] = 0
                    self.board[13] += 1
                    oppositeSideIndex = self.oppositeside[putinto]
                    oppositeSide = self.board[oppositeSideIndex]
                    self.board[oppositeSideIndex] = 0
                    self.board[13] += oppositeSide
                
        
        # if it ends in kalaha
        if player == 1:
            if putinto == 6:
                pick = kalaha.player_move(1)
                kalaha.move(1, pick)
        else:
            if putinto == 13:
                pick = kalaha.player_move(2)
                kalaha.move(2, pick)
                


        
        
kalaha = Kalaha()
winner = None
while True:
    if not kalaha.gameOver():
        print("Turn of player 1")
        pick = kalaha.player_move(1)
        kalaha.move(1, pick)
        print('\n')
    else:
        winner = 1
        break
    if not kalaha.gameOver():
        print("Turn of player 2")
        pick = kalaha.player_move(2)
        kalaha.move(2,pick)
        print('\n')
    else:
        winner = 2
        break
    
kalaha.printboard()
print("GAME OVER!")
print("Player",winner,"won")


