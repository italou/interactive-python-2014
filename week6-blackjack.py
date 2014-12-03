"""
Week 6 Mini-project

Descprition: Implementation of (simple) Blackjack
     Author: Itamar M. B. Lourenço
       Date: 2014-10-26
"""

import simplegui
import random

# Images
# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

CHIP_SIZE = (20, 20)
CHIP_CENTER = (10, 10)
chip_image = simplegui.load_image("http://dl.dropbox.com/s/jm7ekgss56kn9e9/chip.png")

# global variables
in_play = False
table_deck = None
player_hand = None
player_msg = ""
dealer_hand = None
dealer_msg = ""
cash = 1000
bet = 5
allow_bet = True
total_won = 0
total_lost = 0

# globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# for debug info
DEBUG = True
#DEBUG = False


# Card class
class Card:
    """
    Card
    
    self.suit: Suit of the card
    self.rank: Rank of the card
    """
    def __init__(self, suit, rank):
        """
        Initizalize the card.
        
        :param suit: Suit of the card
        :type suit: string
        :param rank: Rank of the card
        :type rank: string
        """
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        """
        Readable representation of the card.
        
        :return: string
        """
        return self.suit + self.rank

    def get_suit(self):
        """
        Get card suit.
        
        :return: string
        """
        return self.suit

    def get_rank(self):
        """
        Get card rank.
        
        :return: string
        """
        return self.rank

    def draw(self, canvas, pos):
        """
        Draw card on canvas.
        
        :param canvas: Canvas for drawing
        :type canvas: Canvas
        :param pos: upper left corner of card
        :type pos: tuple or list
        """
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


# Hand class
class Hand:
    """
    Hand
    
    self.hand_cards: Collection (list) of cards in the hand.
    """
    def __init__(self):
        """
        Initizalize the hand.
        """
        self.hand_cards = []

    def __str__(self):
        """
        Readable representation of the hand.
        
        :return: string
        """
        result = "Hand contains"
        if len(self.hand_cards) > 0:
            for i in range(len(self.hand_cards)):
                result += " " + str(self.hand_cards[i])
        #else:
        #    result += " no card"
        return result

    def add_card(self, card):
        """
        Add card to hand.
        
        :param card: Card to add
        :type suit: Card
        """
        self.hand_cards.append(card)

    def get_value(self):
        """
        Get value of hand.
        
        :return: int
        """
        # aces are first counted as 1
        value = 0
        if len(self.hand_cards) > 0:
            has_aces = 0
            for card in self.hand_cards:
                rank = str(card)[1]
                value += VALUES.get(rank)
                # check for aces
                if rank == "A":
                    has_aces = True       
            # if there is a Ace, compare final value to see if it doesn't bust
            if has_aces and value + 10 <= 21:
                value += 10 # if it doesn't bust, add 10 (count Ace as 11)
        return value
    
    def count(self, rank):
        """
        Counts the number of cards of a specific rank in the hand
        
        :param rank: Card rank
        :type rank: string
        :return: int
        """
        result = 0
        for card in self.hand_cards:
            if card.get_rank() == rank:
                result += 1
        return result
   
    def draw(self, canvas, pos):
        """
        Draw hand on canvas.
        
        :param canvas: Canvas for drawing
        :type canvas: Canvas
        :param pos: upper left corner of the leftmost card
        :type pos: tuple or list
        """
        card_index = 0
        card_row = 0
        # cards will be drawn as a grid of 7x2.
        # In the worst case, there will be 12 cards on one Hand.
        # A A A A 2 2 2 2 3 3 3 3 (value of 24)
        for card in self.hand_cards:
            card.draw(canvas, [card_index * CARD_SIZE[0] + pos[0],
                               card_row * CARD_SIZE[1] - card_row * CARD_CENTER[1]
                               + pos[1]])
            card_index += 1
            if card_index == 7:
                card_row +=1
                # set to 1 and not 0 so that dealer covered card doesn't overlap.
                card_index = 1

                
# Deck class 
class Deck:
    """
    Deck.
        
    self.deck_cards: Collection (list) of card in the deck.
    """
    def __init__(self):
        """
        Initizalize the deck.
        """
        self.deck_cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        """
        Shuffles the cards on the deck.
        """
        random.shuffle(self.deck_cards)

    def deal_card(self):
        """
        Deal a card from the deck.
        
        :return: Card
        """
        return self.deck_cards.pop()
    
    def __str__(self):
        """
        Readable representation of the deck.
        
        :return: string
        """
        result = "Deck contains"
        if len(self.deck_cards) > 0:
            for i in range(len(self.deck_cards)):
                result += " " + str(self.deck_cards[i])
        else:
            result += " no card"
        return result


#define event handlers for buttons
def deal():
    """
    Start a new game and deal two cards to dealer and player.
    """
    global in_play, table_deck, cash, bet, allow_bet, total_lost
    global dealer_hand, dealer_msg, player_hand, player_msg
    
    # check if player has any money left. If not, report and ask to start a new session
    if cash <= 0:
        dealer_msg = "You don't have any money left!"
        player_msg = "Start a new session?"
    else:
        # reset game variables
        dealer_msg = ""
        table_deck = Deck() # create new deck
        table_deck.shuffle() # shuffle the deck
        dealer_hand = Hand() # create dealer hand
        player_hand = Hand() # create player hand
        # deal 2 cards to dealer and player
        for x in range(2):
            player_hand.add_card(table_deck.deal_card())
            dealer_hand.add_card(table_deck.deal_card())   
        # check if there was already a hand being played. If so, player loses the bet.
        if in_play and not allow_bet:
            dealer_msg = "You gave up your hand! You lose."
            cash -= bet
            total_lost += bet
        
        player_msg = "Hint or Stand?"
        bet = 5
        allow_bet = True
        in_play = True
    
        
        # for debug only
        if DEBUG:
            print "---- Deal() ----"
            print str(table_deck)
            print "Dealer "+ str(dealer_hand)
            print "Dealer hand value: "+ str(dealer_hand.get_value())
            print "Dealer msg: " + dealer_msg
            print "Player " + str(player_hand)
            print "Player hand value: " + str(player_hand.get_value())
            print "Player cash: " + str(cash) + " | Player bet: " + str(bet)
            print "Player msg: " + player_msg
            print

def hit():
    """
    Deal a card to the player.
    """
    global in_play, player_msg, dealer_msg, cash, bet, allow_bet, total_lost

    # check if player has any money left. If not, report and ask to start a new session
    if cash <= 0:
        dealer_msg = "You don't have any money left!"
        player_msg = "Start a new session?"
        in_play = False
    else:    
        allow_bet = False # doesn't allow to increase bet after hitting
        # if the hand is in play, hit the player
        if in_play:
            #if player is not busted, deal a card to player
            if player_hand.get_value() <= 21:
                player_hand.add_card(table_deck.deal_card())
                player_msg = "Hint or Stand?"
            # check if player busted (after dealing a card)
            if player_hand.get_value() > 21:
                in_play = False
                dealer_msg = "Player busted! You lose."
                player_msg = "New deal?"
                cash -= bet
                total_lost += bet
        else:
            player_msg = "New deal?"
        
        # for debug only
        if DEBUG:
            print "---- Hit() ----"
            print str(table_deck)
            print "Dealer "+ str(dealer_hand)
            print "Dealer hand value: "+ str(dealer_hand.get_value())
            print "Dealer msg: " + dealer_msg
            print "Player " + str(player_hand)
            print "Player hand value: " + str(player_hand.get_value())
            print "Player cash: " + str(cash) + " | Player bet: " + str(bet)
            print "Player msg: " + player_msg
            print
       
def stand():
    """
    Deal card(s) to the dealer.
    """
    global in_play, player_msg, dealer_msg
    global cash, bet, allow_bet, total_won, total_lost

    # check if player has any money left. If not, report and ask to start a new session
    if cash <= 0:
        dealer_msg = "You don't have any money left!"
        player_msg = "Start a new session?"
    else:
        # doesn't allow betting after stand
        allow_bet = False
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        if in_play:
            # get number of Aces in dealer hand
            num_of_aces = dealer_hand.count("A")
            # if dealer has Aces and the hand value isn't enough to beat player, count Aces
            # as 1 and deal a card (Aces value, 1 or 11, is matched in get_value()).
            if num_of_aces > 0 and dealer_hand.get_value() < player_hand.get_value():
                dealer_hand.add_card(table_deck.deal_card())
                num_of_aces = 0 # reset number of Aces for next verifications/loops

            # while dealer hand value is lower than 17, keep dealing cards to dealer
            # or if it's bigger than 17 but there are Aces, deal a card to match Ace value (1 or 11)
            while dealer_hand.get_value() < 17 or (dealer_hand.get_value() < player_hand.get_value() and num_of_aces == 0):
                dealer_hand.add_card(table_deck.deal_card())
            
            # check if dealer hand is bigger than player hand and lower or equal to 21
            # if yes, dealer wins
            if dealer_hand.get_value() <= 21 and dealer_hand.get_value() >= player_hand.get_value():
                dealer_msg = "You lose!"
                player_msg = "New deal?"
                cash -= bet
                total_lost += bet
            else: # if no (dealer busted or player hand value is bigger), player wins
                dealer_msg = "You win!"
                if dealer_hand.get_value() > 21:
                    dealer_msg = "Dealer busted! You win."
                player_msg = "New deal?"
                cash += bet
                total_won += bet
                
            in_play = False
                    
        else:
            player_msg = "New deal?"
    
        # for debug only
        if DEBUG:
            print "---- Stand() ----"
            print str(table_deck)
            print "Dealer "+ str(dealer_hand)
            print "Dealer hand value: "+ str(dealer_hand.get_value())
            print "Dealer msg: " + dealer_msg
            print "Player " + str(player_hand)
            print "Player hand value: " + str(player_hand.get_value())
            print "Player cash: " + str(cash) + " | Player bet: " + str(bet)
            print "Player msg: " + player_msg
            print

def increase_bet():
    """
    Increase bet value, by 5, to a max of 25.
    """
    global bet
    if in_play and bet < 25:
        bet +=5
    
def decrease_bet():
    """
    Decrease bet value, by 5, to a min of 5.
    """
    global bet
    if in_play and allow_bet and bet > 5:
        bet -=5
        
def new_session():
    """
    Start a new game session.
    """
    global cash, total_won, total_lost
    cash = 1000
    total_won = 0
    total_lost = 0
    deal()

def draw(canvas):
    """
    Draw game.
    """
    # Title
    canvas.draw_text("Blackjack", [20, 60], 60, "White")
    # Dealer text and hand
    canvas.draw_text("Dealer", [20, 150], 26, "White")
    canvas.draw_text(dealer_msg, [250, 150], 22, "Yellow")
    dealer_hand.draw(canvas, [20, 160])
    # Player text and hand
    canvas.draw_text("Player", [20, 360], 26, "White")
    canvas.draw_text(player_msg, [250, 360], 22, "Yellow")
    player_hand.draw(canvas, [20, 370])
    # game stats
    canvas.draw_text("Bet: " + str(bet), [10, 590], 24, "White")
    canvas.draw_text("Won: " + str(total_won), [125, 590], 24, "White")
    canvas.draw_text("Lost: " + str(total_lost), [300, 590], 24, "White")
    canvas.draw_text("Cash: " + str(cash), [460, 590], 24, "White")
    # betting chip(s)    
    for x in range(bet // 5):
        canvas.draw_image(chip_image, CHIP_CENTER, CHIP_SIZE,
                          [22 + x * CHIP_CENTER[0], 550], CHIP_SIZE)
    # if there's a game in play, cover dealear first card.
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [20 + CARD_BACK_CENTER[0], 160 + CARD_BACK_CENTER[1]],
                          CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_label("")
frame.add_button("Bet +5 (Max: 25)", increase_bet, 200)
frame.add_button("Bet -5 (Min:  5)", decrease_bet, 200)
frame.add_label("")
frame.add_button("New Session", new_session, 200)
frame.add_label("")
frame.add_label("")
frame.add_label("After hitting a card, you're only allowed to increase the bet.")
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()