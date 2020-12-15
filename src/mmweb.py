from game import Game
from flask import Flask, render_template, request
import uuid

app = Flask(__name__)

games = {}

@app.route('/games')
def get_games():
    s = ''
    for game in games.values():
        s += f'<tr><td>{game.get_status()}</tr></td>'
    return render_template('status.html', table_contents=s)

