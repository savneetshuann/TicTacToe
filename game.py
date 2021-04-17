# Tic Tac Toe game with SqlLite and Numpy library

import random
from tkinter import *  # tkinter is used to call all the GUI elements
import sqlite3
from functools import partial
from tkinter import messagebox  # importing messagebox
from copy import deepcopy

# sign variable to decide the turn of which player
sign = 0

# Creates an empty board
global board
board = [[" " for x in range(3)] for y in range(3)]  # For loop for board dimensions


# Check l(O/X) won the match or not
# according to the rules of the game
def winner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or  # confirming all the possiblities on the board
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))


# Configure text on button while playing with another player
def get_value(i, j, gb, l1, l2):  # multiplayer configuration for ACTIVE and DISABLED state on the board
    global sign

    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)  # Player1 DISABLED
            l2.config(state=ACTIVE)  # Player2 ACIVE
            board[i][j] = "X"
        else:
            l2.config(state=DISABLED)  # Player2 DISABLED
            l1.config(state=ACTIVE)  # Player1 ACTIVE
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    if winner(board, "X"):
        gb.destroy()
        # global opened
        box = messagebox.showinfo("Winner", "Player1 won the match")
        print(open_multiple.user_name1)
        # and here to add to sqldb
        # textname.get()

        conn = sqlite3.connect('player_info.db')
        c = conn.cursor()
        # c.execute("""insert or replace INTO the players
        # (user_name,no_of_wins,no_of_loss,points)
        # VALUES((select id from players where user_name = user_name1.get(),user_name1.get(),
        # 1,0,10)""")
        c.execute("""insert or replace INTO players
        (user_name,no_of_wins,no_of_loss,points)
        VALUES("test",
        1,0,10)""")
        conn.commit()
        conn.close()

    elif winner(board, "O"):
        gb.destroy()
        messagebox.showinfo("Winner", "Player 2 won the match")
    elif (isfull()):
        gb.destroy()
        messagebox.showinfo("Tie Game", "Tie Game")


# Check if the player can push the button or not
def isfree(i, j):
    return board[i][j] == " "


# Check the board is full or not
def isfull():
    flag = True
    for i in board:
        if i.count(' ') > 0:
            flag = False
    return flag


# Create the GUI of game board for play along with another player
def gameboard_players(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_value, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()


# Decide the next move of system
def machine():
    possiblemove = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                possiblemove.append([i, j])

    if possiblemove == []:
        return
    else:
        for let in ['O', 'X']:
            for i in possiblemove:
                boardcopy = deepcopy(board)
                boardcopy[i[0]][i[1]] = let
                if winner(boardcopy, let):
                    return i
        corner = []
        for i in possiblemove:
            if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                corner.append(i)
        if len(corner) > 0:
            move = random.randint(0, len(corner) - 1)
            return corner[move]
        edge = []
        for i in possiblemove:
            if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                edge.append(i)
        if len(edge) > 0:
            move = random.randint(0, len(edge) - 1)
            return edge[move]


# Configure text on button while playing with system
def get_value_pc(i, j, gb, l1, l2):
    global sign

    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)         #Player DISABLED
            l2.config(state=ACTIVE)           #Computer ACTIVE
            board[i][j] = "X"
        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)          #Computer DISABLED
            l1.config(state=ACTIVE)            #Player ACTIVE
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    x = True
    if winner(board, "X"):
        gb.destroy()
        x = False
        messagebox.showinfo("Winner", "Player won the match")

    elif winner(board, "O"):
        gb.destroy()
        x = False
        messagebox.showinfo("Winner", "Computer won the match")

    elif (isfull()):
        gb.destroy()
        x = False
        messagebox.showinfo("Tie Game", "Tie Game")

    if (x):
        if sign % 2 != 0:
            move = machine()
            button[move[0]][move[1]].config(state=DISABLED)
            get_value_pc(move[0], move[1], gb, l1, l2)


# Create the GUI of game board for play along with system
def gameboard_pc(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_value_pc, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()


# Initialize the game board to play with system
def with_machine(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="Player : X", width=10)
    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Computer : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_pc(game_board, l1, l2)


# Initialize the game board to play with another player
def with_player(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="Player 1 : X", width=10)

    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Player 2 : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_players(game_board, l1, l2)

    # clear text box


# db connections
def connection():
    conn = sqlite3.connect('player_info.db')
    curs = conn.cursor()

    # create table for player information to be stored in SqlLite Database
    curs.execute("""Create table players(P_id integer PRIMARY KEY AUTOINCREMENT,user_name text, no_of_wins integer, no_of_loss integer, 
                 points  integer)""")

    # commit changes
    conn.commit()
    conn.close()


def open_single():
    top = Toplevel()
    wpc = partial(with_machine, top)
    user_name_label = Label(top, text="Enter your username: ")
    user_name_label.grid(row=0, column=0)
    user_name = Entry(top, width=30)
    user_name.grid(row=1, column=0, padx=20)
    submit_btn = Button(top, text="Play", command=wpc, activeforeground='white',
                        activebackground="grey", bg="blue", fg="white", font='Gabriola')
    submit_btn.grid(row=2, column=0, pady=10, padx=10)


def insert():
    # trying to access here
    pass


def open_multiple():
    top = Tk()
    wpl = partial(with_player, top)

    user_name_label1 = Label(top, text="Enter username for Player1: ")
    user_name_label1.grid(row=0, column=0)
    open_multiple.user_name1 = Entry(top, width=30)  # user1 from here need to insert in database
    open_multiple.user_name1.grid(row=1, column=0, padx=20)

    user_name_label2 = Label(top, text="Enter username for Player2: ")
    user_name_label2.grid(row=2, column=0)
    open_multiple.user_name2 = Entry(top, width=30)
    open_multiple.user_name2.grid(row=3, column=0, padx=20)
    submit_btn = Button(top, text="Play", command=wpl, activeforeground='white',  # command=lambda: [wpl, insert]
                        activebackground="grey", bg="blue", fg="white", font='Gabriola')
    submit_btn.grid(row=4, column=0, pady=10, padx=10)
    top.mainloop()


# creating the ui for the game
def run():
    menu = Tk()
    menu.geometry("400x400")
    menu.title("Tic Tac Toe")

    # wpl = partial(with_player, menu)
    # op=partial(open_single,menu)

    # submit_btn = Button(top, "PLAY")
    # submit_btn.grid(row=2, column=0, pady=10, padx=10)

    head = Label(menu, text="Welcome to tic-tac-toe",
                 activeforeground='white',
                 activebackground="black", bg="white",
                 fg="black", width=500, font='Modern', bd=5)

    # menu1 = Button(menu, text="Single Player", command=wpc,
    #                activeforeground='white',
    #                activebackground="grey", bg="blue",
    #                fg="white", width=500, font='Gabriola', bd=5)
    menu1 = Button(menu, text="Single Player", command=open_single, activeforeground='white',
                   activebackground="grey", bg="blue", fg="white",
                   width=500, font='Gabriola', bd=5)

    menu2 = Button(menu, text="Multi Player", command=open_multiple, activeforeground='white',
                   activebackground="grey", bg="blue", fg="white",
                   width=500, font='Gabriola', bd=5)

    menu3 = Button(menu, text="Exit", command=menu.quit, activeforeground='white',
                   activebackground="grey", bg="blue", fg="white",
                   width=500, font='Gabriola', bd=5)
    head.pack(side='top')
    menu1.pack(side='top')
    menu2.pack(side='top')
    menu3.pack(side='top')
    menu.mainloop()


# table creation
# connection()

# execute the program
run()
