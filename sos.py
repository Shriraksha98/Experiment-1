import tkinter as tk
from tkinter import messagebox
import random

# Initialize the board
board = [' ' for _ in range(25)]  # 5x5 grid
human_score = 0
ai_score = 0

# Function to find all SOS sequences
def find_sos(board):
    sos_positions = []
    size = 5
    # Rows
    for r in range(size):
        for c in range(size - 2):
            idxs = [r*size + c, r*size + c+1, r*size + c+2]
            if ''.join(board[i] for i in idxs) == "SOS":
                sos_positions.append(idxs)
    # Columns
    for c in range(size):
        for r in range(size - 2):
            idxs = [r*size + c, (r+1)*size + c, (r+2)*size + c]
            if ''.join(board[i] for i in idxs) == "SOS":
                sos_positions.append(idxs)
    # Diagonals (top-left to bottom-right)
    for r in range(size - 2):
        for c in range(size - 2):
            idxs = [r*size + c, (r+1)*size + c+1, (r+2)*size + c+2]
            if ''.join(board[i] for i in idxs) == "SOS":
                sos_positions.append(idxs)
    # Diagonals (top-right to bottom-left)
    for r in range(size - 2):
        for c in range(2, size):
            idxs = [r*size + c, (r+1)*size + c-1, (r+2)*size + c-2]
            if ''.join(board[i] for i in idxs) == "SOS":
                sos_positions.append(idxs)
    return sos_positions

# Function to check if board is full
def is_draw(board):
    return ' ' not in board

# Award points only for new SOS formed by the latest move
def award_points(player, index):
    global human_score, ai_score
    sos_positions = find_sos(board)
    for seq in sos_positions:
        if index in seq:  # if the last move created SOS
            if player == "Human":
                human_score += 1
            else:
                ai_score += 1

# Smarter AI move: randomized + competitive
def best_move(board):
    empty_cells = [i for i in range(25) if board[i] == ' ']
    if not empty_cells:
        return -1, None

    random.shuffle(empty_cells)  # shuffle to avoid serial order

    best_score = -1
    best_choice = (-1, None)

    for i in empty_cells:
        for letter in ['S', 'O']:
            board[i] = letter
            sos_positions = find_sos(board)
            score_gain = sum(1 for seq in sos_positions if i in seq)
            board[i] = ' '

            if score_gain > best_score:
                best_score = score_gain
                best_choice = (i, letter)

    # If no scoring move, fallback to random
    if best_choice[0] == -1:
        return random.choice(empty_cells), random.choice(['S', 'O'])
    return best_choice

# Handle button click (Human move)
def on_click(index, letter):
    if board[index] != ' ':
        return

    board[index] = letter
    buttons[index].config(text=letter, fg="blue")

    # Award human points
    award_points("Human", index)
    highlight_sos()
    update_score()

    if is_draw(board):
        announce_winner()
        return

    # AI move
    ai_index, ai_letter = best_move(board)
    if ai_index != -1:
        board[ai_index] = ai_letter
        buttons[ai_index].config(text=ai_letter, fg="red")

        # Award AI points
        award_points("AI", ai_index)
        highlight_sos()
        update_score()

        if is_draw(board):
            announce_winner()
            return

# Reset the board
def reset_game():
    global board, human_score, ai_score
    board = [' ' for _ in range(25)]
    human_score = 0
    ai_score = 0
    for btn in buttons:
        btn.config(text=' ', bg="SystemButtonFace")
    update_score()

# Update score display
def update_score():
    score_label.config(text=f"Human: {human_score}   AI: {ai_score}")

# Announce winner based on scores
def announce_winner():
    if human_score > ai_score:
        messagebox.showinfo("Game Over", f"Final Score\nHuman: {human_score} | AI: {ai_score}\n🎉 You win!")
    elif ai_score > human_score:
        messagebox.showinfo("Game Over", f"Final Score\nHuman: {human_score} | AI: {ai_score}\n🤖 AI wins!")
    else:
        messagebox.showinfo("Game Over", f"Final Score\nHuman: {human_score} | AI: {ai_score}\nIt's a draw!")
    reset_game()

# Highlight SOS sequences on the board
def highlight_sos():
    for btn in buttons:
        btn.config(bg="SystemButtonFace")  # reset colors
    sos_positions = find_sos(board)
    for seq in sos_positions:
        for idx in seq:
            buttons[idx].config(bg="yellow")  # highlight SOS

# GUI setup
root = tk.Tk()
root.title("SOS Game (5x5 Grid with Competitive Random AI)")

buttons = []
for i in range(25):
    btn = tk.Button(root, text=' ', font=('Arial', 18, 'bold'),
                    width=4, height=2)
    btn.grid(row=i // 5, column=i % 5)
    buttons.append(btn)

# Control panel for choosing S or O
frame = tk.Frame(root)
frame.grid(row=5, column=0, columnspan=5)

s_btn = tk.Button(frame, text="Place S", font=('Arial', 14),
                  command=lambda: set_letter('S'))
s_btn.pack(side="left", padx=10)

o_btn = tk.Button(frame, text="Place O", font=('Arial', 14),
                  command=lambda: set_letter('O'))
o_btn.pack(side="left", padx=10)

reset_btn = tk.Button(frame, text="Reset", font=('Arial', 14),
                     command=reset_game)
reset_btn.pack(side="left", padx=10)

score_label = tk.Label(frame, text="Human: 0   AI: 0", font=('Arial', 14))
score_label.pack(side="left", padx=20)

# Track current letter choice
current_letter = 'S'
def set_letter(letter):
    global current_letter
    current_letter = letter
    for i, btn in enumerate(buttons):
        btn.config(command=lambda i=i: on_click(i, current_letter))

# Initialize with S
set_letter('S')

root.mainloop()
