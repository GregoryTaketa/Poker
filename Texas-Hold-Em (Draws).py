# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 22:31:44 2017

@author: greg
"""

#TEXAS HOLD 'EM DRAW

import random

#FORM 52-CARD DECK
numbers = list(range(2,11))
faces = ["J", "Q", "K", "A"]
values = numbers + faces
suites = ["D", "C", "H", "S"]
deck = [(v,s) for s in suites for v in values]

#ADD JOKERS, THOUGH RARE IN TEXAS HOLD 'EM
joker = input("Do you use Jokers (y/n)? ")
if joker == "y":
    deck.append(('Joker','Black'))
    deck.append(('Joker','Color'))
    
#NUMBER OF PLAYERS
players = int(input("How many Players? "))
player_list = list(range(0,players))

def deal (deck, player_list):
    """Draw 2 cards per Player, 3 for Flop, 1 for Turn, and 1 for River, without replacement.  Can Rerun the draws."""
    go = 'y'
    while go != 'n':
        draws = random.sample(deck, players*2+5)
        print("")
        #Reveal Players' Hands; Dealt 1 Card Each Time
        for player in player_list:
            print("Player " + str(player_list.index(player)+1)+":")
            print(draws[player])
            print(draws[player+players])
            print("")
        #Reveal Flop, Turn & River
        community = draws[players*2:]
        it = iter(community)
        print("Flop:")
        print(next(it))
        print(next(it))
        print(next(it))
        print("")
        print("Turn:")
        print(next(it))
        print("")
        print("River:")
        print(next(it))
        go = input("Wanna play again (y/n)? ") #Since the 'Enter' key is not 'n', you could just hit 'Enter' to draw again lazily.
    
deal(deck, player_list)
