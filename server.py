from flask import Flask, request
import urllib.request
from flask_socketio import SocketIO, emit, join_room, leave_room
import random


# Server Configuration
app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*")
print("Server is running... Waiting for connections")

questions = [
    'What is your name?',
    'What is your age?'
]

'''
url = 'https://fti.free.nf/fetch.php'


response = urllib.request.urlopen(url)
data1 = response.read().decode()  # Decode the byte response to string
print(data1)  # Print the content of the response
'''


players = []
answers = []
player_answer_dict = {}


@sio.on("test")
def test(data):
    d = data.get("test")
    print(d)

@sio.on("user")
def join_game(data):
    username = data.get("user")
    print(username)
    sio.emit('join_game', {'users': username})

@sio.on("start_game")
def start_game(data):
    global question
    global impostor_question
    users = data.get('start')
    players.append(users)
    impostor = random.choice(users)
    print('Impostor: ' , impostor)
    question = random.choice(questions)
    print('question: ', question)
    impostor_question = random.choice(questions)
    while question == impostor_question:
        impostor_question = random.choice(questions)
    print('Impostor question: ',impostor_question)
    for i in users:
        if i == impostor:
            print(impostor_question)
            sio.emit("question", {'question': impostor_question})
        else:
            print(question)
            sio.emit("question", {'quesiton': question})

@sio.on('answer_submitted')
def answer_submitted(data):
    user_answer_dict = data.get('answers')
    for user, answer in user_answer_dict.items():
        print(f'check for dicts {user, answer, user_answer_dict}')
        player_answer_dict[user] = answer
        answers.append(answer)


    if len(players) == len(answers):
        sio.emit('display_answer', {'reveal': player_answer_dict})


@sio.on('question_reveal')
def question_reveal(data):
    x = data.get('quesiton')
    sio.emit('q_reveal', {'question': question})

if __name__ == "__main__":
    sio.run(app, host="0.0.0.0", port=10000, allow_unsafe_werkzeug=True, debug=True)