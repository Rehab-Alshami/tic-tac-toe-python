from tkinter import *
from tkinter import messagebox
current_player=None
game_running=False
root = Tk()
root.title("Tic-Tac-Toe")
# To choose game mode
play_with_var = StringVar()
play_with_var.set("computer")
Label(root, text="Play With").grid(row=0, column=0, sticky="w")

Radiobutton(root, text="Computer", variable=play_with_var, value="computer").grid(row=0, column=1)
Radiobutton(root, text="Player 2", variable=play_with_var, value="player2").grid(row=0, column=2)

# To choose letter (X or O)
letter_var = StringVar()
letter_var.set("X")
Label(root, text="Select").grid(row=1, column=0, sticky="w")

Radiobutton(root, text="X", variable=letter_var, value="X").grid(row=1, column=1)
Radiobutton(root, text="O", variable=letter_var, value="O").grid(row=1, column=2)

# To choose who starts
start_var = StringVar()
start_var.set("yes")
Label(root, text="Start the game").grid(row=2, column=0, sticky="w")

Radiobutton(root, text="Yes", variable=start_var, value="yes").grid(row=2, column=1)
Radiobutton(root, text="No", variable=start_var, value="no").grid(row=2, column=2)


board = {i: " " for i in range(1, 10)}
buttons = {}

# To reset a board
def reset_board():
    for i in range(1, 10):
        board[i] = " "
        if i in buttons:
            buttons[i]["text"] = " "


# Start 
def on_start():
    global current_player, game_running, player_letter, comp_letter
    reset_board()  
    first_letter = letter_var.get()           
    other_letter = "O" if first_letter == "X" else "X"

    player_letter = first_letter
    comp_letter = other_letter

    #Start a game
    if start_var.get() == "yes":
        current_player = first_letter
    else:
        current_player = other_letter
    game_running = True
    messagebox.showinfo("Start", "Game started")

    if play_with_var.get() == "computer" and current_player == comp_letter:
        pos = get_computer_move(comp_letter, player_letter)
        board[pos] = comp_letter
        buttons[pos]["text"] = comp_letter

        if check_win(comp_letter):
            messagebox.showinfo("Winner", f"Computer ({comp_letter}) wins")
            game_running = False
            return

        if is_draw():
            messagebox.showinfo("Draw", "It is a draw")
            game_running = False
            return

        current_player = player_letter


# Start Button
Button(root, text="Start", command=on_start).grid(row=3, column=2, pady=10)


def on_cell_click(pos):
    global current_player, game_running
    if not game_running:
        messagebox.showwarning("Warning", "Press Start Button")
        return

    if board[pos] != " ":
        messagebox.showwarning("Warning", "This cell is full")
        return

    board[pos] = current_player
    buttons[pos]["text"] = current_player

    if check_win(current_player):
        messagebox.showinfo("Winner", f"Player {current_player} wins")
        game_running = False

        again=messagebox.askyesno("play again","Do you want to play again?")
        if again:
            on_start
        else:
            root.destroy()
        return
    if is_draw():
        messagebox.showinfo("Draw", "It is a draw")
        game_running = False

        again=messagebox.askyesno("play again","Do you want to play again?")
        if again:
            on_start
        else:
            root.destroy()
        return


    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"

    
    if play_with_var.get() == "computer" and current_player == comp_letter:
        pos = get_computer_move(comp_letter, player_letter)
        board[pos] = comp_letter
        buttons[pos]["text"] = comp_letter

        if check_win(comp_letter):
            messagebox.showinfo("Winner", f"Computer ({comp_letter}) wins")
            game_running = False

            again=messagebox.askyesno("play again","Do you want to play again?")
            if again:
              on_start
            else:
             root.destroy()
            return

        if is_draw():
            messagebox.showinfo("Draw", "It is a draw")
            game_running = False
            again=messagebox.askyesno("play again","Do you want to play again?")
            if again:
              on_start
            else:
             root.destroy()
            return

        current_player = player_letter


def check_win_sim(test_board, player):
    win_combos = [
        (1,2,3),(4,5,6),(7,8,9),
        (1,4,7),(2,5,8),(3,6,9),
        (1,5,9),(3,5,7)
    ]
    for c in win_combos:
        if (test_board[c[0]] == player and
            test_board[c[1]] == player and
            test_board[c[2]] == player):
            return True
    return False

# To make computer play in smart
def get_computer_move(comp_letter, player_letter):
    for pos in board:
        if board[pos] == " ":
            board_copy = board.copy()
            board_copy[pos] = player_letter
            if check_win_sim(board_copy, player_letter):
                return pos

    for pos in board:
        if board[pos] == " ":
            board_copy = board.copy()
            board_copy[pos] = comp_letter
            if check_win_sim(board_copy, comp_letter):
                return pos

    if board[5] == " ":
        return 5

    for corner in [1, 3, 7, 9]:
       if board[corner] == " ":
            return corner

    for pos in board:
        if board[pos] == " ":
            return pos

    return None


def build_board():
    pos = 1
    for r in range(4, 7):         
        for c in range(0, 3):     
            btn = Button(root, text=" ", width=6, height=3,
             bg="gray", activebackground="gray",
             command=lambda p=pos: on_cell_click(p))
            btn.grid(row=r, column=c, padx=2, pady=2)
            buttons[pos] = btn
            pos += 1

build_board()


#To chack is free or not 
def is_free(pos):
    return board[pos] == " "

#To check if win
def check_win(player):
    win_combos = [
        (1,2,3), (4,5,6), (7,8,9),   
        (1,4,7), (2,5,8), (3,6,9),   
        (1,5,9), (3,5,7)             
    ]
    for combo in win_combos:
        if (board[combo[0]] == player and
            board[combo[1]] == player and
            board[combo[2]] == player):
            return True
    return False

#To check if draw
def is_draw():
    return all(board[pos] != " " for pos in board)

root.mainloop()
