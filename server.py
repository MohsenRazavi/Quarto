import time

from socketio import *
from gevent import pywsgi
import GameClass
import copy



server = Server(async_mode='gevent')

All_mohre = [('Black', 'Tall', 'ToPor', 'Circular'),
             ('Black', 'Tall', 'ToPor', 'Squerness'),
             ('Black', 'Tall', 'ToKhali', 'Circular'),
             ('Black', 'Tall', 'ToKhali', 'Squerness'),
             ('Black', 'Short', 'ToPor', 'Circular'),
             ('Black', 'Short', 'ToPor', 'Squerness'),
             ('Black', 'Short', 'ToKhali', 'Circular'),
             ('Black', 'Short', 'ToKhali', 'Squerness'),
             ('White', 'Tall', 'ToPor', 'Circular'),
             ('White', 'Tall', 'ToPor', 'Squerness'),
             ('White', 'Tall', 'ToKhali', 'Circular'),
             ('White', 'Tall', 'ToKhali', 'Squerness'),
             ('White', 'Short', 'ToPor', 'Circular'),
             ('White', 'Short', 'ToPor', 'Squerness'),
             ('White', 'Short', 'ToKhali', 'Circular'),
             ('White', 'Short', 'ToKhali', 'Squerness')]

all_mohre_backup = copy.deepcopy(All_mohre)


occupied_positions = []
players_info = {}
players_id = []
id = 0
startGame = 0
def printBoard(board):
    for i in board:
        for j in i:
            print(j, end=' ')
        print()



@server.event
def connect(sid, environ, auth):
    print(sid, "connected!")
    players_id.append(sid)



@server.event
def startGame(sid, data):  # catchs players info list
    global startGame
    players_info[sid] = data
    if len(players_info) == 2:
        startGame = 1
        server.emit('show_partner_info', data=players_info[players_id[1]], room=players_id[0])
        server.emit('show_partner_info', data=players_info[players_id[0]], room=players_id[1])
        GameClass.mohre_giri(server,players_id[0])
        server.emit('show_message', data='---> Wait for your partner to choose the mohre\n(Thanks for your patience :))', room=players_id[1])
        GameClass.addPlayerToScoreBoard(players_info[players_id[0]][0], players_info[players_id[1]][0])



@server.event
def mohreGir(sid, data):  # catchs player mohre and shows mohre to other player
    if id == 0 and startGame == 1:
        GameClass.makan_giri(server, data, players_id[1])
    elif id == 1 and startGame == 1:
        GameClass.makan_giri(server, data, players_id[0])


@server.event
def mohre_pardazesh(sid,data):
    global All_mohre
    if id == 0 and startGame == 1:
        All_mohre.remove(tuple(data))
        GameClass.makan_giri(server, data, players_id[1])
    elif id == 1 and startGame == 1:
        All_mohre.remove(tuple(data))
        GameClass.makan_giri(server, data, players_id[0])



@server.event
def makanGir(sid, data):  # pardazesh mohre\makan ersal update
    global occupied_positions, id, startGame, temp , All_mohre
    print(f'{data} is hereeee !!')
    print(f'id is {id}')
    occupied_positions.append(data)

    if id == 0 and startGame == 1:
        GameClass.makan_pardazesh(data, players_info[players_id[1]][2])
        print(f'{data} sent to makan pardazesh in GameClass')
        GameClass.send_updates(server, All_mohre, occupied_positions)
        print('Updates are cominggg ...')
        printBoard(GameClass.board_for_check)
        if GameClass.win_check(GameClass.board_for_check) == True:
            print('win check is running')
            server.emit('show_message',data=f'{players_info[players_id[0]][0]} win !')
            startGame = 0
            players_info.clear()
            server.emit('new_game',data=0)
        #end of game
            players_info.clear()
            occupied_positions.clear()
            All_mohre = copy.deepcopy(all_mohre_backup)
        else:
            print('win check is failed')
            GameClass.mohre_giri(server, players_id[1])
            print('mohre giri is runing')
            id = 1
    elif id == 1 and startGame == 1:
        GameClass.makan_pardazesh(data, players_info[players_id[0]][2])
        print(f'{data} sent to makan pardazesh in GameClass')
        GameClass.send_updates(server, All_mohre, occupied_positions)
        print('Updates are cominggg ...')
        printBoard(GameClass.board_for_check)
        if GameClass.win_check(GameClass.board_for_check) == True:
            print('win check is running')
            server.emit('show_message',data=f'{players_info[players_id[1]][0]} win !')
            startGame = 0
            players_info.clear()
            server.emit('new_game', data=0)
        #end of game
            players_info.clear()
            occupied_positions.clear()
            All_mohre = copy.deepcopy(all_mohre_backup)
        else:
            print('win check is failed')
            GameClass.mohre_giri(server, players_id[0])
            print('mohre giri is runing')
            id = 0

    occupied_positions.append(data)


@server.event
def exitAndSave(sid, data):
    if data == 'Exit':
        server.emit('show_message', data=f'---> {players_info[sid][0]} left the game')
        GameClass.Save()
    elif data == 'New Game':
        server.emit('show_message', data=f'---> {players_info[sid][0]} wants to play a new game')
@server.event
def disconnect(sid):
    print('disconnect ', sid)
    server.disconnect(sid)


app = WSGIApp(server)

pywsgi.WSGIServer(("127.0.0.1", 5000), app).serve_forever()
