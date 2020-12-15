import json
import random
from guess import Guess

class Game:
    def __init__(self, *, allow_repeat=False, unique_digits=6, num_digits=4, guesses=10):
        self.secret = self.get_secret(allow_repeat, unique_digits, num_digits)
        self.num_guesses = guesses
        self.used_guesses = 0
        self.history = []
        if unique_digits == 10:
            self.allowed_digits = set(map(str, range(10)))
        else:
            self.allowed_digits = set(map(str, range(1, unique_digits+1)))
        self.num_digits = num_digits

    def get_secret(self, allow_repeats: bool, distinct_digits: int, num_digits: int) -> str:
        '''
            Generate the secret number

            Parameters:
                num_digits:      Integer. The length of the secret number.
                allow_repeats:   Boolean. Whether digits are allowed to repeat.
                distinct_digits: Integer. The number of distinct digites allowed.

            Returns:
                The secret number as a string.
        '''
        if allow_repeats and distinct_digits == 10:
            return str(random.randrange(10**(num_digits-1), 10**num_digits))
        secret = []
        while len(secret) < num_digits:
            n = random.randrange(1,distinct_digits+1)
            if allow_repeats or n not in secret:
                secret.append(n)

    def get_json_response(self, *, status=None, message=None, secret=False, hint=None):
        resp = {}
        resp['status'] = status
        resp['guesses'] = self.num_guesses - self.used_guesses
        if secret:
            resp['secret'] = self.secret
        if message:
            resp['message'] = message
        if hint:
            resp['hint'] = hint
        return json.dumps(resp)
    
    def get_hint(self, guess):
        s = '<tr>'
        for _ in guess.right:
            s += '<td class="right">X</td>'
        for _ in guess.close:
            s += '<td class="close">O</td>'
        for _ in range(self.num_digits - guess.right - guess.close):
            s += '<td class="wrong">-</td>'
        return s + '</tr>'


    def get_digits(self):
        dig = sorted(self.allowed_digits)
        s = ', '.join(dig[:-1])
        s += f', and {dig[-1]}'
        return s

    def get_response(self, hint):
        if hint.isAWin:
            status = 'win'
            secret = self.secret
        elif self.used_guesses == self.num_guesses:
            status = 'lose'
            secret = self.secret
        else:
            status = 'continue'
            secret = None
        return self.get_json_response(status=status, secret=secret, hint=self.get_hint(hint))

    def process_guess(self, guess):
        if len(guess) != self.num_digits:
            return self.get_json_response(status='error', message=f'Guess must be {self.num_digits} long.')
        for n in guess:
            if n not in self.allowed_digits:
                return self.get_json_response(status='error', message=f'Only {self.get_digits()} are allowed.')
        self.used_guesses += 1
        hint = Guess(self.secret, guess)
        self.history.append(hint)
        return self.get_response(hint)

    def get_status(self):
        if self.history:
            return self.get_response(self.history[-1])
        return self.get_json_response(status='continue', hint=' ')

    def in_progress(self):
        if self.history:
            if self.history[-1].isAWin:
                return 'Player won'
            if self.used_guesses == self.num_guesses:
                return 'Computer won'
            else:
                return f'{self.num_guesses - self.used_guesses} guesses remaining.'
        return f'No guesses made. {self.num_guesses} remaining.'       