from kalaha import Kalaha, AI, Player, Board
import matplotlib.pyplot as plt

win_player_1 = 0
win_player_2 = 0
draw = 0
score_list_p1 = []
score_list_p2 = []

simulations = 4

kalaha = Kalaha()

ai1_depth = 5
ai2_depth = 1

for i in range(simulations):
    kalaha.reset_board()
    winner, score = kalaha.ai_against_ai(ai1_depth, ai2_depth)
    if winner == 1:
        win_player_1 += 1
        score_list_p1.append(score)
        score_list_p2.append(48-score)
    elif winner == 2:
        win_player_2 += 1
        score_list_p2.append(score)
        score_list_p1.append(48-score)
    else:
        draw += 1
        score_list_p2.append(score)
        score_list_p1.append(48-score)
    

header = "Player1, Player2, Draw\n"
result = str(win_player_1) + ", " + str(win_player_2) + ", " + str(draw)
print(result)


xbar=[1,2,3]
plt.bar(xbar,[win_player_1, win_player_2, draw], width=0.4)
plt.xticks(xbar, ('Player 1', 'Player 2', 'Draw'))
plt.ylabel('Wins')
plt.title("Simulations of AI vs AI")
plt.show()

"""
x = list(range(simulations))
plt.plot(x, score_list_p1, label="Player 1")
plt.plot(x, score_list_p2, label="Player 2")
plt.xlabel("Games")
plt.xticks(x)
plt.ylabel("Points")
plt.legend()
#plt.show()"""