# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 14:12:56 2017

@author: greg
"""

#7-Card Stud Poker:  Draw Simulation

#At this time, I do not have an algorithm to rank face-up cards for betting purposes.

import random

#NUMBER OF STARTING PLAYERS
starting_players = int(input("Welcome to the 7-Card Stud Draw Simulation!  How many Players (2 to 8)? "))
while starting_players < 2 or starting_players > 8:
    starting_players = int(input("Very funny.  Pick a number of 2 to 8. "))
starting_players_list = list(range(0,starting_players))

#Form the 52-card Deck
def form_deck():
    """Form 52 Cards"""
    numbers = list(range(2,11))
    faces = ["J", "Q", "K", "A"]
    values = numbers + faces
    suites = ["D", "C", "H", "S"]
    new_deck = [(v,s) for s in suites for v in values]
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
    
#1st Round of Drawing       
def third_street ():
    """Draw 2 holes and 1 face-up card per Player.  May fold."""
    global all_hands
    global deck
    global players
    #Set of all cards for third street draw    
    third_street_draws = random.sample(deck, len(players)*3)
    #Remove drawn cards from deck
    for card in third_street_draws:
            deck.remove(card)
    #Deal 1 Card Each Player Until 3, then reveal third street.
    for player in players:
        hand = []
        for i in range(0,3):
            hand.append(third_street_draws[player+len(players)*i])
        all_hands.append(hand)
        if player == you:
            print("Your hand is: ", str(all_hands[you]))
        else:
            print("Player ", str(player+1), "'s 3rd Street hand is: ", str(hand[2]))

#Subsequent Rounds of Drawing, 4th to 6th Street:    
def next_street():
    global all_hands
    global burn
    global deck
    global folded
    global players
    global turn 
    #Burn the top card for each Street after 3rd
    burn_card = random.sample(deck, 1)
    burn.append(burn_card[0])
    print("Burn pile is", str(burn))
    deck.remove(burn_card[0]) #burn_card is a list, so remove as element
    
    #Draw the cards
    draw = random.sample(deck, len(players))
    for card in draw:
        deck.remove(card) #draw is a list, but must remove by elements
    for player in players:
        #the index of players will not match the numbered elements
        new_card = draw[players.index(player)]
        all_hands[player].append(new_card)
    
    #Reveal face-up cards and folded players
    for player in starting_players_list:    
        if player == you:
            print("Your hand is: ", str(all_hands[you]))
        else:
            print("Player ",str(player+1),"'s ", str(turn),"th Street hand is: ", str(all_hands[player][2:]))
    print("Folded Players are: ",str(folded))
    
    turn = turn + 1
    
def river ():
    global all_hands
    global burn
    global deck
    global players
    #If not enough cards for everyone:
    if len(players) > len(deck):
        #If you can still burn 1 before Community Card:
        if len(deck) > 1:
            burn_card = random.sample(deck, 1)
            burn.append(burn_card[0])
            print("Burn pile is", str(burn))
            deck.remove(burn_card[0])
            draw = random.sample(deck,1)
            print("Not enough cards for remaining players, so Community Card is: ", str(draw))
            for player in players:
                all_hands[player].append(draw[0])
        #If you really only have 1 card left:
        else:
            draw = random.sample(deck,1)
            print("Not enough cards for remaining players, so Community Card is: ", str(draw))
            for player in players:
                all_hands[player].append(draw[0])
    
    #If exactly enough cards for everyone:
    elif len(players) == len(deck):
        draw = random.sample(deck, len(players))
        for player in players:
            #the index of players will not match the numbered elements
            new_card = draw[players.index(player)]
            all_hands[player].append(new_card)
    
    #If enough to burn and draw for everyone:
    else:
        burn_card = random.sample(deck, 1)
        burn.append(burn_card[0])
        print("Burn pile is", str(burn))
        deck.remove(burn_card[0])
    
        draw = random.sample(deck, len(players))
        for card in draw:
            deck.remove(card) #draw is a list, but must remove by elements
        for player in players:
            #the index of players will not match the numbered elements
            new_card = draw[players.index(player)]
            all_hands[player].append(new_card)

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
    all_hands = [] #Reset the hands
    third_street()
    print("")
    fold()
    print("")
    turn = 4
    if len(players) > 1:
        while turn < 7:
            next_street()
            print("")
            fold()
            print("")
            if len(players) <= 1:
                break
    if len(players) > 1:
        river ()
    for player in players:
        if player == you:
            print("Last Round Player: ",str(player+1),"(you)")
        else:
            print("Last Round Player: ",str(player+1))
    for hand in all_hands:
        print("Player ", str(all_hands.index(hand)+1),"'s Hand: ", str(hand))
    print("Burn pile: ",str(burn))
    go = input("Wanna play again (y/n)? ") #Since the 'Enter' key is not 'n', you could just hit 'Enter' to draw again lazily.
    print("")