#BlackJack Game:

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}

playing = True

#Class Definition:

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_card = ""
        for card in self.deck:
            deck_card += "\n " + card.__str__()
        return "This deck has:" + deck_card

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        deal_card = self.deck.pop()
        return deal_card

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -=10
            self.aces -=1

class Chips:
    
    def __init__(self):
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

#Function Definitions:

def take_bet(chip):
    while True:
        try:
            chip.bet = int(input('How many chips do you want to bet?'))
        except:
            print('Sorry, number of chips must be an integer.')
        else:
            if chip.total < chip.bet:
                print('Sorry, you cannot bet more than',chip.total)
            else:
                break    

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck,hand):
    global playing # to control an upcoming while loop
    
    while True:
        x = input('Would you like to hit or stand? (h or s)').lower()
        if x.startswith('h'):
            hit(deck,hand)
        
        elif x.startswith('s'):
            print('Player stands, dealer plays.')
            playing = False
        
        else: 
            print("Please enter 'hit' or 'stand'")
            continue
        break

def show_some(player,dealer):
    print('\nDealer Hands:')
    print('<Hidden card>')
    print(dealer.cards[1])
    print('\nPlayer Hands:', *player.cards, sep='\n')

def show_all(player,dealer):
    print('\nDealer Hands:', *dealer.cards, sep='\n')
    print('\nDealer Value:', dealer.value)
    print('\nPlayer Hands:', *player.cards, sep='\n')
    print('\nPlayer Value:', player.value)

def player_busts(player,dealer,chips):
    print('Player busts!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('Player wins!')
    chips.win_bet()    

def dealer_busts(player,dealer,chips):
    print('Dealer busts!')
    chips.win_bet()    
    
def dealer_wins(player,dealer,chips):
    print('Dealer wins!')
    chips.lose_bet()    
    
def push(player,dealer):
    print('Dealer and Player tie!')

#GamePlay

while True:
    # Print an opening statement
    print('Welcome to BlackJack, try to reach 21 but not over. Dealer will hit until reach at least 17.\n\
    Ace can take value as 1 or 11.')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
        
    # Set up the Player's chips
    player_chip = Chips()
    dealer_chip = Chips()
    
    # Prompt the Player for their bet
    take_bet(player_chip)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    
    while playing:
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chip)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
    
        # Show all cards
        show_all(player_hand, dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chip)
            
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand,dealer_hand,player_chip)
            
        elif player_hand.value < dealer_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chip)
            
        else:
            push(player_hand,dealer_hand)
    
    # Inform Player of their chips total 
    print("\nPlayer's chips stand at:",player_chip.total)
    
    # Ask to play again
    play = input('Would you like to play again? y or n').lower()

    if play[0] == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing.')
        break    


