import termcolor2
import json


XOboard = [['O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O']]
board = [[' ### ', ' ### ', ' ### ', ' ### '], [' ### ', ' ### ', ' ### ', ' ### '],
         [' ### ', ' ### ', ' ### ', ' ### '], [' ### ', ' ### ', ' ### ', ' ### ']]
board_for_check = [['###', '###', '###', '###'], ['###', '###', '###', '###'],
         ['###', '###', '###', '###'], ['###', '###', '###', '###']]
last_mohre = ''
mohre_for_check = []
Scores = {}




def addPlayerToScoreBoard(player1 , player2):
    global Scores
    Scores[player2] = 0
    Scores[player1] = 0

def mohre_giri(server, player_id):  # mohre neshoon mide va az client migire
    server.emit('mohre_gir', data='---> Enter a mohre : ', room=player_id)


def makan_giri(server, choosen_mohre, player_id):
    global last_mohre , mohre_for_check
    server.emit('show_choosen_mohre', data=choosen_mohre, room=player_id)
    server.emit('makan_gir', data='---> Enter a position (Order of numbers is like matris) :', room=player_id)
    last_mohre = '[' + (' '.join(choosen_mohre)) + ']'
    mohre_for_check = choosen_mohre[:]

def makan_pardazesh(choosen_position, color):
    global mohre_for_check
    x = termcolor2.colored('X', color=color)
    colored_mohre = termcolor2.colored(last_mohre, color=color)
    XOboard[choosen_position[0]][choosen_position[1]] = x
    board[choosen_position[0]][choosen_position[1]] = colored_mohre
    board_for_check[choosen_position[0]][choosen_position[1]] = mohre_for_check

def send_updates(server, All_mohre, occupied_position):  # send all mohre board XOboard occupied positions
    server.emit('get_updates', data=[All_mohre, board, XOboard, occupied_position])

def win_check(board):
    win = 0
    brk_flag = False
    def mohre_check(m1, m2):
        if m1 == '###' or m2 == '###':
            return False
        for i in range(4):
            if m1[i] == m2[i]:
                return True
        return False


    # satr check
    for satr in board_for_check:
        if '###' in satr:
            win = 0
            continue
        for i in range(4):
            for j in range(i + 1, 4):
                if mohre_check(satr[i], satr[j]) == True:
                    win = 1
                    brk_flag = True
                    print('satr check became true')
            if brk_flag == True:
                break
        if brk_flag == True:
            break
    if win == 1:
        return True


    # sotoon check
    for i in range(4):
        for j in range(3):
            if '###' in board_for_check[j][i] or '###' in board_for_check[j+1][i]:
                win = 0
                continue
        else:
            if mohre_check(board_for_check[j][i] , board_for_check[j+1][i]) == True:
                win = 1
                brk_flag = True
                print('sotoon check became true')
            if brk_flag == True:
                break
        if brk_flag == True:
            break
    if win == 1:
        return True

    # qotr check
    for i in range(4):
        for j in range(i + 1, 4):
            if '###' in board_for_check[i][i] or '###' in board_for_check[j][j]:
                win = 0
                continue
        else:
            if mohre_check(board_for_check[i][i], board_for_check[j][j]) == True:
                win = 1
                brk_flag = True
                print('qotr check brcame true')
                break
        if brk_flag == True:
            break
    if win == 1:
        return True

    #qotr faree check
    temp = [[0, 3], [1, 2], [2, 1], [3, 0]]
    for i in range(4):
        for j in range(i+1, 4):
            if '###' in board_for_check[temp[i][0]][temp[i][1]] or '###' in board_for_check[temp[j][0]][temp[j][1]]:
                win = 0
                continue
            elif board_for_check[0][3] == '###' or board_for_check[1][2] == '###' or board_for_check[2][1] == '###' or board_for_check[3][0] == '###' :
                win = 0
                continue
            else:
                if mohre_check(board_for_check[temp[i][0]][temp[i][1]], board_for_check[temp[j][0]][temp[j][1]]) == True:
                    win = 1
                    brk_flag = True
                    print('qotr faree check became true')
                    break
        if brk_flag == True:
            break
    if win == 1:
        return True

def scoreBoardUpdate(win):
    global Scores
    Scores[win] += 1

def Save():
    global Scores
    with open('ScoreBoard.txt', 'a') as f:
        f.write('\n',json.dumps(Scores))
