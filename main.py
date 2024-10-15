import tkinter as tk
import copy
import os
import sys

window = tk.Tk()
window.geometry('800x600')
window.title('Sokoban')

#Init variables
level = 1
score = 0
best_score = 0
best_pushes = 0
pushes = 0
movecount = 0
timespent = 0
nbBoxesOnHoles = 0
x_caisse = []
y_caisse = []
x_char = []
y_char = []
caisse = []
can_move = True
game_board = [[' ', ' ', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' '],
              ['#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
              ['#', ' ', '$', ' ', '#', '#', '#', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', '$', ' ', ' ', ' '],
              [' ', ' ', ' ', '.', '.', ' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '@'],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
              ]
initial_game_board = copy.deepcopy(game_board) #COPY OF THE INITIAL GAME BOARD FOR RESTART

#Calcul du nombre de caisses
nbcaisses = 0
for i in range(len(game_board)):
    nbcaisses += game_board[i].count('$')

dim_case = 50 #Taille de chaque case

#Load assets
mur = tk.PhotoImage(file="assets/wall.gif")
perso = tk.PhotoImage(file="assets/homme.gif")
box = tk.PhotoImage(file="assets/caisse.gif")
hole = tk.PhotoImage(file="assets/hole.gif")


backgd = tk.Canvas(window, width = len(game_board[0])*dim_case, height=len(game_board)*dim_case, bg="#FFFFFF")
backgd.grid(rowspan=500)

#Text zone -------------------------------------------------------
info_lvl = tk.Label(window, text='Niveau' + str(level))
info_lvl.grid(column = 1, row = 0, columnspan = 3)

info_moves = tk.Label(window, text='Mouvements : ')
info_moves.grid(column = 1, row = 2, sticky='w')
info_vmoves = tk.Label(window, text=str(movecount))
info_vmoves.grid(column=2, row=2, sticky='w')

info_best_moves = tk.Label(window, text='Record : ' + str(best_score))
info_best_moves.grid(column = 3, row = 2)

info_pushes = tk.Label(window, text='Poussées : '+str(best_pushes))
info_pushes.grid(column=1, row=4)

info_best_pushes = tk.Label(window, text = "Record : " + str(best_pushes))
info_best_pushes.grid(column=3, row=4)

info_time = tk.Label(window, text = 'Temps : ')
info_time.grid(column=1, row=6)
info_vtime = tk.Label(window, text=str(timespent))
info_vtime.grid(column=2, row=6)

info_auteur = tk.Label(window, text="Author : thomh")
info_auteur.grid(column = 1, row = 499, columnspan = 3)

#END Text zone ---------------------------------------------------

#FONCTIONS--------------------------------------------------------
"""def clear_console(): #TODO: A SUPPRIMER APRES TEST (used for debug atm)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')"""

def draw_board():
    global backgd, char, caisse, x_char, y_char, x_caisse, y_caisse, nbcaisses, nbcaisses_a_pousser

    backgd.config(width=len(game_board[0]) * dim_case, height=len(game_board) * dim_case)
    for j in range(len(game_board[0])):
        for i in range(len(game_board)):
            x, y = j * dim_case, i * dim_case
            if game_board[i][j] == '#':  # Wall
                backgd.create_image(x, y, image=mur, anchor='nw')
            elif game_board[i][j] == '@':  # Personnage
                char = backgd.create_image(x, y, image=perso, anchor='nw')
                x_char.append(x)
                y_char.append(y)
            elif game_board[i][j] == '.':  # But
                backgd.create_image(x, y, image=hole, anchor='nw')
            elif game_board[i][j] == '$':  # Caisse
                x_caisse.append(i)
                y_caisse.append(j)
                caisse.append(backgd.create_image(x + 25, y + 25, image=box, anchor='center'))
            elif game_board[i][j] == '+': #Character on hole
                char = backgd.create_image(x, y, image=perso, anchor='nw')
                x_char.append(x)
                y_char.append(y)
                backgd.create_image(x, y, image=hole, anchor='nw')
            elif game_board[i][j] == '*': #Box on hole
                x_caisse.append(i)
                y_caisse.append(j)
                caisse.append(backgd.create_image(x + 25, y + 25, image=box, anchor='center'))
                backgd.create_image(x, y, image=hole, anchor='nw')
    backgd.tag_raise(char)
    for i in range(nbcaisses):
        backgd.tag_raise(caisse[i])

"""CHECKING AND HANDLING THE WIN"""
def check_win():
    global game_board, nbBoxesOnHoles, nbcaisses
    nbBoxesOnHoles = 0 #Reset the number of boxes on holes (fix to issue where the number of boxes on holes would be incremented with each move)
    for i in range(len(game_board)): #Check if the number of boxes on holes is equal to the number of boxes
        nbBoxesOnHoles += game_board[i].count('*')
    return nbBoxesOnHoles == nbcaisses

def win():
    global backgd, can_move
    backgd.create_text(len(game_board[0]) * dim_case // 2, len(game_board) * dim_case // 2, text="Félicitations ! c'est gagné.",
                     font=('Arial', 30),
                     fill='yellow')
    can_move = False

"""MOVEMENT FUNCTIONS - UP, DOWN, LEFT, RIGHT + BOX LOGIC """
def up(evt):
    global x_char, y_char, backgd, movecount, char, game_board, caisse, pushes, can_move

    if not can_move:
        return

    new_y = y_char[0] - 50
    current_x = x_char[0] // 50
    current_y = y_char[0] // 50
    next_y = new_y // 50

    if next_y < 0 or game_board[next_y][current_x] in ['#', '*']:
        return

    if game_board[next_y][current_x] == '$':
        new_box_y = new_y - 50
        next_box_y = new_box_y // 50

        if next_box_y < 0 or game_board[next_box_y][current_x] not in [' ', '.', '*']:
            return

        game_board[next_y][current_x] = ' '
        if game_board[next_box_y][current_x] == '.':
            game_board[next_box_y][current_x] = '*'
        else:
            game_board[next_box_y][current_x] = '$'

        for i in range(len(caisse)):
            coords = backgd.coords(caisse[i])
            if coords == [current_x * 50 + 25, next_y * 50 + 25]:
                backgd.coords(caisse[i], current_x * 50 + 25, new_box_y + 25)
                break

        pushes += 1
        info_pushes.config(text='Poussées : ' + str(pushes))

    if game_board[current_y][current_x] == '+':
        game_board[current_y][current_x] = '.'
    else:
        game_board[current_y][current_x] = ' '

    if game_board[next_y][current_x] == '.':
        game_board[next_y][current_x] = '+'
    else:
        game_board[next_y][current_x] = '@'

    backgd.coords(char, x_char[0], new_y)
    y_char[0] = new_y

    movecount += 1
    info_vmoves.config(text=str(movecount))

    """#clear_console()
    print(game_board)  # Debug print to check the game board state"""

    if check_win():
        win()

def left(evt):
    global x_char, y_char, backgd, movecount, char, game_board, caisse, pushes, can_move

    if not can_move:
        return

    new_x = x_char[0] - 50
    current_x = x_char[0] // 50
    current_y = y_char[0] // 50
    next_x = new_x // 50

    if next_x < 0 or game_board[current_y][next_x] in ['#', '*']:
        return

    if game_board[current_y][next_x] == '$':
        new_box_x = new_x - 50
        next_box_x = new_box_x // 50

        if next_box_x < 0 or game_board[current_y][next_box_x] not in [' ', '.', '*']:
            return

        game_board[current_y][next_x] = ' '
        if game_board[current_y][next_box_x] == '.':
            game_board[current_y][next_box_x] = '*'
        else:
            game_board[current_y][next_box_x] = '$'

        for i in range(len(caisse)):
            coords = backgd.coords(caisse[i])
            if coords == [new_x + 25, current_y * 50 + 25]:
                backgd.coords(caisse[i], new_box_x + 25, current_y * 50 + 25)
                break

        pushes += 1
        info_pushes.config(text='Poussées : ' + str(pushes))

    if game_board[current_y][current_x] == '+':
        game_board[current_y][current_x] = '.'
    else:
        game_board[current_y][current_x] = ' '

    if game_board[current_y][next_x] == '.':
        game_board[current_y][next_x] = '+'
    else:
        game_board[current_y][next_x] = '@'

    backgd.coords(char, new_x, y_char[0])
    x_char[0] = new_x

    movecount += 1
    info_vmoves.config(text=str(movecount))

    """#clear_console()
    print(game_board)  # Debug print to check the game board state"""

    if check_win():
        win()

def right(evt):
    global x_char, y_char, backgd, movecount, char, game_board, caisse, pushes, can_move

    if not can_move:
        return

    new_x = x_char[0] + 50
    current_x = x_char[0] // 50
    current_y = y_char[0] // 50
    next_x = new_x // 50

    if next_x >= len(game_board[0]) or game_board[current_y][next_x] in ['#', '*']:
        return

    if game_board[current_y][next_x] == '$':
        new_box_x = new_x + 50
        next_box_x = new_box_x // 50

        if next_box_x >= len(game_board[0]) or game_board[current_y][next_box_x] not in [' ', '.', '*']:
            return

        game_board[current_y][next_x] = ' '
        if game_board[current_y][next_box_x] == '.':
            game_board[current_y][next_box_x] = '*'
        else:
            game_board[current_y][next_box_x] = '$'

        for i in range(len(caisse)):
            coords = backgd.coords(caisse[i])
            if coords == [new_x + 25, current_y * 50 + 25]:
                backgd.coords(caisse[i], new_box_x + 25, current_y * 50 + 25)
                break

        pushes += 1
        info_pushes.config(text='Poussées : ' + str(pushes))

    if game_board[current_y][current_x] == '+':
        game_board[current_y][current_x] = '.'
    else:
        game_board[current_y][current_x] = ' '

    if game_board[current_y][next_x] == '.':
        game_board[current_y][next_x] = '+'
    else:
        game_board[current_y][next_x] = '@'

    backgd.coords(char, new_x, y_char[0])
    x_char[0] = new_x

    movecount += 1
    info_vmoves.config(text=str(movecount))

    """#clear_console()
    print(game_board)  # Debug print to check the game board state"""

    if check_win():
        win()

def down(evt):
    global x_char, y_char, backgd, movecount, char, game_board, caisse, pushes, can_move

    if not can_move:
        return

    new_y = y_char[0] + 50
    current_x = x_char[0] // 50
    current_y = y_char[0] // 50
    next_y = new_y // 50

    if next_y >= len(game_board) or game_board[next_y][current_x] in ['#', '*']:
        return

    if game_board[next_y][current_x] == '$':
        new_box_y = new_y + 50
        next_box_y = new_box_y // 50

        if next_box_y >= len(game_board) or game_board[next_box_y][current_x] not in [' ', '.', '*']:
            return

        game_board[next_y][current_x] = ' '
        if game_board[next_box_y][current_x] == '.':
            game_board[next_box_y][current_x] = '*'
        else:
            game_board[next_box_y][current_x] = '$'

        for i in range(len(caisse)):
            coords = backgd.coords(caisse[i])
            if coords == [current_x * 50 + 25, new_y + 25]:
                backgd.coords(caisse[i], current_x * 50 + 25, new_box_y + 25)
                break

        pushes += 1
        info_pushes.config(text='Poussées : ' + str(pushes))

    if game_board[current_y][current_x] == '+':
        game_board[current_y][current_x] = '.'
    else:
        game_board[current_y][current_x] = ' '

    if game_board[next_y][current_x] == '.':
        game_board[next_y][current_x] = '+'
    else:
        game_board[next_y][current_x] = '@'

    backgd.coords(char, x_char[0], new_y)
    y_char[0] = new_y

    movecount += 1
    info_vmoves.config(text=str(movecount))

    """#clear_console()
    print(game_board)  # Debug print to check the game board state"""

    if check_win():
        win()

def abandon():
    global game_board, x_char, y_char, x_caisse, y_caisse, caisse, nbcaisses, pushes, movecount, can_move, nbBoxesOnHoles

    # Reset the game board to the initial state and variables
    game_board = copy.deepcopy(initial_game_board)
    x_char = []
    y_char = []
    x_caisse = []
    y_caisse = []
    caisse = []
    pushes = 0
    movecount = 0
    nbBoxesOnHoles = 0
    can_move = True
    backgd.delete('all')
    draw_board()
    info_vmoves.config(text=str(movecount))
    info_pushes.config(text='Poussées : ' + str(pushes))


#END FONCTIONS----------------------------------------------------

#BOUTONS----------------------------------------------------------
tk.Button(window, text='Abandon', command=abandon).grid(column = 1, row = 50, columnspan = 3)
tk.Button(window, text='Niveau Préc.',).grid(column = 1, row = 100, columnspan = 3)
tk.Button(window, text='Niveau Suiv.').grid(column = 1, row = 110, columnspan = 3)
#END BOUTONS------------------------------------------------------

#COMMANDES--------------------------------------------------------
window.bind_all('<z>', up)
window.bind_all('<q>', left)
window.bind_all('<s>', down)
window.bind_all('<d>', right)
#END COMMANDES----------------------------------------------------

draw_board()
window.mainloop()
