from kalaha import Kalaha, AI, Player, Board
import matplotlib.pyplot as plt
from statistics import stdev, mean

def run_sim(simulations, ai1_depth, ai2_depth):
    
    win_player_1 = 0
    win_player_2 = 0
    draw = 0
    
    score_diff_p1 = []
    score_diff_p2 = []

    kalaha = Kalaha()


    for i in range(simulations):
        kalaha.reset_board()
        winner, score = kalaha.ai_against_ai(ai1_depth, ai2_depth)
        if winner == 1:
            win_player_1 += 1
            score_diff_p1.append(score - (48-score))

        elif winner == 2:
            win_player_2 += 1
            score_diff_p2.append(score - (48-score))

        else:
            draw += 1

    header = "Player1, Player2, Draw\n"
    result = str(win_player_1) + ", " + str(win_player_2) + ", " + str(draw)
    print(header)
    print(result)
    print("")
    print("In games where Player 1 wins.")
    print("Wins on average by",mean(score_diff_p1),"points")
    print("with a stdev of",stdev(score_diff_p1))

    print("In games where Player 2 wins.")
    print("Wins on average by",mean(score_diff_p2),"points")
    print("with a stdev of",stdev(score_diff_p2))

    #plot
    xbar=[1,2,3]
    y = [win_player_1, win_player_2, draw]
    plt.bar(xbar,y, width=0.4)
    plt.xticks(xbar, ('Player 1\n Search depth: '+str(ai1_depth), 'Player 2\n Search depth: '+str(ai2_depth), 'Draw'))
    plt.ylabel('Wins')
    plt.show()

# run_sim(1000,1,1)
# run_sim(1000,1,2)
#run_sim(1000,1,3)
# run_sim(1000,1,4)
# run_sim(1000,1,5)
# run_sim(1000,1,6)
# run_sim(1000,2,1)
# run_sim(1000,3,1)
# run_sim(1000,4,1)
run_sim(1000,5,1)
# run_sim(1000,6,1)