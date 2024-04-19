from socketio import *
import fpfc
import termcolor
import time
from tabulate import tabulate


client = Client()

mohre_mojaz = [('Black', 'Tall', 'ToPor', 'Circular'),
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
               ('White', 'Short', 'ToKhali', 'Squerness')
               ]

occupied_positions = []



def printBoard(board):
    print(tabulate(board, headers=[1, 2, 3, 4], showindex=[1, 2, 3, 4]), '\n')


@client.event
def show_partner_info(data):
    text = termcolor.colored(f'--->> Your partner is {data[0]} <<---', color=data[2])
    print(text)


@client.event
def show_message(data): #about winner
    time.sleep(1.5)
    print(data)


@client.event
def mohre_gir(data):  # shows the message and sends mohre
    time.sleep(1)
    print(data)
    for i in mohre_mojaz:
        print(i)
    mohre = [a for a in input().split()]
    while True:
        if tuple(mohre) in mohre_mojaz:
            break
        else:
            print('Invalid mohre . Try again')
            mohre = [a for a in input().split()]
    print(f' > {mohre} sent ! <')
    client.emit('mohre_pardazesh', data=mohre)


@client.event
def show_choosen_mohre(data):
    print(f'---> your partner choosed {data} <---')


@client.event
def makan_gir(data):
    print(data)

    position = [int(a) for a in input().split()]
    p = position[:]
    position[0] -= 1
    position[1] -= 1
    while True:
        if position[0] < 0 or position[0] > 3 or position[1] < 0 or position[1] > 3:
            print("Invalid Position . Try again")
            position = [int(a) for a in input().split()]
            p = position[:]
            position[0] -= 1
            position[1] -= 1
        elif position in occupied_positions:
            print('This position is occupied . Try again')
            position = [int(a) for a in input().split()]
            p = position[:]
            position[0] -= 1
            position[1] -= 1
        else:
            client.emit('makanGir', data=position)
            print(f'---> The mohre set at {p} !')
            break


@client.event
def get_updates(data):
    global mohre_mojaz
    global occupied_positions
    mohre_mojaz = [tuple(a) for a in data[0]]  # all mohre
    time.sleep(.5)
    printBoard(data[1])  # board
    printBoard(data[2])  # XOboard
    occupied_positions += data[3]  # occupied positions


@client.event
def new_game(data):
    time.sleep(1.5)
    if data == 0:
        if player.new_game() == 'Exit':
            client.emit('exitAndSave', data='Exit')
            time.sleep(.7)
            client.emit('disconnect')


client.connect("http://127.0.0.1:5000")

player = fpfc.User()
player.main_page()

if player.start_game() == 1:
    userInfo = player.user_info
    client.emit('startGame', data=userInfo)