import tkinter as tk
from tkinter import messagebox, scrolledtext
import socketio
import threading
import time
import random

SERVER_URL = "http://127.0.0.1:10000"  # Replace with your server URL
sio = socketio.Client()

# Connect to the server before emitting any event
sio.connect(SERVER_URL)

# Emit an event after a successful connection
sio.emit("test", {"test": 'test'})


#vars

users = []
answers = {}

def join_game():
    user = name_entry.get()
    sio.emit("user", {'user': user})

def start_game_request():
    sio.emit('start_game', {'start': users})

@sio.on('question')
def question_received(data):
    quesiton = data.get('question')
    question_label.config(text=quesiton)


@sio.on('display_answer')
def display_answer(data):
    user_answer_dict = data.get('reveal')
    print('answer to be displayed')
    status_label.config(text='All players have submitted their answers as below')
    reveal_answer_label.config(text=f'{user_answer_dict}')



@sio.on('join_game')
def game_ui(data):
    global status_label
    global question_label
    global reveal_answer_label

    joined_user = data.get('users')
    users.append(joined_user)
    print('hello world')
    game_window = tk.Toplevel(root)
    game_window.title("Find The Impostor")
    game_window.geometry("600x600")

    # Create a frame with some padding
    frame = tk.Frame(game_window, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    #
    # # Game controls (for all players, but only first can use it)
    control_frame = tk.Frame(frame)
    control_frame.pack(fill=tk.X, pady=5)

    check = tk.Label(control_frame,  text=f'Players joined: {users}')
    check.pack()

    # Check if we're the first player by seeing if the list is empty before we joined
    is_first_player = users[0] == joined_user

    start_button = tk.Button(control_frame, text="Start Game", command=start_game_request)
    # # Only the first player can start the game
    if is_first_player:
        start_button.config(state=tk.NORMAL)
    else:
        start_button.config(state=tk.DISABLED)
    start_button.pack(side=tk.LEFT, padx=5)

    question_label = tk.Label(control_frame, text='Waiting for the game to start, you question will appear here once the host has started the game')
    question_label.pack()

    # Answer section
    answer_frame = tk.Frame(frame)
    answer_frame.pack(pady=10, fill=tk.X)

    tk.Label(answer_frame, text="Your Answer:").pack(side=tk.LEFT)
    answer_entry = tk.Entry(answer_frame, width=40, state=tk.NORMAL)
    answer_entry.pack(side=tk.LEFT, padx=5)

    def submit_answer():
        answer = answer_entry.get()
        if not answer:
            messagebox.showerror("Error", "Please enter an answer")
            return

        answers[joined_user] = answer
        #sio.emit("submit_answer", {"answer": answer, "name": name})
        answer_entry.delete(0, tk.END)
        answer_entry.config(state=tk.DISABLED)
        status_label.config(text='Answer submitted, waiting for others...')
        sio.emit('answer_submitted', {'answers': answers})

    submit_btn = tk.Button(answer_frame, text="Submit", command=submit_answer)
    submit_btn.pack(side=tk.LEFT, padx=5)

    status_frame = tk.Frame(frame)
    status_frame.pack(pady=10, fill=tk.X)

    status_label = tk.Label(status_frame, text='Status label')
    status_label.pack()

    reveal_answer_label = tk.Label(status_frame, text="Reveal Answer Label")
    reveal_answer_label.pack()







    # timer_label = tk.Label(control_frame, text="Waiting to start...", font=("Arial", 10, "bold"))
    # timer_label.pack(side=tk.RIGHT, padx=5)
    #
    # # Status section
    # if is_first_player:
    #     status_text = "You are the host. Click Start Game when everyone has joined."
    # else:
    #     status_text = "Waiting for host to start the game..."
    #
    # status_label = tk.Label(frame, text=status_text, font=("Arial", 10, "italic"), wraplength=560)
    # status_label.pack(pady=5, fill=tk.X)
    #
    # # Question section - hidden until game starts
    # question_label = tk.Label(frame, text="Waiting for game to start...", font=("Arial", 12, "bold"), wraplength=560)
    # question_label.pack(pady=10, fill=tk.X)
    #
    # # Answer section
    # answer_frame = tk.Frame(frame)
    # answer_frame.pack(pady=10, fill=tk.X)
    #
    # tk.Label(answer_frame, text="Your Answer:").pack(side=tk.LEFT)
    # answer_entry = tk.Entry(answer_frame, width=40, state=tk.DISABLED)
    # answer_entry.pack(side=tk.LEFT, padx=5)



root = tk.Tk()
root.title("Find The Impostor - Login")
root.geometry("300x150")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="Enter Your Name:").pack(pady=5)
name_entry = tk.Entry(frame, width=25)
name_entry.pack(pady=5)

tk.Button(frame, text="Join Game", command=join_game).pack(pady=10)

root.mainloop()