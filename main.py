import tkinter as tk

window = tk.Tk()
window.geometry('800x600')

#Init variables
level = 1
score = 0
best_score = 0
best_pushes = 0
pushes = 0
movecount = 0
timespent = 0
x_caisse = []
y_caisse = []
x_char = []
y_char = []
caisse = []
game_board = [[' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', '#', '#', '#', '#', ' ', '$', ' ', ' '],
              [' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', '.', ' '],
              [' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', '@'],
              [' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' '],
              ]

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

tk.Button(window, text='Abandon').grid(column = 1, row = 50, columnspan = 3)
tk.Button(window, text='Niveau Préc.').grid(column = 1, row = 100, columnspan = 3)
tk.Button(window, text='Niveau Suiv.').grid(column = 1, row = 110, columnspan = 3)
#END Text zone ---------------------------------------------------

#FONCTIONS--------------------------------------------------------
def draw_board():
    global backgd, char, caisse, x_char, y_char, x_caisse, y_caisse, nbcaisses, nbcaisses_a_pousser

    backgd.config(width=len(game_board[0]) * dim_case, height=len(game_board) * dim_case)
    for j in range(len(game_board[0])):
        for i in range(len(game_board)):
            x, y = j * dim_case, i * dim_case
            if game_board[i][j] == '#':  # Wall
                backgd.create_image(x, y, image=mur, anchor='nw')
            elif game_board[i][j] == '@':  # Personnage
                backgd.create_image(x, y, image=perso, anchor='nw')
            elif game_board[i][j] == '.':  # But
                backgd.create_image(x, y, image=hole, anchor='nw')
            elif game_board[i][j] == '$':  # Caisse
                x_caisse.append(i)
                y_caisse.append(j)
                caisse.append(backgd.create_image(x + 25, y + 25, image=box, anchor='center'))
    backgd.tag_raise(char)
    for i in range(nbcaisses):
        backgd.tag_raise(caisse[i])


#END FONCTIONS----------------------------------------------------

draw_board()
window.mainloop()
