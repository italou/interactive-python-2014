"""
Week 5 Mini-project

Descprition: Implementation of the Memory card game
     Author: Itamar M. B. Lourenço
       Date: 2014-10-23
"""
# imports
import simplegui
import random

# global variables
state = 0 # card choice state
deck = [] # deck of 16 cards
exposed = []  # list of exposed cards
turned_card1 = -1 # previous cards turned
turned_card2 = -1 # previous cards turned
num_of_turns = 0 # number of turns made
# card back image link
cardback_img = simplegui.load_image("http://dl.dropbox.com/s/vmgqicyjofb6382/cardback.jpg")

# True for showing debug information
DEBUG = False
#DEBUG = True


# helper functions
def new_game():
    """Start a new game."""
    global state, deck, turned_card1, turned_card2, exposed, num_of_turns
    deck = range(0, 8) + range(0, 8) # creates the deck
    random.shuffle(deck) # shuffles the cards
    # reset the cards position, exposed (true) or face down (false)
    exposed = [False for x in range(0, len(deck))]
    # reset game variables
    state = 0
    turned_card1 = -1
    turned_card2 = -1
    num_of_turns = 0
    label.set_text("Turns =")


# event handlers
def mouseclick(pos):
    """Mouseclick event handler
    
    :param pos: pair of screen coordinates
    """
    global state, exposed, turned_card1, turned_card2, num_of_turns
    current_card = pos[0] // 50 # get card number from clicked (x) position
    # if card is not exposed, does game logic. Else does nothing
    if not exposed[current_card]:
        exposed[current_card] = True # expose the card
        if state == 0: # if no card has been exposed (and one is clicked)
            turned_card1 = current_card # saves clicked card position/index
            state = 1 # advance state
        elif state == 1: # if one card has been exposed (and one is clicked)
            turned_card2 = current_card # saves clicked card position/index
            state = 2 # advance state
            num_of_turns += 1 # adds 1 turn to counter
        else: # if two cards had been turned (and a third one, not exposed, was clicked)
            if not deck[turned_card1] == deck[turned_card2]: # check if exposed cards match
                # if don't match, turn back over cards (already exposed on previous states)
                exposed[turned_card1] = False
                exposed[turned_card2] = False
            turned_card1 = current_card # saves clicked card position/index
            state = 1 # go to previous state (1 card exposed and 1 to choose)
    
def draw(canvas):
    """Draw handler."""
    global exposed
    card_number = 0 # to save card index in iteration
    for card in deck: # iterates card list (deck)
        if not exposed[card_number]: # if card is not exposed/turned
            # draw back of the card (rectangle)
            canvas.draw_polygon([[card_number * 50, 0], [card_number * 50 + 50, 0],
                             [card_number * 50 + 50, 100], [card_number * 50, 100]],
                            1, "White", "Maroon")
            # draw image of card back
            canvas.draw_image(cardback_img, [25, 50], [50, 100],
                              [card_number * 50 + 25 + 1, 50], [50 - 2, 100]) # - 2 to look better
            if DEBUG: # for debug only
                canvas.draw_text(str(deck[card_number]),
                                 [card_number * 50 + 8, 73], 70, "Silver")
        else: # if card is exposed
            # draw front of the card (rectangle)
            canvas.draw_polygon([[card_number * 50, 0], [card_number * 50 + 50, 0],
                             [card_number * 50 + 50, 100], [card_number * 50, 100]],
                            1, "Maroon", "White")
            # draw number of the card
            canvas.draw_text(str(deck[card_number]), [card_number * 50 + 8, 73], 70, "Black")
        if DEBUG: # for debug only
            canvas.draw_text(str(exposed[card_number]),
                             [card_number * 50 + 10, 95], 14, "Silver")
        card_number += 1 # increments card number/index, to move to next one.
    label.set_text("Turns = " + str(num_of_turns)) # updates number of turns

# create frame and add a button and labels
frame = simplegui.create_frame("Memory Card Game", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns =")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()