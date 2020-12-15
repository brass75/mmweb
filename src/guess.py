from collections import Counter

class Guess:
    def __init__(self, secret: str, guess: str):
        '''
            Constructor for the Guess class

            Parameters:
                secret:     The secret number
                guess:      The guessed number
            
            Returns:
                A Guess object
        '''
        close = 0
        right = 0
        count = Counter(secret)
        for i, c in enumerate(guess):
            if i < len(secret) and secret[i] == c:
                right += 1
                if count[c]:
                    count[c] -= 1
                else:
                    close -= 1
            elif c in count and count[c]:
                close += 1
                count[c] -= 1
        self.length = len(secret)
        self.guess = guess
        self.res = {'right': right, 'close': close}

    def __str__(self):
        '''
            Return the string representation of a guess.
        '''
        s = ''
        s += 'X' * self.res['right']
        s += 'O' * self.res['close']
        s += '-' * (len(self.guess) - len(s))
        s += ' ' + self.guess
        return s
    

    @property
    def isAWin(self):
        '''
            Property to return whether the guess was a winning guess.
        '''
        return self.right == self.length
    
    @property
    def right(self):
        '''
            Property to return the number of correct (correct number and correct place) digits in the guess.
        '''
        return self.res['right']

    @property
    def close(self):
        '''
            Property to return the number of close (correct number but incorrect place) digits in the guess.
        '''
        return self.res['close']
