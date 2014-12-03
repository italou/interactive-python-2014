"""
Week 2 Mini-project

Descprition: Implementation of "Guess the number" game
     Author: Itamar M. B. Lourenço
       Date: 2014-10-06
"""

# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math


# globals
secret_number = 0
low = 0
high = 100
guess_remaining = 7


# helper functions

def new_game():
    """ Starts (and restarts) a game """
    # initialize global variables used
    global secret_number, guess_remaining
    secret_number = random.randrange(low,high)
    
    # resets available attempts
    guess_remaining = int(math.ceil(math.log(high - low + 1, 2)))
    
    print "New game. Range is from", low, "to", high
    print "Number of remaining guesses is", guess_remaining 
#    print "secret_number:", secret_number
    print ""
    
def has_attempts_left():
    """ verifies if player has any attempt(s) left """
    if guess_remaining > 0:
        return True
    else:
        print "You ran out of guesses. The number was", secret_number
        return False    

    
# define event handlers for control panel

def range100():
    # button that changes the range to [0,100) and starts a new game
    global high, low
    low = 0
    high = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game
    global high, low
    low = 0
    high = 1000
    new_game()
    
def input_guess(guess):
    """ Validates guess number and remaining attempts left"""
    global guess_remaining
    
    # checks if input is a valid number
    if guess.isdigit():
        if has_attempts_left():
            print "Guess was", guess
                
            guess_remaining -= 1
            print "Number of remaining guesses is", guess_remaining
    
            # main game logic goes here
            if int(guess) < secret_number:
                if has_attempts_left():
                    print "Higher!"
            elif int(guess) > secret_number:
                if has_attempts_left():
                    print "Lower!"
            else:
                print "Correct!"
                print""
                new_game()
                
    else:
        print "Please, enter a valid number!"
    print ""

    
# create frame
frame = simplegui.create_frame("Guess the Number!", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
frame.add_button("New Game", new_game, 200)

inp = frame.add_input('Enter a guess:', input_guess, 200)

frame.start()


# call new_game 
new_game()