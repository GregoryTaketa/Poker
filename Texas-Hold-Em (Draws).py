# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 00:45:32 2017

@author: greg
"""

#Texas Hold 'Em Draws and Folds Simulation

#At this time, I do not have an algorithm to rank face-up cards for betting purposes.

#For some reason, showing face values messes up the sorting, even if .copy a list.  All_hands absorbs the face values, which messes up sorting later.

import random

#NUMBER OF STARTING PLAYERS
starting_players = int(input("Welcome to the Texas Hold 'Em Draw Simulation!  How many Players (2 to 22)? "))
while starting_players < 2 or starting_players > 22:
    starting_players = int(input("Very funny.  Pick a number of 2 to 22. "))
starting_players_list = list(range(0,starting_players))

#Form the 52-card Deck
def form_deck():
    """Form 52 Cards"""
    numbers = list(range(2,15))
    #faces = ["J", "Q", "K", "A"]
    values = numbers #+ faces
    suites = ["D", "C", "H", "S"]
    new_deck = [[v,s] for s in suites for v in values]
    return new_deck

#Store form_deck() results as new_deck to reset deck w/o re-running
new_deck = form_deck()

#Computer's propensity to Fold
they_fold = 0.35

#Form option to Fold
def fold ():
    global folded
    global players
    removal = []
    for player in players:
        if len(players)-len(removal) == 1: #len(players) does not update with each iteration of this loop, it seems.  But removal does.
            print("Player ", str(player+1)," wins.")
            break
        #You decide whether to fold
        elif player == you:
            you_fold = input("Do you want to fold (y/n)? ")
            if you_fold == 'y':
                print("You have folded from this game.")
                folded.append(player+1)
                #players.remove(player) #Skips you when previous player folds.
                removal.append(player)
        #Computers randomly fold based on pre-determined propensity
        else:
            if random.random() < they_fold:
                print("Player ",str(player+1)," has folded.")
                folded.append(player+1)
                #players.remove(player)
                removal.append(player)
    #Separate for loop for removing players because previous version skips you when previous players is removed.
    for person in removal:
        players.remove(person)
    return players, folded

def Suite(item):
    return item[1]

def Value(item):
    return item[0]

def sort_hand(stuff):
    """Sort the hand by Value then Suite"""
    stuff.sort(key=Suite) #inplace, but hasn't been a problem with .copy() because didn't affect .index(final_hand) at the end
    stuff.sort(key=Value)
    return stuff

#This is problematic because Face Values absorbed into all_hands
def show_face(blah):
    """Convert numbers to Faces"""
    for card in blah:
        if card[0] == 11:
            card[0]="J"
        elif card[0]== 12:
            card[0]="Q"
        elif card[0]== 13:
            card[0]="K"
        elif card[0] == 14:
            card[0]="A"
        else:
            card[0]=card[0]
    return blah

#1st Round of Drawing       
def two_holes ():
    """Draw 2 holes."""
    global all_hands
    global deck
    global players
    #Set of all cards for the two holes   
    two_holes_draws = random.sample(deck, len(players)*2)
    #Remove drawn cards from deck
    for card in two_holes_draws:
            deck.remove(card)
    #Deal 1 Card Each Player Until 2.  
    for player in players:
        hand = []
        for i in range(0,2):
            hand.append(two_holes_draws[player+len(players)*i])
        all_hands.append(hand)
    
    #Only you can see your 2 holes.
    your_hand = all_hands[you].copy()
    your_sorted = sort_hand(your_hand)
    #your_shown = show_face(your_sorted)
    print("Your hand is: ", str(your_sorted))#your_shown))
            
#/Subsequent Rounds of Drawing
def flop_turn_river():
    """In flop/turn/river, burn a card and draw 1 card for Community"""
    global all_hands
    global burn
    global community
    global deck
    global folded
    global players
    global turn 
    
    #Burn the top card
    burn_card = random.sample(deck, 1)
    burn.append(burn_card[0])
    print("Burn pile is", str(burn))
    deck.remove(burn_card[0]) #burn_card is a list, so remove as element
    
    #Turns determine flop, turn, or river
    if turn == 2:
        deal = 3
    else:
        deal = 1
    
    #Draw the cards
    draw = random.sample(deck, deal)
    for card in draw:
        deck.remove(card) #draw is a list, but must remove by elements
        community.append(card)
        for player in players:
            all_hands[player].append(card) #accumulate community with hands
    
    #Reveal face-up cards and folded players
    print("The Community Pile is: ", str(community))
    your_hand = all_hands[you].copy()
    your_sorted = sort_hand(your_hand)
    #your_shown = show_face(your_sorted)
    print("Your hand is: ", str(your_sorted))#your_shown))
    print("Folded Players are: ",str(folded))
    turn = turn + 1

#After asking for players, the game runs in a voluntary loop, resetting the deck each iteration.
go = 'y'
while go != 'n':
    players = list(starting_players_list) #Reset the number of players
    you = random.randrange(0,len(players))  #Reset your position
    print("")
    print("This game, you are Player ", str(you+1))
    print("")
    folded = [] #Reset the folded players
    deck = list(new_deck) #Reset the deck
    burn = [] #Reset the burn cards
    community = [] #Reset the community pile
    all_hands = [] #Reset the hands
    two_holes()
    print("")
    fold()
    print("")
    turn = 2
    if len(players) > 1:
        while turn <= 4:
            flop_turn_river()
            print("")
            fold()
            print("")
            if len(players) <= 1:
                break
    for player in players:
        if player == you:
            print("Last Round Player: ",str(player+1),"(you)")
        else:
            print("Last Round Player: ",str(player+1))
    for final_hand in all_hands:
        final_hand_copy = final_hand.copy()
        sorted_hand = sort_hand(final_hand_copy)
        #show_hand = show_face(sorted_hand)
        print("Player ", str(all_hands.index(final_hand)+1),"'s Hand: ", str(sorted_hand))#show_hand))
    print("Burn pile: ",str(burn))
    go = input("Wanna play again (y/n)? ") #Since the 'Enter' key is not 'n', you could just hit 'Enter' to draw again lazily.
    print("")