import tkinter as tk
import copy
import os

window = tk.Tk()
window.title('Sokoban')
LVL_FOLDER = 'levels/'
dim_case = 50
mur = tk.PhotoImage(file="assets/wall.gif")
perso = tk.PhotoImage(file="assets/homme.gif")
box = tk.PhotoImage(file="assets/caisse.gif")
hole = tk.PhotoImage(file="assets/hole.gif")
x_caisse = []
y_caisse = []
x_char = []
y_char = []
caisse = []
movecount = 0
pushcount = 0
bestmoves = 0
bestpushes = 0
can_move = True

#GAME FUNCTIONS ---------------------------------------------------
def clear_main_menu():
    """Clears the main menu widgets."""
    for widget in window.winfo_children():
        widget.destroy()

def level_to_list(level_filename):
    # Construct the full path to the level file
    levels_dir = '/home/thomh/PycharmProjects/sokobanPy/levels'
    level_path = os.path.join(levels_dir, level_filename)

    try:
        # Open and read the level file
        with open(level_path, 'r') as level_file:
            level_content = level_file.readlines()  # Read all lines into a list

        # Process the level content into a list of lists (2D board)
        # Note: Do NOT use strip() here as it would remove leading/trailing spaces
        board = [list(line.rstrip('\n')) for line in level_content]  # Only strip newlines

        return board

    except FileNotFoundError:
        print(f"Error: Level file '{level_filename}' not found in {levels_dir}.")
        return None

def main_menu():
    """Creates the main menu for the game."""
    global can_move, movecount, pushcount
    can_move = True
    movecount = 0
    pushcount = 0

    window.title("Sokoban - Menu")

    # Set window size and position
    window.geometry("400x400")  # Adjust the size as per your requirement

    # Clear any previous widgets
    for widget in window.winfo_children():
        widget.destroy()

    # Title label
    title_label = tk.Label(window, text="Welcome to Sokoban", font=("Helvetica", 20, "bold"))
    title_label.pack(pady=50)

    # Start Game button (opens the level selection screen)
    start_button = tk.Button(window, text="Start Game", font=("Helvetica", 14), width=15, command=level_selection)
    start_button.pack(pady=20)

    # Exit button
    exit_button = tk.Button(window, text="Exit", font=("Helvetica", 14), width=15, command=window.quit)
    exit_button.pack(pady=20)

#TODO: dynamic list size for levels depending on the number of levels in the folder (not harcoding it like it is now)
def level_selection():
    """Opens the level selection screen and hides the menu."""
    # Hide the main menu
    window.withdraw()

    # Create level selection window (replace it later with actual logic to load levels)
    level_selection_window = tk.Toplevel()
    level_selection_window.title("Select Level")
    level_selection_window.geometry("400x400")

    # Add buttons for levels
    levels = ["Level 1", "Level 2", "Level 3", "Level 4"]
    for i, level in enumerate(levels):
        level_button = tk.Button(level_selection_window, text=level, font=("Helvetica", 14), width=15,
                                 command=lambda lvl=i + 1: start_game(lvl, level_selection_window))
        level_button.pack(pady=10)

    # Back button to return to main menu
    back_button = tk.Button(level_selection_window, text="Back", font=("Helvetica", 14), width=15,
                            command=lambda: [level_selection_window.destroy(), window.deiconify()])
    back_button.pack(pady=20)

def start_game(level_number, level_selection_window):
    """Starts the game with the selected level."""
    global board
    # Hide the level selection window
    level_selection_window.withdraw()

    # Clear the main menu widgets
    clear_main_menu()

    # Load the selected level
    level_filename = f"Level{level_number}.txt"
    board = level_to_list(level_filename)
    print(board)  # DEBUG

    # Check if the level was loaded successfully
    if board is None:
        # Show an error message and return to the level selection screen
        error_label = tk.Label(window, text=f"Error loading {level_filename}!", font=("Helvetica", 16, "bold"))
        error_label.pack(pady=50)

        # Add a back button to return to the level selection screen
        back_button = tk.Button(window, text="Back", font=("Helvetica", 14), width=15,
                                command=lambda: [error_label.destroy(), window.deiconify()])
        back_button.pack(pady=20)

        return
    else:
        # Show the main window and start the game
        window.deiconify()
        level_selection_window.destroy()
        playgame(board)

def playgame(board):
    # Creates a new window and draws the board
    window.title("Sokoban - Game")
    global backgd, char, caisse, x_char, y_char, x_caisse, y_caisse, nbcaisses, nbcaisses_a_pousser, dim_case, board_init, movecount, pushcount, bestmoves, bestpushes
    backgd = tk.Canvas(window, width=len(board[0]) * dim_case, height=len(board) * dim_case, bg="#FFFFFF")

    #Set x_char and y_char to empty lists
    x_char = []
    y_char = []
    # Count the number of boxes on the board:
    nbcaisses = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '$':
                nbcaisses += 1
    # Make a copy of the board to reset the game
    board_init = copy.deepcopy(board)

    # Add scores and Reset button to the window, on the right side using rows and columns
    moves = tk.Label(window, text="Moves: " + str(movecount), font=("Helvetica", 16))
    moves.grid(row=0, column=len(board[0]), sticky='w')
    pushes = tk.Label(window, text="Pushes: " + str(pushcount), font=("Helvetica", 16))
    pushes.grid(row=1, column=len(board[0]), sticky='w')
    best_moves = tk.Label(window, text="Best Moves: " + str(bestmoves), font=("Helvetica", 16))
    best_moves.grid(row=2, column=len(board[0]), sticky='w')
    best_pushes = tk.Label(window, text="Best Pushes: " + str(bestpushes), font=("Helvetica", 16))
    best_pushes.grid(row=3, column=len(board[0]), sticky='w')
    reset = tk.Button(window, text="Reset", font=("Helvetica", 16), command=reset_game)
    reset.grid(row=4, column=len(board[0]), sticky='w')
    backToMenu = tk.Button(window, text="Back to Menu", font=("Helvetica", 16), command=main_menu)
    backToMenu.grid(row=5, column=len(board[0]), sticky='w')

    # Calculate the required window size
    window_width = len(board[0]) * dim_case + 200  # Additional space for scoreboards
    window_height = len(board) * dim_case + 100  # Additional space for scoreboards
    window.geometry(f"{window_width}x{window_height}")

    backgd.config(width=len(board[0]) * dim_case, height=len(board) * dim_case)
    for j in range(len(board[0])):
        for i in range(len(board)):
            x, y = j * dim_case, i * dim_case
            if board[i][j] == '#':  # Wall
                backgd.create_image(x, y, image=mur, anchor='nw')
            elif board[i][j] == '@':  # Personnage
                char = backgd.create_image(x, y, image=perso, anchor='nw')
                x_char.append(x)
                y_char.append(y)
            elif board[i][j] == '.':  # But
                backgd.create_image(x, y, image=hole, anchor='nw')
            elif board[i][j] == '$':  # Caisse
                x_caisse.append(i)
                y_caisse.append(j)
                caisse.append(backgd.create_image(x + 25, y + 25, image=box, anchor='center'))
            elif board[i][j] == '+':  # Character on hole
                char = backgd.create_image(x, y, image=perso, anchor='nw')
                x_char.append(x)
                y_char.append(y)
                backgd.create_image(x, y, image=hole, anchor='nw')
            elif board[i][j] == '*':  # Box on hole
                x_caisse.append(i)
                y_caisse.append(j)
                caisse.append(backgd.create_image(x + 25, y + 25, image=box, anchor='center'))
                backgd.create_image(x, y, image=hole, anchor='nw')
    backgd.tag_raise(char)
    for i in range(nbcaisses):
        backgd.tag_raise(caisse[i])

    # Use grid to place the Canvas
    backgd.grid(row=0, column=0, rowspan=len(board), columnspan=len(board[0]))

def check_win():
    global board, nbBoxesOnHoles, nbcaisses
    nbBoxesOnHoles = 0 #Reset the number of boxes on holes (fix to issue where the number of boxes on holes would be incremented with each move)
    for i in range(len(board)): #Check if the number of boxes on holes is equal to the number of boxes
        nbBoxesOnHoles += board[i].count('*')
    return nbBoxesOnHoles == nbcaisses

def win():
    global can_move, movecount, pushcount, backgd
    can_move = False
    backgd.create_text(len(board[0]) * dim_case // 2, len(board) * dim_case // 2, text="You win!", font=("Helvetica", 32, "bold"))

#TODO: movecount not resetting properly when movecount >= 10 !!!!!!!
def reset_game():
    global board, board_init, backgd, char, caisse, x_char, y_char, x_caisse, y_caisse, movecount, pushcount, bestmoves, bestpushes, can_move
    board = copy.deepcopy(board_init)
    backgd.delete("all")
    x_char.clear()
    y_char.clear()
    x_caisse.clear()
    y_caisse.clear()
    caisse.clear()
    movecount = 0
    moves = tk.Label(window, text="Moves: " + str(movecount), font=("Helvetica", 16))
    moves.grid(row=0, column=len(board[0]), sticky='w')
    pushcount = 0
    pushes = tk.Label(window, text="Pushes: " + str(pushcount), font=("Helvetica", 16))
    pushes.grid(row=1, column=len(board[0]), sticky='w')

    can_move = True
    playgame(board)

"""MOVEMENT FUNCTIONS"""
#TODO: fix bug when you psuh a box into another box for each direction
def up(evt):
    global x_char, y_char, backgd, movecount, char, board, caisse, pushes, can_move, pushcount

    if not can_move:
        return

    new_y = y_char[0] - 50
    current_x = x_char[0] // 50
    current_y = y_char[0] // 50
    next_y = new_y // 50

    if next_y < 0 or board[next_y][current_x] in ['#', '*']:
        return

    if board[next_y][current_x] == '$':
        new_box_y = new_y - 50
        next_box_y = new_box_y // 50

        if next_box_y < 0 or board[next_box_y][current_x] not in [' ', '.', '*']:
            return

        board[next_y][current_x] = ' '
        if board[next_box_y][current_x] == '.':
            board[next_box_y][current_x] = '*'
        else:
            board[next_box_y][current_x] = '$'

        for i in range(len(caisse)):
            coords = backgd.coords(caisse[i])
            if coords == [current_x * 50 + 25, new_y + 25]:
                backgd.coords(caisse[i], current_x * 50 + 25, new_box_y + 25)
                break

        pushcount += 1
        pushes = tk.Label(window, text="Pushes: " + str(pushcount), font=("Helvetica", 16))
        pushes.grid(row=1, column=len(board[0]), sticky='w')

    if board[current_y][current_x] == '+':
        board[current_y][current_x] = '.'
    else:
        board[current_y][current_x] = ' '

    if board[next_y][current_x] == '.':
        board[next_y][current_x] = '+'
    else:
        board[next_y][current_x] = '@'

    backgd.coords(char, x_char[0], new_y)
    y_char[0] = new_y

    movecount += 1
    # Update the movecount label
    moves = tk.Label(window, text="Moves: " + str(movecount), font=("Helvetica", 16))
    moves.grid(row=0, column=len(board[0]), sticky='w')

    if check_win():
        win()

def left(evt):
    global x_char, y_char, backgd, movecount, char, board, caisse, pushes, can_move, pushcount

    if not can_move:
        return

    new_x = x_char[0] - 50
    current_x = x_char[0] // 50
    current_y = y_char[0] // 50
    next_x = new_x // 50

    if next_x < 0 or board[current_y][next_x] in ['#', '*']:
        return

    if board[current_y][next_x] == '$':
        new_box_x = new_x - 50
        next_box_x = new_box_x // 50

        if next_box_x < 0 or board[current_y][next_box_x] not in [' ', '.', '*']:
            return

        board[current_y][next_x] = ' '
        if board[current_y][next_box_x] == '.':
            board[current_y][next_box_x] = '*'
        else:
            board[current_y][next_box_x] = '$'

        for i in range(len(caisse)):
            coords = backgd.coords(caisse[i])
            if coords == [new_x + 25, current_y * 50 + 25]:
                backgd.coords(caisse[i], new_box_x + 25, current_y * 50 + 25)
                break

        pushcount += 1
        pushes = tk.Label(window, text="Pushes: " + str(pushcount), font=("Helvetica", 16))
        pushes.grid(row=1, column=len(board[0]), sticky='w')

    if board[current_y][current_x] == '+':
        board[current_y][current_x] = '.'
    else:
        board[current_y][current_x] = ' '

    if board[current_y][next_x] == '.':
        board[current_y][next_x] = '+'
    else:
        board[current_y][next_x] = '@'

    backgd.coords(char, new_x, y_char[0])
    x_char[0] = new_x

    movecount += 1
    moves = tk.Label(window, text="Moves: " + str(movecount), font=("Helvetica", 16))
    moves.grid(row=0, column=len(board[0]), sticky='w')

    if check_win():
        win()

def down(evt):
    global x_char, y_char, backgd, movecount, char, board, caisse, pushes, can_move, pushcount

    if not can_move:
        return

    new_y = y_char[0] + 50
    current_x = x_char[0] // 50
    current_y = y_char[0] // 50
    next_y = new_y // 50

    if next_y >= len(board) or board[next_y][current_x] in ['#', '*']:
        return

    if board[next_y][current_x] == '$':
        new_box_y = new_y + 50
        next_box_y = new_box_y // 50

        if next_box_y >= len(board) or board[next_box_y][current_x] not in [' ', '.', '*']:
            return

        board[next_y][current_x] = ' '
        if board[next_box_y][current_x] == '.':
            board[next_box_y][current_x] = '*'
        else:
            board[next_box_y][current_x] = '$'

        for i in range(len(caisse)):
            coords = backgd.coords(caisse[i])
            if coords == [current_x * 50 + 25, new_y + 25]:
                backgd.coords(caisse[i], current_x * 50 + 25, new_box_y + 25)
                break

        pushcount += 1
        pushes = tk.Label(window, text="Pushes: " + str(pushcount), font=("Helvetica", 16))
        pushes.grid(row=1, column=len(board[0]), sticky='w')

    if board[current_y][current_x] == '+':
        board[current_y][current_x] = '.'
    else:
        board[current_y][current_x] = ' '

    if board[next_y][current_x] == '.':
        board[next_y][current_x] = '+'
    else:
        board[next_y][current_x] = '@'

    backgd.coords(char, x_char[0], new_y)
    y_char[0] = new_y

    movecount += 1
    moves = tk.Label(window, text="Moves: " + str(movecount), font=("Helvetica", 16))
    moves.grid(row=0, column=len(board[0]), sticky='w')

    if check_win():
        win()

def right(evt):
    global x_char, y_char, backgd, movecount, char, board, caisse, pushes, can_move, pushcount

    if not can_move:
        return

    new_x = x_char[0] + 50
    current_x = x_char[0] // 50
    current_y = y_char[0] // 50
    next_x = new_x // 50

    #TODO: fix bug when you psuh a box into another box for each direction
    if next_x >= len(board[0]) or board[current_y][next_x] in ['#', '*']:
        return

    if board[current_y][next_x] == '$':
        new_box_x = new_x + 50
        next_box_x = new_box_x // 50

        if next_box_x >= len(board[0]) or board[current_y][next_box_x] not in [' ', '.', '*']:
            return

        board[current_y][next_x] = ' '
        if board[current_y][next_box_x] == '.':
            board[current_y][next_box_x] = '*'
        else:
            board[current_y][next_box_x] = '$'

        for i in range(len(caisse)):
            coords = backgd.coords(caisse[i])
            if coords == [new_x + 25, current_y * 50 + 25]:
                backgd.coords(caisse[i], new_box_x + 25, current_y * 50 + 25)
                break

        pushcount += 1
        pushes = tk.Label(window, text="Pushes: " + str(pushcount), font=("Helvetica", 16))
        pushes.grid(row=1, column=len(board[0]), sticky='w')

    if board[current_y][current_x] == '+':
        board[current_y][current_x] = '.'
    else:
        board[current_y][current_x] = ' '

    if board[current_y][next_x] == '.':
        board[current_y][next_x] = '+'
    else:
        board[current_y][next_x] = '@'

    backgd.coords(char, new_x, y_char[0])
    x_char[0] = new_x

    movecount += 1
    moves = tk.Label(window, text="Moves: " + str(movecount), font=("Helvetica", 16))
    moves.grid(row=0, column=len(board[0]), sticky='w')

    if check_win():
        win()

#END GAME FUNCTIONS------------------------------------------------
#COMMANDES--------------------------------------------------------
window.bind_all('<z>', up)
window.bind_all('<q>', left)
window.bind_all('<s>', down)
window.bind_all('<d>', right)
#END COMMANDES----------------------------------------------------

main_menu()
window.mainloop()