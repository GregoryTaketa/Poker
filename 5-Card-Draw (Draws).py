# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 01:44:39 2017

@author: greg
"""

#5-Card Draw Poker:  Draw Simulation

import random

#NUMBER OF PLAYERS
players = int(input("Welcome to 5-Card Poker Draw Simulation!  How many Players? "))
player_list = list(range(0,players))

#Initialize deck and discard_pile as global variable.
deck = []
discard_pile = []


#Use the form_deck function to allow resetting the deck when repeating game.
def form_deck():
    """Form 52 Cards + Jokers"""
    numbers = list(range(2,11))
    faces = ["J", "Q", "K", "A"]
    values = numbers + faces
    suites = ["D", "C", "H", "S"]
    deck = [(v,s) for s in suites for v in values]
    deck.append(('Joker','Black'))
    deck.append(('Joker','Color'))
    discard_pile = []
    return deck, discard_pile

#Discard will serve as an inner function to the deal function.
def discard(hand, deck, player_number):
    """Discard up to 3 cards (or 4 if possessing an Ace or Joker).  Then re-draw."""
    replace = 0 #initialize to keep while loop of discards going
    high = 0 #initialize to count Aces or Jokers to discard up to 4
    #Count Aces and Jokers to discard up to 4
    for card in hand:
        if card[0] == 'A' or card[0] == 'Joker':
            high = high + 1
    if high > 0:
        i = 4
    else:
        i = 3
    #Discarding
    while replace != 6 and i > 0:
        print("Player ", str(player_number), ", you may discard up to ", str(i), " cards.")
        for index, value in enumerate(hand):
            print(index, value)
        print("")
        replace = int(input("Type the number left of one of the cards you want to discard.  If you do not want to discard any, type 6. "))
        print("")
        if replace !=6:
            print("Discarding " + str(hand[replace]))
            print("")
            discard_pile.append(hand[replace])
            print("Discard pile" + str(discard_pile))
            print("")
            del hand[replace]
            i = i - 1
    #Perform second draw
    second_draw = random.sample(deck, 5-len(hand))
    for card in second_draw:
        deck.remove(card)
    hand = hand + second_draw
    print("Player ", str(player_number), "'s hand is:")
    for index, value in enumerate(hand):
        print(index, value)
    print("")    
    
def deal (deck, player_list):
    """Draw 5 cards per Player.  Each Player discards and draws."""
    #Set of all cards for 1st draw    
    first_draws = random.sample(deck, players*5)
    #Remove drawn cards from deck
    for card in first_draws:
            deck.remove(card)
    print("")
    #Deal 1 Card Each Player Until 5, then Discard and Re-Draw
    for player in player_list:
        hand = []
        for j in range(0,5):
            hand.append(first_draws[player+players*j])
        discard(hand, deck, player)


#After asking for players, the game runs in a voluntary loop, resetting the deck each iteration.
go = 'y'
while go != 'n':
    deck, discard_pile = form_deck() #Reset the deck
    deal(deck, player_list)
    go = input("Wanna play again (y/n)? ") #Since the 'Enter' key is not 'n', you could just hit 'Enter' to draw again lazily.