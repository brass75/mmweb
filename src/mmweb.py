from game import Game
from flask import Flask, render_template, request
import uuid
import os
import json

app = Flask(__name__)

DEFAULT_PORT=8080
CONFIG_FILE='config.json'
STYLE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'styles'))
SCRIPT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

games = {}


@app.route('/games')
def get_games():
    return render_template('status.html', gvals=map(json.loads, [game.get_status() for game in games.values()]))

@app.route('/')
@app.route('/new_game.html')
def new_game():
    return render_template('new_game.html')

@app.route('/play.html/<game_id>/<guess>')
def play_game(game_id, guess):
    if game_id not in games:
        return(json.dumps({
            'status': 'error',
            'message': 'game not found'
        }))
    game = games[game_id]
    print (game)
    status = json.loads(game.get_status())['status']
    if status == 'new' or status == 'continue':
        return game.process_guess(guess)
    return game.get_status()
 

@app.route('/game.html', methods=['POST'])
def start_game():
    game = Game(
                allow_repeat='allow_repeats' in request.form,
                unique_digits=int(request.form['unique_digits']),
                guesses=int(request.form['num_guesses']),
                num_digits=int(request.form['num_digits'])
            )    
    game_id = str(uuid.uuid4())
    games[game_id] = game
    return render_template('play.html', game_id=game_id, 
                           num_digits=int(request.form['num_digits']), 
                           num_guesses=int(request.form['num_guesses']),
                           allow_repeats='allow_repeats' in request.form,
                           unique_digits=int(request.form['unique_digits']))

@app.route('/styles/<file>')
def get_style(file):
    '''
    Function to read and return a stylesheet file
    '''
    if os.path.exists(os.path.join(STYLE_DIR, file)):
        with open(os.path.join(STYLE_DIR, file)) as f:
            return f.read()
    return (f'Unable to find {file}', 404)


@app.route('/scripts/<file>')
def get_script(file):
    '''
    Function to read and return a stylesheet file
    '''
    if os.path.exists(os.path.join(SCRIPT_DIR, file)):
        with open(os.path.join(SCRIPT_DIR, file)) as f:
            return f.read()
    return (f'Unable to find {file}', 404)

if __name__ == '__main__':
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    port = config.get('port', DEFAULT_PORT)
    app.run('0.0.0.0', port, debug=True)