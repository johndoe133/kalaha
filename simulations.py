from kalaha import Kalaha
import matplotlib.pyplot as plt

win_player_1 = 0
win_player_2 = 0
draw = 0
f = open("sim.txt","w+")
for i in range(100):
    kalaha = Kalaha()
    winner, score = kalaha.ai_against_ai(3,3)
    if winner == 1:
        win_player_1 += 1
    elif winner == 2:
        win_player_2 += 1
    else:
        draw += 1

header = "Player1, Player2, Draw\n"
f.write(header)
result = str(win_player_1) + ", " + str(win_player_2) + ", " + str(draw)
print(result)
f.write(result)
f.close()

x=[1,2,3]
plt.bar(x,[win_player_1, win_player_2, draw])
plt.xticks(x, ('Player 1', 'Player 2', 'Draw'))
plt.ylabel('Wins')
plt.show()
